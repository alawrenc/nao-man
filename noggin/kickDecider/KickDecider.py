from ..players import KickingConstants as constants
from .. import NogginConstants
from ..typeDefs.Location import Location

class KickDecider:
    """
    Class to hold all the things we need to decide a kick
    """

    def __init__(self, brain):
        self.chosenKick = None
        self.justKicked = False
        self.bigKick = False

        self.kickObjective = None


        # Kickoff kick
        self.hasKickedOffKick = True

        self.oppGoalLeftPostBearings = []
        self.oppGoalRightPostBearings = []
        self.myGoalLeftPostBearings = []
        self.myGoalRightPostBearings = []

        self.oppGoalLeftPostDists = []
        self.oppGoalRightPostDists = []
        self.myGoalLeftPostDists = []
        self.myGoalRightPostDists = []

        self.oppLeftPostBearing = None
        self.oppRightPostBearing = None
        self.myLeftPostBearing = None
        self.myRightPostBearing = None

        self.oppLeftPostDist = 0.0
        self.oppRightPostDist = 0.0
        self.myLeftPostDist = 0.0
        self.myRightPostDist = 0.0


        self.sawOwnGoal = False
        self.sawOppGoal = False

        self.brain = brain
        self.ballForeFoot = constants.LEFT_FOOT

    def update(self):
        self.collectData()
        self.calculate()

    def resetData(self):
        """
        reset data btwn frames to avoid confusion
        """
        self.chosenKick = None
        self.justKicked = False
        self.bigKick = False

        self.kickObjective = None

        # Kickoff kick
        self.hasKickedOffKick = True

        self.oppGoalLeftPostBearings = []
        self.oppGoalRightPostBearings = []
        self.myGoalLeftPostBearings = []
        self.myGoalRightPostBearings = []

        self.oppGoalLeftPostDists = []
        self.oppGoalRightPostDists = []
        self.myGoalLeftPostDists = []
        self.myGoalRightPostDists = []

        self.oppLeftPostBearing = None
        self.oppRightPostBearing = None
        self.myLeftPostBearing = None
        self.myRightPostBearing = None

        self.oppLeftPostDist = 0.0
        self.oppRightPostDist = 0.0
        self.myLeftPostDist = 0.0
        self.myRightPostDist = 0.0

        self.sawOwnGoal = False
        self.sawOppGoal = False


    def collectData(self):
        """
        Collect info on any observed goals
        """
        if self.brain.myGoalLeftPost.on:
            if self.brain.myGoalLeftPost.certainty == NogginConstants.SURE:
                self.sawOwnGoal = True
                self.myGoalLeftPostBearings.append(self.brain.myGoalLeftPost.bearing)
                self.myGoalLeftPostDists.append(self.brain.myGoalLeftPost.dist)

        if self.brain.myGoalRightPost.on:
            if self.brain.myGoalRightPost.certainty == NogginConstants.SURE:
                self.sawOwnGoal = True
                self.myGoalRightPostBearings.append(self.brain.myGoalRightPost.bearing)
                self.myGoalRightPostDists.append(self.brain.myGoalRightPost.dist)

        if self.brain.oppGoalLeftPost.on:
            if self.brain.oppGoalLeftPost.certainty == NogginConstants.SURE:
                self.sawOppGoal = True
                self.oppGoalLeftPostBearings.append(self.brain.oppGoalLeftPost.bearing)
                self.oppGoalLeftPostDists.append(self.brain.oppGoalLeftPost.dist)

        if self.brain.oppGoalRightPost.on:
            if self.brain.oppGoalRightPost.certainty == NogginConstants.SURE:
                self.sawOppGoal = True
                self.oppGoalRightPostBearings.append(self.brain.oppGoalRightPost.bearing)
                self.oppGoalRightPostDists.append(self.brain.oppGoalRightPost.dist)

    def calculate(self):
        """
        Get usable data from the collected data
        """
        if len(self.myGoalLeftPostBearings) > 0:
            self.myLeftPostBearing = (sum(self.myGoalLeftPostBearings) /
                                      len(self.myGoalLeftPostBearings))
        if len(self.myGoalRightPostBearings) > 0:
            self.myRightPostBearing = (sum(self.myGoalRightPostBearings) /
                                       len(self.myGoalRightPostBearings))
        if len(self.oppGoalLeftPostBearings) > 0:
            self.oppLeftPostBearing = (sum(self.oppGoalLeftPostBearings) /
                                       len(self.oppGoalLeftPostBearings))
        if len(self.oppGoalRightPostBearings) > 0:
            self.oppRightPostBearing = (sum(self.oppGoalRightPostBearings) /
                                        len(self.oppGoalRightPostBearings))

        if len(self.myGoalLeftPostDists) > 0:
            self.myLeftPostDist = (sum(self.myGoalLeftPostDists) /
                                   len(self.myGoalLeftPostDists))
        if len(self.myGoalRightPostDists) > 0:
            self.myRightPostDist = (sum(self.myGoalRightPostDists) /
                                    len(self.myGoalRightPostDists))
        if len(self.oppGoalLeftPostDists) > 0:
            self.oppLeftPostDist = (sum(self.oppGoalLeftPostDists) /
                                    len(self.oppGoalLeftPostDists))
        if len(self.oppGoalRightPostDists) > 0:
            self.oppRightPostDist = (sum(self.oppGoalRightPostDists) /
                                     len(self.oppGoalRightPostDists))


    # Make sure ball is on before doing this
    def ballForeWhichFoot(self):
        ball = self.brain.ball

        if not (constants.MAX_KICK_X > ball.relX > constants.MIN_KICK_X) or \
                not ball.on:
            self.ballForeFoot = constants.INCORRECT_POS

        elif constants.LEFT_FOOT_L_Y > ball.relY >= constants.LEFT_FOOT_R_Y:
            self.ballForeFoot = constants.LEFT_FOOT

        elif constants.LEFT_FOOT_R_Y > ball.relY >= 0:
            self.ballForeFoot = constants.MID_LEFT

        elif 0 > ball.relY > constants.RIGHT_FOOT_L_Y:
            self.ballForeFoot = constants.MID_RIGHT

        elif constants.RIGHT_FOOT_L_Y > ball.relY > constants.RIGHT_FOOT_R_Y:
            self.ballForeFoot = constants.RIGHT_FOOT

        else:
            print "ball in incorrect pos, ball at %.2f, %.2f" % (ball.relX,
                                                                 ball.relY)
            self.ballForeFoot = constants.INCORRECT_POS

    def __str__(self):
        s = ""
        if self.myLeftPostBearing is not None:
            s += ("My left post bearing is: " + str(self.myLeftPostBearing) +
                  " dist is: " + str(self.myLeftPostDist) + "\n")
        if self.myRightPostBearing is not None:
            s += ("My right post bearing is: " + str(self.myRightPostBearing) +
                  " dist is: " + str(self.myRightPostDist) +  "\n")
        if self.oppLeftPostBearing is not None:
            s += ("Opp left post bearing is: " + str(self.oppLeftPostBearing) +
                  " dist is: " + str(self.oppLeftPostDist) + "\n")
        if self.oppRightPostBearing is not None:
            s += ("Opp right post bearing is: " + str(self.oppRightPostBearing)
                  + " dist is: " + str(self.oppRightPostDist) +  "\n")
        if s == "":
            s = "No goal posts observed"
        return s

    def getShotCloseAimPoint(self):
        return (NogginConstants.FIELD_WIDTH,
                NogginConstants.MIDFIELD_Y)

    def getShotFarAimPoint(self):
        if self.brain.my.y < NogginConstants.MIDFIELD_Y:
            return constants.SHOOT_AT_LEFT_AIM_POINT
        else :
            return constants.SHOOT_AT_RIGHT_AIM_POINT

    def updateKickObjective(self):
        """
        Figure out what to do with the ball
        """
        avgOppGoalDist = 0.0

        my = self.brain.my

        if not self.hasKickedOffKick:
            self.kickObjective = constants.OBJECTIVE_KICKOFF
            self.hasKickedOffKick = True
            self.bigKick = False


        if my.x < NogginConstants.FIELD_WIDTH / 2:
            self.kickObjective = constants.OBJECTIVE_CLEAR

        elif my.dist(Location(NogginConstants.OPP_GOALBOX_RIGHT_X,
                              NogginConstants.OPP_GOALBOX_MIDDLE_Y)) > \
                              NogginConstants.FIELD_WIDTH / 3:
            self.kickObjective = constants.OBJECTIVE_CENTER

        elif my.x > NogginConstants.FIELD_WIDTH * 3/4 and \
                NogginConstants.FIELD_HEIGHT/4. < my.y < \
                NogginConstants.FIELD_HEIGHT * 3./4.:
            self.kickObjective = constants.OBJECTIVE_SHOOT_CLOSE

        else :
            self.kickObjective = constants.OBJECTIVE_SHOOT_FAR

    def getKick(self):
        if self.kickObjective == constants.OBJECTIVE_KICKOFF:
            getClearBallKick(self)


    def getClearBallKick(self):
        """
        
        """
        if self.oppLeftPostBearing is not None and \
                self.oppRightPostBearing is not None:

            avgOppBearing = (self.oppLeftPostBearing + self.oppRightPostBearing)/2
            if fabs(avgOppBearing) < constants.ALIGN_FOR_KICK_BEARING_THRESH:
                if constants.DEBUG_KICKS: print ("\t\t Straight 1")
                self.bigKick = True
                getStraightKick(self)

            elif avgOppBearing > constants.ALIGN_FOR_KICK_BEARING_THRESH:
                if constants.DEBUG_KICKS: print ("\t\t Left 5")
                getLeftKick(self)

            elif avgOppBearing < -constants.ALIGN_FOR_KICK_BEARING_THRESH:
                if constants.DEBUG_KICKS: print ("\t\t Right 5")
                getRightKick(self)

        elif self.sawOwnGoal:
            if self.myLeftPostBearing is not None and self.myRightPostBearing is not None:
                # Goal in front
                avgMyGoalBearing = (self.myRightPostBearing + self.myLeftPostBearing)/2

                if avgMyGoalBearing > 0:
                    if constants.DEBUG_KICKS: print ("\t\tright 1")
                    getRightKick(self)
                else :
                    if constants.DEBUG_KICKS: print ("\t\tleft 1")
                    getLeftKick(self)

            else :
                postBearing = 0.0
                if self.myLeftPostBearing is not None:
                    postBearing = self.myLeftPostBearing
                else :
                    postBearing = self.myRightPostBearing
                if postBearing > 0:
                    getRightKick(self)
                else :
                    getLeftKick(self)

        else:
            # use localization for kick
            my = player.brain.my

            if my.inCenterOfField():
                if abs(my.h) <= constants.CLEAR_CENTER_FIELD_STRAIGHT_ANGLE:
                    if constants.DEBUG_KICKS: print ("\t\tcenter1")
                    self.bigKick = True
                    getStraightKick(self)

                elif my.h < -constants.CLEAR_CENTER_FIELD_STRAIGHT_ANGLE:
                    if constants.DEBUG_KICKS: print ("\t\tcenter2")
                    getLeftKick(self)

                elif my.h > constants.CLEAR_CENTER_FIELD_STRAIGHT_ANGLE:
                    if constants.DEBUG_KICKS: print ("\t\tcenter3")
                    getRightKick(self)

            elif my.inTopOfField():
                if constants.FACING_SIDELINE_ANGLE < my.h:
                    if constants.DEBUG_KICKS: print ("\t\ttop1")
                    getRightKick(self)

                elif my.h < -90:
                    if constants.DEBUG_KICKS: print ("\t\ttop3")
                    getLeftKick(self)

                else :
                    if constants.DEBUG_KICKS: print ("\t\ttop4")
                    self.bigKick = True
                    getStraightKick(self)

            elif my.inBottomOfField():
                if -constants.FACING_SIDELINE_ANGLE > my.h:
                    if constants.DEBUG_KICKS: print ("\t\tbottom1")
                    getLeftKick(self)

                elif my.h > 90:
                    if constants.DEBUG_KICKS: print ("\t\tbottom3")
                    getRightKick(self)

                else :
                    if constants.DEBUG_KICKS: print ("\t\tbottom4")
                    self.bigKick = True
                    getStraightKick(self)

        self.bigKick = False
        getStraightKick(self)

