from .. import NogginConstants
from . import RoleConstants
from . import SubRolesConstants
from . import PositionConstants
from . import SubRoles

def rChaser(team, workingPlay):
    workingPlay.setRole(RoleConstants.CHASER)
    workingPlay.setSubRole(SubRolesConstants.CHASE_NORMAL)
    pos = (team.brain.my.x,team.brain.my.y)
    workingPlay.setPosition(pos)

def rSearcher(team, workingPlay):
    '''
    Determines positioning for robots while using the finder formation
    '''
    workingPlay.setRole(RoleConstants.SEARCHER)
    if team.numActiveFieldPlayers == 1:
        workingPlay.setSubRole(SubRolesConstants.OTHER_FINDER)
        workingPlay.setPosition((PositionConstants.SWEEPER_X,
                                 PositionConstants.SWEEPER_Y))
    else:
        teammate = team.getOtherActiveTeammate()
        pos = team.getLeastWeightPosition(
            PositionConstants.TWO_DOG_FINDER_POSITIONS,
            teammate)
        if pos == PositionConstants.TWO_DOG_FINDER_POSITIONS[0]:
            workingPlay.setSubRole(SubRolesConstants.FRONT_FINDER)
        else:
            workingPlay.setSubRole(SubRolesConstants.OTHER_FINDER)
        workingPlay.setPosition(pos[:2])

def rDefender(team, workingPlay):
    '''gets positioning for defender'''
    workingPlay.setRole(RoleConstants.DEFENDER)
    # If the ball is deep in our side, we become a sweeper
    if team.brain.ball.x < PositionConstants.SWEEPER_X:
        SubRoles.pSweeper(team, workingPlay)

    elif team.brain.ball.x > NogginConstants.MIDFIELD_X:
        if team.brain.ball.y < NogginConstants.MIDFIELD_Y:
            SubRoles.pBottomStopper(team, workingPlay)
        else:
            SubRoles.pTopStopper(team, workingPlay)

    elif team.brain.ball.y < NogginConstants.MIDFIELD_Y:
        SubRoles.pTopStopper(team, workingPlay)
    else:
        SubRoles.pBottomStopper(team, workingPlay)

def rOffender(team, workingPlay):
    """
    The offensive attacker!
    """
    workingPlay.setRole(RoleConstants.OFFENDER)
    # RIGHT_WING  if ball is in opp half but not in a corner
    if ((team.brain.ball.x > NogginConstants.CENTER_FIELD_X) and
        (team.brain.ball.y < NogginConstants.CENTER_FIELD_Y)):
        SubRoles.pRightWing(team, workingPlay)
    # LEFT_WING otherwise
    else:
        SubRoles.pLeftWing(team, workingPlay)

def rGoalie(team, workingPlay):
    """
    The Goalie
    """
    workingPlay.setRole(RoleConstants.GOALIE)
    if (team.brain.gameController.currentState == 'gameReady' or
        team.brain.gameController.currentState =='gameSet'):
        SubRoles.pGoalieReady(team, workingPlay)
    if team.goalieShouldChase():
        SubRoles.pGoalieChaser(team, workingPlay)
    else:
        SubRoles.pGoalieNormal(team, workingPlay)

def rMiddie(team, workingPlay):

    workingPlay.setRole(RoleConstants.MIDDIE)
    SubRoles.pDefensiveMiddie(team, workingPlay)

def rDefenderDubD(team, workingPlay):

    workingPlay.setRole(RoleConstants.DEFENDER_DUB_D)
     # Figure out who isn't penalized with you
    other_teammate = team.getOtherActiveTeammate()

    leftPos = PositionConstants.LEFT_DEEP_BACK_POS
    rightPos = PositionConstants.RIGHT_DEEP_BACK_POS
    # Figure out who should go to which position
    pos = team.getLeastWeightPosition((leftPos,rightPos), other_teammate)

    if pos == leftPos:
        SubRoles.pLeftDeepBack(team, workingPlay)
    else: #if pos == rightPos
        SubRoles.pRightDeepBack(team, workingPlay)
