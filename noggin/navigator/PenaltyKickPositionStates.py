from man.noggin.navigator import NavHelper as helper

def penaltyBallInOppGoalbox(nav):
    if nav.firstFrame():
        helper.setSpeed(nav, 0, 0, 0)

    if not nav.brain.ball.inOppGoalBox():
        return nav.goLater('chase')

    return nav.stay()
