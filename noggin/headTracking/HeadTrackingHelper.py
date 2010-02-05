from . import TrackingConstants as constants
import man.motion as motion
from man.motion import MotionConstants
from ..util import MyMath as MyMath
from man.motion import StiffnessModes
from math import (fabs, sin, cos, pi, hypot)

class HeadTrackingHelper():
    def __init__(self, tracker):
        self.tracker = tracker

    def executeHeadMove(self, headMove):
        """performs a sweetmove"""
        for position in headMove:
            if len(position) == 4:
                move = motion.HeadJointCommand(position[1] ,# time
                                               position[0], # head pos
                                               position[3], # chain stiffnesses
                                               position[2], # interpolation type
                                               )
            else:
                self.printf("What kind of sweet ass-Move is this?")

            self.tracker.brain.motion.enqueue(move)


    def trackObject(self):
        """
        Method to actually perform the tracking.
        Should only be called explicitly from state
        methods in TrackingStates.py
        """
        #if self.firstFrame():
         #   self.brain.motion.stopHeadMoves()
        (changeX,changeY) = (0., 0.)
        # Find the target's angular distance from the center of the screen
        # if we have an object, track that
        if self.tracker.target and \
                self.tracker.target.on:
            changeX = self.tracker.target.angleX
            changeY = self.tracker.target.angleY #the pitch is pos = down
        else:
            # by default, the change is none
            #self.printf( "No object")
            return

        motionAngles = self.tracker.brain.sensors.motionAngles
        curPitch = motionAngles[MotionConstants.HeadPitch]
        curYaw = motionAngles[MotionConstants.HeadYaw]

        maxChange = 13.0

        #Warning- no gain is applied currently!
        safeChangeX = MyMath.clip(changeX, -maxChange, maxChange )
        safeChangeY = MyMath.clip(changeY, -maxChange, maxChange )

        newYaw = curYaw + safeChangeX/3
        newPitch = curPitch - safeChangeY/3

        newYaw = MyMath.clip(newYaw, -80., 80.)

        maxSpeed = 2.0
        headMove = motion.SetHeadCommand(newYaw, newPitch,
                                         maxSpeed, maxSpeed)
        self.tracker.brain.motion.setHead(headMove)

    def panTo(self, heads):
        """
        Pan heads at appropriate speed to given heads
        """
        motionAngles = self.tracker.brain.sensors.motionAngles

        headPitch = motionAngles[MotionConstants.HeadPitch]
        headYaw = motionAngles[MotionConstants.HeadYaw]

        yawDiff = fabs(heads[0] - headYaw)
        pitchDiff = fabs(heads[1] - headPitch)


        maxDiff = max(pitchDiff, yawDiff)
        panTime = maxDiff/constants.MAX_PAN_SPEED
        self.executeHeadMove( ((heads, panTime, 0,
                                 StiffnessModes.LOW_HEAD_STIFFNESSES), ) )

    def lookToPoint(self):
        """look to an absolute position on the field"""
        t = self.tracker
        my = t.brain.my

        globalRelX = t.visGoalX - my.x
        globalRelY = t.visGoalY - my.y

        dist = hypot(globalRelX, globalRelY)

        bearingToPointInDeg = MyMath.getRelativeBearing( my.x, my.y, my.h,
                                                         t.visGoalX,
                                                         t.visGoalY )
        bearingToPointInRad = bearingToPointInDeg * (pi/180.)

        xRelMe = dist*cos(bearingToPointInRad)
        yRelMe = dist*sin(bearingToPointInRad)

        #relH is relative to camera height. negative is normal
        lensHeightInCM = self.getCameraHeight()
        relHeight = lensHeightInCM - t.visGoalHeight
        headMove = motion.CoordHeadCommand( xRelMe, yRelMe, relHeight )
        t.brain.motion.coordHead(headMove)


    def getCameraHeight(self):
        """gets the height of the (hopefully)lower camera in cm"""
        pose = self.tracker.brain.vision.pose
        cameraInWorldFrameZ = pose.cameraInWorldFrameZ
        comHeight = pose.bodyCenterHeight
        lensHeight = cameraInWorldFrameZ + comHeight
        lensHeightInCM = lensHeight/10.
        return lensHeightInCM
