
def getApproachPosition(nav):
    ball = nav.brain.ball
    my = nav.brain.my

    if nav.penaltyKicking:
        destKickLoc = nav.getPenaltyKickingBallDest()
        ballLoc = RobotLocation(ball.x, ball.y, NogginConstants.OPP_GOAL_HEADING)
        destH = MyMath.getRelativeBearing(destKickLoc)

    elif nav.shouldMoveAroundBall():
        return nav.getPointToMoveAroundBall()
    elif nav.inFrontOfBall():
        destH = nav.getApproachHeadingFromFront()
    else :
        destH = nav.getApproachHeadingFromBehind()

    destX = ball.x - ChaseConstants.APPROACH_DIST_TO_BALL * \
        cos(radians(destH))
    destY = ball.y - ChaseConstants.APPROACH_DIST_TO_BALL * \
        sin(radians(destH))
    return RobotLocation(destX, destY, destH)

def getApproachHeadingFromBehind(nav):
    ball = nav.brain.ball
    aimPoint = KickingHelpers.getShotFarAimPoint(nav)
    ballLoc = RobotLocation(ball.x, ball.y, NogginConstants.OPP_GOAL_HEADING)
    ballBearingToGoal = ballLoc.getRelativeBearing(aimPoint)
    return ballBearingToGoal

def getPenaltyKickingBallDest(nav):
    if not nav.penaltyMadeFirstKick:
        return (NogginConstants.FIELD_WIDTH * 3/4,
                NogginConstants.FIELD_HEIGHT /4)

    return Location(NogginConstants.OPP_GOAL_MIDPOINT[0],
                    NogginConstants.OPP_GOAL_MIDPOINT[1] )


def getNextOrbitPos(self):
    relX = -ChaseConstants.ORBIT_OFFSET_DIST * \
        cos(radians(ChaseConstants.ORBIT_STEP_ANGLE)) + self.brain.ball.relX
    relY =  -ChaseConstants.ORBIT_OFFSET_DIST * \
        sin(radians(ChaseConstants.ORBIT_STEP_ANGLE)) + self.brain.ball.relY
    relTheta = ChaseConstants.ORBIT_STEP_ANGLE * 2 + self.brain.ball.bearing
    return RobotLocation(relX, relY, relTheta)

def shouldMoveAroundBall(self):
    return (self.brain.ball.x < self.brain.my.x
            and (self.brain.my.x - self.brain.ball.x) <
            75.0 )

def getPointToMoveAroundBall(self):
    ball = self.brain.ball
    x = ball.x

    if ball.y > self.brain.my.y:
        y = self.brain.ball.y - 75.0
        destH = 90.0
    else:
        y = self.brain.ball.y + 75.0
        destH = -90.0

    return RobotLocation(x, y, destH)

def getBallApproachParam(ball):
    # Determine our speed for approaching the ball

    if ball.dist < constants.APPROACH_WITH_GAIN_DIST:
        sX = MyMath.clip(ball.dist*constants.APPROACH_X_GAIN,
                         constants.MIN_APPROACH_X_SPEED,
                         constants.MAX_APPROACH_X_SPEED)
    else :
        sX = constants.MAX_APPROACH_X_SPEED

    # Determine the speed to turn to the ball
    sTheta = MyMath.clip(ball.bearing*constants.APPROACH_SPIN_GAIN,
                         -constants.APPROACH_SPIN_SPEED,
                         constants.APPROACH_SPIN_SPEED)
    # Avoid spinning so slowly that we step in place
    if fabs(sTheta) < constants.MIN_APPROACH_SPIN_MAGNITUDE:
        sTheta = 0.0

    # Set our walk towards the ball
    if ball.on:
        return (sX, 0, sTheta)

    else:
        return (0, 0, 0)
