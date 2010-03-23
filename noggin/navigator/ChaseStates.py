from man.noggin.util import MyMath
from man.noggin.navigator import ChaseTransitions as transitions
from man.noggin.navigator import ChaseHelper as cHelper
from man.noggin.navigator import NavHelper as helper

DEBUG = False

def chase(nav):

    if transitions.shouldScanFindBall(player):
        return player.goNow('stop')
    elif transitions.shouldApproachBallWithLoc(player):
        return player.goNow('approachBallWideWalk')
    elif transitions.shouldApproachBall(player):
        return player.goNow('approachBall')
    elif transitions.shouldKick(player):
        return player.goNow('stop')
    elif transitions.shouldTurnToBall_ApproachBall(player):
        return player.goNow('turnToBall')
    else:
        return player.goNow('stop')

def approachBallStraight(nav):
    """
    Once we are alligned with the ball, approach it
    """
    if nav.firstFrame():
        nav.hasAlignedOnce = False
        nav.brain.CoA.setRobotGait(nav.brain.motion)

    x,y,theta = cHelper.getBallApproachParam(nav.brain.ball)
    helper.setSpeed(nav, x, y, theta)

    if nav.brain.player.penaltyKicking and \
           nav.brain.ball.InOppGoalBox():
        return player.goNow('penaltyBallInOppGoalbox')

    elif transitions.shouldPositionForKick(player):
        return player.goNow('positionForKick')

    elif transitions.shouldNotGoInBox(player):
        return player.goLater('ballInMyBox')

    elif transitions.shouldChaseAroundBox(player):
        return player.goLater('chaseAroundBox')

    elif transitions.shouldApproachBallWithLoc(player):
        return player.goNow('approachBallWithLoc')

    elif transitions.shouldTurnToBall_ApproachBall(player):
        return player.goLater('spinToBall')

    elif not player.brain.tracker.activeLocOn and \
            transitions.shouldScanFindBall(player):
        return player.goLater('stop')

    elif player.brain.tracker.activeLocOn and \
            transitions.shouldScanFindBallActiveLoc(player):
        return player.goLater('stop')

    elif transitions.shouldAvoidObstacleDuringApproachBall(player):
        return player.goLater('avoidObstacle')

    return nav.stay()

def spinToBall(nav):
    """
    Rotate to align with the ball. When we get close, we will approach it
    """
    ball = nav.brain.ball

    if nav.firstFrame():
        nav.hasAlignedOnce = False
        nav.brain.CoA.setRobotGait(nav.brain.motion)

    # Determine the speed to turn to the ball
    turnRate = MyMath.clip(ball.bearing * constants.BALL_SPIN_GAIN,
                           -constants.BALL_SPIN_SPEED,
                           constants.BALL_SPIN_SPEED)

    # Avoid spinning so slowly that we step in place
    if fabs(turnRate) < constants.MIN_BALL_SPIN_MAGNITUDE:
        turnRate = MyMath.sign(turnRate) * constants.MIN_BALL_SPIN_MAGNITUDE

    if ball.on:
        nav.setSpeed(nav, x=0, y=0, theta=turnRate)

    if transitions.shouldKick(player):
        return player.goNow('stop')
    elif transitions.shouldPositionForKick(nav):
        return nav.goNow('positionForKick')
    elif transitions.shouldApproachBall(nav):
        return nav.goLater('approachBallStraight')
    elif transitions.shouldScanFindBall(player):
        return player.goLater('stop')


    return nav.stay()

def approachBallWithLoc(self, target):
    '''
    will act similarily to current approachBallWithLoc
    '''
    if nav.firstFrame():
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        nav.hasAlignedOnce = False

    my = nav.brain.my

    dest = cHelper.getApproachPosition()

    walkX, walkY, walkTheta = helper.getWalkStraightParam(my, dest)
    helper.setSpeed(nav, walkX, walkY, walkTheta)

    if useOmni = my.dist(dest) <= constants.APPROACH_OMNI_DIST:
        nav.changeOmniGoToCounter += 1
        if nav.changeOmniGoToCounter > PositionConstants.CHANGE_OMNI_THRESH:
            return nav.goLater('approachBallWideOmni')
    else :
        nav.changeOmniGoToCounter = 0

    if transitions.shouldKick(nav):
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goNow('stop')
    elif transitions.shouldPositionForKickFromApproachLoc(nav):
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('positionForKick')
    elif transitions.shouldNotGoInBox(nav):
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('ballInMyBox')
    elif transitions.shouldChaseAroundBox(nav):
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('chaseAroundBox')
    elif transitions.shouldAvoidObstacleDuringApproachBall(nav):
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('avoidObstacle')
    elif my.locScoreFramesBad > constants.APPROACH_NO_LOC_THRESH:
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('approachBallStraight')

    return nav.stay()

