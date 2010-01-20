
from man.motion import SweetMoves as SweetMoves
from man.motion import HeadMoves as HeadMoves
from .util import cofsa as fsa

"""
Fall Protection and Recovery States
"""
@fsa.state
def fallen(guard):
    """
    Activates when robot has fallen. Deactivates player
    and puts standup in motion
    """
    guard.brain.roboguardian.enableFallProtection(False)
    guard.brain.tracker.stopHeadMoves()
    guard.brain.motion.resetWalk()
    guard.brain.motion.resetScripted()
    guard.brain.motion.stopHeadMoves()
    guard.brain.player.gainsOn()
    yield
    #everything above was in a 'if firstFrame():', we automatically make the first call to get to here on creation, right?
    # Put player into safe mode
    while True:
        guard.brain.player.switchTo('fallen')
        yield guard.goLater('standup')

@fsa.state
def falling(guard):
    """
    Protect the robot when it is falling.
    """
    guard.brain.tracker.stopHeadMoves()
    yield guard.goLater('notFallen')

@fsa.state
def standup(guard):
    """
    Performs the appropriate standup routine
    """
    inertial = guard.brain.sensors.inertial
    #guard.printf("standup angleY is "+str(inertial.angleY))

    guard.brain.tracker.stopHeadMoves()
    guard.brain.tracker.setNeutralHead()
    yield

    while True:
        # If on back, perform back stand up
        if ( inertial.angleY < -guard.FALLEN_THRESH ):
            yield guard.goLater('standFromBack')

            # If on stomach, perform stand up from front
        elif ( inertial.angleY > guard.FALLEN_THRESH ):
            yield guard.goLater('standFromFront')

        yield guard.stay()

@fsa.state
def standFromBack(guard):
    guard.brain.player.executeMove(SweetMoves.STAND_UP_BACK)
    guard.standupMoveTime = SweetMoves.getMoveTime(SweetMoves.STAND_UP_BACK)
    yield

    while True:
        yield guard.goLater('standing')

@fsa.state
def standFromFront(guard):
    guard.brain.player.executeMove(SweetMoves.STAND_UP_FRONT)
    guard.standupMoveTime = SweetMoves.getMoveTime(SweetMoves.STAND_UP_FRONT)
    yield

    while True:
        yield guard.goLater('standing')

@fsa.state
def standing(guard):
    while guard.stateTime <= guard.standupMoveTime:
        yield guard.stay()

    yield guard.goLater('doneStanding')

@fsa.state
def doneStanding(guard):
    """
    Does clean up after standing up.
    """
    guard.brain.player.gainsOn()
    guard.brain.player.stopWalking()
    yield

    while True:
        guard.brain.player.switchTo(guard.brain.gameController.currentState)
        yield guard.goLater('notFallen')

@fsa.state
def notFallen(guard):
    guard.standingUp = False
    guard.brain.roboguardian.enableFallProtection(True)
    yield
    """
    Does nothing
    """
    while True:
        yield guard.stay()


