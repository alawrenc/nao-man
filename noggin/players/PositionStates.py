from .. import NogginConstants
from . import ChaseBallConstants as ChaseConstants
import man.noggin.playbook.PBConstants as PBConstants
import man.noggin.util.MyMath as MyMath
from man.noggin.typeDefs.Location import RobotLocation, Location
import PositionTransitions as transitions
import PositionConstants as constants

def positionLocalize(player):
    """
    Localize better in order to position
    """
    return player.stay()

def playbookPosition(player):
    """
    Have the robot navigate to the position reported to it from playbook
    """
    brain = player.brain
    nav = brain.nav
    my = brain.my
    ball = brain.ball

    if player.firstFrame():
        if brain.gameController.currentState == 'gameReady':
            brain.tracker.locPans()
        else:
            brain.tracker.activeLoc()

    if ball.on:
        destHeading = my.h + ball.bearing
    elif ball.framesOff < 30:
        destHeading = my.h + ball.locBearing
    else:
        destHeading = NogginConstants.OPP_GOAL_HEADING

    position = player.brain.play.getPosition()
    position = RobotLocation(position[0], position[1], destHeading)

    nav.positionPlaybook(position)

    if brain.my.locScore == NogginConstants.BAD_LOC:
        player.shouldRelocalizeCounter += 1
    else:
        player.shouldRelocalizeCounter = 0
    if player.shouldRelocalizeCounter > constants.SHOULD_RELOC_FRAME_THRESH:
        return player.goLater('relocalize')

    if transitions.shouldAvoidObstacle(player):
        return player.goNow('avoidObstacle')

    # we're at the point, let's switch to another state
    if nav.isStopped() and player.counter > 0:
        return player.goLater('atPosition')

    return player.stay()

def atPosition(player):
    """
    State for when we're at the position
    """
    nav = player.brain.nav
    position = player.brain.play.getPosition()
    position = Location(position[0], position[1])
    if player.firstFrame():
        player.stopWalking()
    ##     player.notAtPositionCounter = 0

    ## if not nav.atHeading(nav.destH) or not nav.atDestinationCloser() or\
    ##         nav.destX != position[0] or nav.destY != position[1]:
    ##     player.notAtPositionCounter += 1
    ## else:
    ##     player.notAtPositionCounter = 0

    if (abs(nav.dest.x - position.x) > constants.GOTO_DEST_EPSILON or
        abs(nav.dest.y - position.y) > constants.GOTO_DEST_EPSILON or
        not player.atDestinationCloser() or
        not player.atHeading()):
        return player.goLater('playbookPosition')

    return player.stay()

def spinToBall(player):
    """
    State to spin to turn to the ball
    """
    if player.firstFrame():
        player.stopWalking()
        player.brain.tracker.trackBall()
    ball = player.brain.ball

    turnRate = MyMath.clip(ball.locBearing*ChaseConstants.BALL_SPIN_GAIN,
                           -ChaseConstants.BALL_SPIN_SPEED,
                           ChaseConstants.BALL_SPIN_SPEED)

    if transitions.atSpinBallDir(player):
        return player.goLater('atSpinBallPosition')

    elif transitions.shouldSpinFindBallPosition(player):
        return player.goLater('spinFindBallPosition')

    elif player.currentSpinDir != MyMath.sign(turnRate):
        player.stopWalking()
        player.currentSpinDir = MyMath.sign(turnRate)
    elif player.stoppedWalk and ball.on and player.brain.nav.isStopped():
        player.setWalk(x=0,y=0,theta=turnRate)

    return player.stay()

def atSpinBallPosition(player):
    """
    Spun to the ball heading, spin again
    """
    if player.firstFrame():
        player.stopWalking()
        player.brain.tracker.activeLoc()

    if transitions.shouldTurnToBall_fromAtBallPosition(player):
        return player.goLater('spinToBall')
    elif transitions.shouldSpinFindBallPosition(player):
        return player.goLater('spinFindBallPosition')

    return player.stay()

def spinFindBallPosition(player):
    """
    Spin to find the ball if it is not being seen.
    """
    if player.brain.nav.isStopped():
        player.stoppedWalk = True

    if player.firstFrame() and player.stoppedWalk:
        player.setWalk(0,
                        0,
                        ChaseConstants.FIND_BALL_SPIN_SPEED)
        player.brain.tracker.trackBall()


    if transitions.shouldTurnToBall_fromAtBallPosition(player):
        return player.goLater('spinToBall')
    if transitions.atSpinBallDir(player):
        return player.goLater('atSpinBallPosition')

    return player.stay()

def relocalize(player):
    if player.firstFrame():
        player.stopWalking()
    if player.brain.my.locScore == NogginConstants.GOOD_LOC or \
            player.brain.my.locScore == NogginConstants.OK_LOC:
        return player.goLater(player.lastDiffState)

    if not player.brain.motion.isHeadActive():
        player.brain.tracker.locPans()

    if player.counter > constants.RELOC_SPIN_FRAME_THRESH:
        player.setWalk(0 , 0, constants.RELOC_SPIN_SPEED)
    return player.stay()