def approachBallWithLocOmni(self, target):
    '''
    will act similarily to current approachBallWithLoc
    '''
    if nav.firstFrame():
        nav.hasAlignedOnce = False
        nav.brain.CoA.setRobotSlowGait(nav.brain.motion)

    my = nav.brain.my

    dest = cHelper.getApproachPosition()

    walkX, walkY, walkTheta = helper.getOmniWalkParam(my, dest)
    helper.setSpeed(nav, walkX, walkY, walkTheta)

    if my.dist(dest) >= constants.APPROACH_OMNI_DIST
        nav.changeOmniGoToCounter += 1
        if nav.changeOmniGoToCounter > PositionConstants.CHANGE_OMNI_THRESH:
            return nav.goLater('approachBalWideWalk')
    else :
        nav.changeOmniGoToCounter = 0

    if transitions.shouldKick(nav):
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goNow('stop')
    elif transitions.shouldPositionForKickFromApproachLoc(nav):
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('positionForKick')
    elif transitions.shouldNotGoInBox(nav):
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('ballInMyBox')
    elif transitions.shouldChaseAroundBox(nav):
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('chaseAroundBox')
    elif transitions.shouldAvoidObstacleDuringApproachBall(nav):
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('avoidObstacle')
    elif my.locScoreFramesBad > constants.APPROACH_NO_LOC_THRESH:
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('approachBallStraight')

    return nav.stay()

def positionForKick(self):
    """
    State to align on the ball once we are near it
    """

    if nav.firstFrame():
        nav.brain.CoA.setRobotSlowGait(nav.brain.motion)

    ball = nav.brain.ball

    nav.inKickingState = True
    # Leave this state if necessary
    if transitions.shouldKick(nav):
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goNow('waitBeforeKick')
    elif transitions.shouldScanFindBall(nav):
        nav.inKickingState = False
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('scanFindBall')
    elif transitions.shouldTurnToBallFromPositionForKick(nav):
        nav.inKickingState = False
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('spinToBall')
    elif transitions.shouldApproachFromPositionForKick(nav):
        nav.inKickingState = False
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('approachBallStraight')

    # Determine approach speed
    targetY = ball.relY

    sY = MyMath.clip(targetY * constants.PFK_Y_GAIN,
                     constants.PFK_MIN_Y_SPEED,
                     constants.PFK_MAX_Y_SPEED)

    sY = max(constants.PFK_MIN_Y_MAGNITUDE,sY) * MyMath.sign(sY)

    if transitions.shouldApproachForKick(nav):
        targetX = (ball.relX -
                   (constants.BALL_KICK_LEFT_X_CLOSE +
                    constants.BALL_KICK_LEFT_X_FAR) / 2.0)
        sX = MyMath.clip(ball.relX * constants.PFK_X_GAIN,
                         constants.PFK_MIN_X_SPEED,
                         constants.PFK_MAX_X_SPEED)
    else:
        sX = 0.0

    if ball.on:
        helper.setSpeed(sX,sY,0)
    return nav.stay()

def dribble(nav):
    """
    Keep running at the ball, but dribble
    """
    if nav.firstFrame():
        nav.brain.CoA.setRobotDribbleGait(nav.brain.motion)

    # if we should stop dribbling, see what else we should do
    if transitions.shouldStopDribbling(nav):

        if transitions.shouldKick(nav):
            return nav.goNow('waitBeforeKick')
        elif transitions.shouldPositionForKick(nav):
            return nav.goNow('positionForKick')
        elif transitions.shouldApproachBall(nav):
            return nav.goNow('approachBallStraight')

    helper.setSpeed(cHelper.getApproachTargetParam(nav.brain.ball))

    return nav.stay()

