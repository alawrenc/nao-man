import man.motion.SweetMoves as SweetMoves
import GoalieTransitions as helper

CENTER_SAVE_THRESH = 15

def goalieSave(player):
    brain = player.brain
    if player.firstFrame():
        player.saving = True
        player.isChasing = False
        brain.motion.stopHeadMoves()
        brain.nav.switchTo('stop')
        brain.tracker.trackBall()
    if not brain.nav.isStopped():
        return player.stay()
    ball = brain.ball

    # Figure out where the ball is going and when it will be there
    if ball.on:
        relY = ball.relY
    else:
        relY = ball.locRelY
    # Decide the type of save
    if relY > CENTER_SAVE_THRESH:
        print "Should be saving left"
        return player.goNow('saveLeft')
    elif relY < -CENTER_SAVE_THRESH:
        print "Should be saving right"
        return player.goNow('saveRight')
    else:
        print "Should be saving center"
        return player.goNow('saveCenter')

def saveRight(player):
    if player.firstFrame():
        player.executeMove(SweetMoves.SAVE_RIGHT_DEBUG)
    if player.stateTime >= SweetMoves.getMoveTime(SweetMoves.SAVE_RIGHT_DEBUG):
        return player.goLater('holdRightSave')
    return player.stay()

def saveLeft(player):
    if player.firstFrame():
        player.executeMove(SweetMoves.SAVE_LEFT_DEBUG)
    if player.stateTime >= SweetMoves.getMoveTime(SweetMoves.SAVE_LEFT_DEBUG):
        return player.goLater('holdLeftSave')
    return player.stay()

def saveCenter(player):
    if player.firstFrame():
        player.executeMove(SweetMoves.SAVE_CENTER_DEBUG)
    if player.stateTime >= SweetMoves.getMoveTime(SweetMoves.SAVE_CENTER_DEBUG):
        return player.goLater('holdCenterSave')
    return player.stay()

def holdRightSave(player):
    if helper.shouldHoldSave(player):
        player.executeMove(SweetMoves.SAVE_RIGHT_HOLD_DEBUG)
    else:
        return player.goLater('postSave')
    return player.stay()

def holdLeftSave(player):
    if helper.shouldHoldSave(player):
        player.executeMove(SweetMoves.SAVE_LEFT_HOLD_DEBUG)
    else:
        return player.goLater('postSave')
    return player.stay()

def holdCenterSave(player):
    if helper.shouldHoldSave(player):
        player.executeMove(SweetMoves.SAVE_CENTER_HOLD_DEBUG)
    else:
        return player.goLater('postSave')
    return player.stay()

def postSave(player):
    player.standup()
    #if player.brain.ball.on:
    player.brain.tracker.trackTarget(player.brain.ball)
    #else: do not yet created postSaveScan
    roleState = player.getRoleState(player.currentRole)
    player.saving = False
    return player.goLater(roleState)