def getShotKick(self):
    """
    Put it in the hole!
    """
    my = self.brain.my

    if self.oppLeftPostBearing is not None and \
            self.oppRightPostBearing is not None:

        if (self.oppRightPostBearing < -constants.KICK_STRAIGHT_POST_BEARING and
            self.oppLeftPostBearing > constants.KICK_STRAIGHT_POST_BEARING):
            player.bigKick = True
            getStraightKick(self)

        avgOppBearing = (self.oppLeftPostBearing + self.oppRightPostBearing)/2
        if fabs(avgOppBearing) < constants.KICK_STRAIGHT_BEARING_THRESH:
            if constants.DEBUG_KICKS: print ("\t\t Straight 1")
            player.bigKick = True
            getStraightKick(self)

        elif fabs(avgOppBearing) < constants.ALIGN_FOR_KICK_BEARING_THRESH and \
                not player.hasAlignedOnce:
            if constants.DEBUG_KICKS: print ("\t\t Align 1")
            player.angleToAlign = avgOppBearing
            player.bigKick = True
            ## getStraightKick(self)
            return player.goLater('alignOnBallStraightKick')

        elif avgOppBearing > constants.ALIGN_FOR_KICK_BEARING_THRESH:
            if constants.DEBUG_KICKS: print ("\t\t Left 5")
            getLeftKick(self)

        elif avgOppBearing < -constants.ALIGN_FOR_KICK_BEARING_THRESH:
            if constants.DEBUG_KICKS: print ("\t\t Right 5")
            getRightKick(self)

    elif self.myLeftPostBearing is not None and self.myRightPostBearing is not None:

        avgMyGoalBearing = (self.myRightPostBearing + self.myLeftPostBearing)/2
        if my.inCenterOfField():
            if constants.DEBUG_KICKS: print ("\t\tcenterfieldkick")
            if avgMyGoalBearing > 0:
                getRightKick(self)
            else :
                getLeftKick(self)

        elif my.inTopOfField():
            if constants.DEBUG_KICKS: print ("\t\ttopfieldkick")
            if 90 > avgMyGoalBearing > -30:
                getRightKick(self)
            elif avgMyGoalBearing < -30:
                getLeftKick(self)
            else :
                getStraightKick(self)

        elif my.inBottomOfField():
            if constants.DEBUG_KICKS: print ("\t\tbottomfieldkick")
            if -90 < avgMyGoalBearing < 30:
                getRightKick(self)

            elif avgMyGoalBearing > 30:
                getLeftKick(self)

            else :
                getStraightKick(self)

    # if somehow we didn't return already with our kick choice,
    # use localization for kick
    if self.kickObjective == constants.OBJECTIVE_SHOOT_CLOSE:
        return player.goNow('shootBallClose')
    else :
        return player.goNow('shootBallFar')