# WARNING: avoidObstacle could possibly go into our own box
def avoidObstacle(nav):
    """
    If we detect something in front of us, dodge it
    """
    if nav.firstFrame():
        nav.doneAvoidingCounter = 0
        nav.printf(nav.brain.sonar)

        nav.brain.CoA.setRobotGait(nav.brain.motion)

        if (transitions.shouldAvoidObstacleLeft(nav) and
            transitions.shouldAvoidObstacleRight(nav)):
            # Backup
            nav.printf("Avoid by backup");
            nav.setWalk(constants.DODGE_BACK_SPEED, 0, 0)

        elif transitions.shouldAvoidObstacleLeft(nav):
            # Dodge right
            nav.printf("Avoid by right dodge");
            nav.setWalk(0, constants.DODGE_RIGHT_SPEED, 0)

        elif transitions.shouldAvoidObstacleRight(nav):
            # Dodge left
            nav.printf("Avoid by left dodge");
            nav.setWalk(0, constants.DODGE_LEFT_SPEED, 0)

    if not transitions.shouldAvoidObstacle(nav):
        nav.doneAvoidingCounter += 1
    else :
        nav.doneAvoidingCounter -= 1
        nav.doneAvoidingCounter = max(0, nav.doneAvoidingCounter)

    if nav.doneAvoidingCounter > constants.DONE_AVOIDING_FRAMES_THRESH:
        nav.shouldAvoidObstacleRight = 0
        nav.shouldAvoidObstacleLeft = 0
        return nav.goLater(nav.lastDiffState)

    return nav.stay()

def chaseAroundBox(nav):
    if nav.firstFrame():
        nav.shouldNotChaseAroundBox = 0

        nav.brain.CoA.setRobotGait(nav.brain.motion)

    if transitions.shouldKick(nav):
        return nav.goNow('waitBeforeKick')
    elif transitions.shouldScanFindBall(nav):
        return nav.goLater('scanFindBall')
    elif transitions.shouldAvoidObstacle(nav): # Has potential to go into box!
        return nav.goLater('avoidObstacle')

    if not transitions.shouldChaseAroundBox(nav):
        nav.shouldChaseAroundBox += 1
    else :
        nav.shouldChaseAroundBox = 0
    if nav.shouldChaseAroundBox > constants.STOP_CHASING_AROUND_BOX:
        return nav.goLater('chase')

    ball = nav.brain.ball
    my = nav.brain.my
    if my.x > NogginConstants.MY_GOALBOX_RIGHT_X:
        # go to corner nearest ball
        if ball.y > NogginConstants.MY_GOALBOX_TOP_Y:
            ##### FIX_ME
            nav.goTo( (NogginConstants.MY_GOALBOX_RIGHT_X +
                       constants.GOALBOX_OFFSET,
                       NogginConstants.MY_GOALBOX_TOP_Y +
                       constants.GOALBOX_OFFSET,
                       NogginConstants.MY_GOAL_HEADING ))

        if ball.y < NogginConstants.MY_GOALBOX_BOTTOM_Y:
            ##### FIX_ME
            nav.goTo(( NogginConstants.MY_GOALBOX_RIGHT_X +
                       constants.GOALBOX_OFFSET,
                       NogginConstants.MY_GOALBOX_BOTTOM_Y -
                       constants.GOALBOX_OFFSET,
                       NogginConstants.MY_GOAL_HEADING ))

    if my.x < NogginConstants.MY_GOALBOX_RIGHT_X:
        # go to corner nearest ball
        if my.y > NogginConstants.MY_GOALBOX_TOP_Y:
            ##### FIX_ME
            nav.goTo(( NogginConstants.MY_GOALBOX_RIGHT_X +
                       constants.GOALBOX_OFFSET,
                       NogginConstants.MY_GOALBOX_TOP_Y +
                       constants.GOALBOX_OFFSET,
                       NogginConstants.MY_GOAL_HEADING ))

        if my.y < NogginConstants.MY_GOALBOX_BOTTOM_Y:
            ##### FIX_ME
            nav.goTo(( NogginConstants.MY_GOALBOX_RIGHT_X +
                       constants.GOALBOX_OFFSET,
                       NogginConstants.MY_GOALBOX_BOTTOM_Y -
                       constants.GOALBOX_OFFSET,
                       NogginConstants.MY_GOAL_HEADING ))
    return nav.stay()

def orbitBeforeKick(nav):
    """
    State for circling the ball when we're facing our goal.
    """
    brain = nav.brain
    my = brain.my
    if nav.firstFrame():
        nav.orbitStartH = my.h
        brain.CoA.setRobotGait(brain.motion)

        shotPoint = KickingHelpers.getShotCloseAimPoint(nav)
        bearingToGoal = my.getRelativeBearing(shotPoint)
        spinDir = -MyMath.sign(bearingToGoal)

        ####FIX-ME
        nav.orbitAngle(spinDir * 90)

    if not nav.brain.tracker.activeLocOn and \
            transitions.shouldScanFindBall(nav):
        nav.brain.CoA.setRobotGait(nav.brain.motion)
        return nav.goLater('scanFindBall')

    elif brain.ball.dist > constants.STOP_ORBIT_BALL_DIST:
        return nav.goLater('chase')

    ##### FIX_ME
    if nav.isStopped() and not nav.firstFrame():
        return nav.goLater('positionForKick')
    return nav.stay()
