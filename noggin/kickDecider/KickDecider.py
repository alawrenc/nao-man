from ..players import KickingConstants as constants
from .. import NogginConstants
from ..typeDefs.Location import Location

class KickDecider:
    """
    Class to hold all the things we need to decide a kick
    """

    def __init__(self, brain):
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

    def getKickObjective(self):
        """
        Figure out what to do with the ball
        """
        avgOppGoalDist = 0.0

        my = self.brain.my

        if not self.hasKickedOffKick:
            return constants.OBJECTIVE_KICKOFF

        if my.x < NogginConstants.FIELD_WIDTH / 2:
            return constants.OBJECTIVE_CLEAR

        elif my.dist(Location(NogginConstants.OPP_GOALBOX_RIGHT_X,
                              NogginConstants.OPP_GOALBOX_MIDDLE_Y)) > \
                              NogginConstants.FIELD_WIDTH / 3:
            return constants.OBJECTIVE_CENTER

        elif my.x > NogginConstants.FIELD_WIDTH * 3/4 and \
                NogginConstants.FIELD_HEIGHT/4. < my.y < \
                NogginConstants.FIELD_HEIGHT * 3./4.:
            return constants.OBJECTIVE_SHOOT_CLOSE

        else :
            return constants.OBJECTIVE_SHOOT_FAR