def getCloseShot(self):
        """
    Slam-dunk!
    """
    my = player.brain.my
    shotAimPoint = getShotCloseAimPoint(self)
    leftPostBearing = my.getRelativeBearing(self.brain.oppGoalLeftPost)
    rightPostBearing = my.getRelativeBearing(self.brain.oppGoalRightPost)

    # Am I looking between the posts?
    if (rightPostBearing < -constants.KICK_STRAIGHT_POST_BEARING and
        leftPostBearing > constants.KICK_STRAIGHT_POST_BEARING):
        getStraightKick(self)

    leftShotPointBearing = my.getRelativeBearing(constants.SHOOT_AT_LEFT_AIM_POINT)

    rightShotPointBearing = my.getRelativeBearing(constants.SHOOT_AT_RIGHT_AIM_POINT)

    # Turn to the closer shot point
    if fabs(rightShotPointBearing) < fabs(leftShotPointBearing):
        angleToAlign = rightShotPointBearing
    else :
        angleToAlign = leftShotPointBearing

    if constants.SHOOT_BALL_SIDE_KICK_ANGLE > abs(angleToAlign) > \
            constants.SHOOT_BALL_LOC_ALIGN_ANGLE and \
            not player.hasAlignedOnce:
        player.angleToAlign = angleToAlign
        self.bigKick = False
        return player.goNow('alignOnBallStraightKick')
    elif angleToAlign > constants.SHOOT_BALL_SIDE_KICK_ANGLE:
        getLeftKick(self)

    elif angleToAlign < -constants.SHOOT_BALL_SIDE_KICK_ANGLE:
        getRightKick(self)

    else :
        player.bigKick = False
        getStraightKick(self)


def getStraightKick(self):

    if self.ballForeFoot == constants.LEFT_FOOT:
        if self.bigKick:
            self.chosenKick = SweetMoves.LEFT_BIG_KICK
        else :
            self.chosenKick = SweetMoves.LEFT_FAR_KICK

    elif self.ballForeFoot == constants.RIGHT_FOOT:
        if self.bigKick:
            self.chosenKick = SweetMoves.RIGHT_BIG_KICK
        else :
            self.chosenKick = SweetMoves.RIGHT_FAR_KICK

    elif self.ballForeFoot == constants.MID_RIGHT:
        if self.bigKick:
            self.chosenKick = SweetMoves.RIGHT_BIG_KICK
        else :
            self.chosenKick = SweetMoves.RIGHT_FAR_KICK

    elif self.ballForeFoot == constants.MID_LEFT:
        if self.bigKick:
            self.chosenKick = SweetMoves.LEFT_BIG_KICK
        else :
            self.chosenKick = SweetMoves.LEFT_FAR_KICK

    else :                  # INCORRECT_POS
        return self.goLater('positionForKick')

def getLeftKick(player):
    """
    Kick the ball to the left, with right foot
    """

    player.chosenKick = SweetMoves.RIGHT_SIDE_KICK

def getRightKick(player):
    """
    Kick the ball to the right, using the left foot
    """
    player.chosenKick = SweetMoves.LEFT_SIDE_KICK

def getRightShortKick(player):
    player.chosenKick = SweetMoves.SHORT_LEFT_SIDE_KICK

def getLeftShortKick(player):
    player.chosenKick = SweetMoves.SHORT_RIGHT_SIDE_KICK
