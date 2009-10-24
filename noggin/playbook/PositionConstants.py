from .. import NogginConstants
from math import pi

## POSITION CONSTANTS ##

# Dub_d
DEEP_BACK_X = SWEEPER_X
LEFT_DEEP_BACK_Y = NogginConstants.MY_GOALBOX_BOTTOM_Y - 40.
RIGHT_DEEP_BACK_Y = NogginConstants.MY_GOALBOX_TOP_Y + 40.
LEFT_DEEP_BACK_POS =  (DEEP_BACK_X, LEFT_DEEP_BACK_Y)
RIGHT_DEEP_BACK_POS = (DEEP_BACK_X, RIGHT_DEEP_BACK_Y)

# Finder
TWO_DOG_FINDER_POSITIONS = (
    (NogginConstants.FIELD_WIDTH * 1./2.,
     NogginConstants.CENTER_FIELD_Y),
    (NogginConstants.FIELD_WIDTH * 1./3.,
     NogginConstants.CENTER_FIELD_Y))

# READY/SET Positions - our kickoff
READY_KICKOFF_DEFENDER_X = NogginConstants.CENTER_FIELD_X * 0.5
READY_KICKOFF_DEFENDER_CENTER_OFFSET = NogginConstants.FIELD_WHITE_HEIGHT/10.

READY_KICKOFF_DEFENDER_0_POS = [READY_KICKOFF_DEFENDER_X,
                                NogginConstants.CENTER_FIELD_Y -
                                READY_KICKOFF_DEFENDER_CENTER_OFFSET] # left

READY_KICKOFF_DEFENDER_1_POS = [READY_KICKOFF_DEFENDER_X,
                                NogginConstants.CENTER_FIELD_Y +
                                READY_KICKOFF_DEFENDER_CENTER_OFFSET] # right

READY_KICKOFF_OFFENDER_X = READY_KICKOFF_DEFENDER_X #keeps positions level
READY_KICKOFF_OFFENDER_CENTER_OFFSET = READY_KICKOFF_DEFENDER_CENTER_OFFSET

READY_KICKOFF_OFFENDER_0_POS = [READY_KICKOFF_OFFENDER_X,
                                NogginConstants.CENTER_FIELD_Y +
                                READY_KICKOFF_OFFENDER_CENTER_OFFSET] # right

READY_KICKOFF_OFFENDER_1_POS = [READY_KICKOFF_OFFENDER_X,
                                NogginConstants.CENTER_FIELD_Y -
                                READY_KICKOFF_OFFENDER_CENTER_OFFSET] # left

READY_KICKOFF_CHASER_POS = [NogginConstants.CENTER_FIELD_X -
                        NogginConstants.CENTER_CIRCLE_RADIUS/2.0,
                        NogginConstants.CENTER_FIELD_Y] # near center

# Ready/Set positions- not our kickoff

READY_NON_KICKOFF_MAX_X = (NogginConstants.GREEN_PAD_X +
                                NogginConstants.FIELD_GREEN_WIDTH * 1./4.)

READY_NON_KICKOFF_DEFENDER_POS = [READY_NON_KICKOFF_MAX_X,
                              NogginConstants.GREEN_PAD_Y +
                              NogginConstants.FIELD_GREEN_HEIGHT * 1./5.]

READY_NON_KICKOFF_CHASER_POS = [READY_NON_KICKOFF_MAX_X,
                            NogginConstants.CENTER_FIELD_Y]

READY_NON_KICKOFF_OFFENDER_POS = [READY_NON_KICKOFF_MAX_X,
                              NogginConstants.GREEN_PAD_Y +
                              NogginConstants.FIELD_WHITE_WIDTH * 3./5.]

#TODO: reconsider where players should move after kickoff
# KICK OFF POSITIONS (right after kickoff, rather)
KICKOFF_OFFENDER_0_POS = [NogginConstants.CENTER_FIELD_X * 1./2.,
                      NogginConstants.FIELD_HEIGHT * 1./4.]

KICKOFF_OFFENDER_1_POS = [NogginConstants.CENTER_FIELD_X * 1./2.,
                      NogginConstants.FIELD_HEIGHT * 3./4.]

KICKOFF_DEFENDER_0_POS = [NogginConstants.CENTER_FIELD_X * 1./2.,
                      NogginConstants.FIELD_HEIGHT * 1./4.]

KICKOFF_DEFENDER_1_POS = [NogginConstants.CENTER_FIELD_X * 1./2.,
                      NogginConstants.FIELD_HEIGHT * 3./4.]
# Defender
DEFENDER_BALL_DIST = 100
SWEEPER_X = NogginConstants.MY_GOALBOX_RIGHT_X + 50.
SWEEPER_Y = NogginConstants.CENTER_FIELD_Y
STOPPER_MAX_X = NogginConstants.CENTER_FIELD_X - 75.
STOPPER_X = NogginConstants.CENTER_FIELD_X - 150.
TOP_STOPPER_Y = NogginConstants.CENTER_FIELD_Y + 75.
BOTTOM_STOPPER_Y = NogginConstants.CENTER_FIELD_Y - 75.

# Middie Positions
MIDDIE_X_OFFSET = 50.0
MIDDIE_Y_OFFSET = 75.0
MIN_MIDDIE_Y = NogginConstants.FIELD_WHITE_BOTTOM_SIDELINE_Y + MIDDIE_Y_OFFSET
MAX_MIDDIE_Y = NogginConstants.FIELD_WHITE_TOP_SIDELINE_Y - MIDDIE_Y_OFFSET
DEFENSIVE_MIDDIE_X = NogginConstants.CENTER_FIELD_X - MIDDIE_X_OFFSET
OFFENSIVE_MIDDIE_X = NogginConstants.CENTER_FIELD_X + MIDDIE_X_OFFSET

# Offender
WING_X_OFFSET = 100.
WING_Y_OFFSET = 100.
WING_MIN_X = NogginConstants.CENTER_FIELD_X
WING_MAX_X = NogginConstants.OPP_GOALBOX_LEFT_X
LEFT_WING_MIN_Y = NogginConstants.GREEN_PAD_Y
LEFT_WING_MAX_Y = NogginConstants.CENTER_FIELD_Y
RIGHT_WING_MIN_Y = NogginConstants.CENTER_FIELD_Y
RIGHT_WING_MAX_Y = (NogginConstants.FIELD_WIDTH - NogginConstants.GREEN_PAD_Y)

#GOALIE
BALL_LOC_LIMIT = 220 # Dist at which we stop active localization and just track
# elliptical positioning
GOAL_CENTER_X = NogginConstants.FIELD_WHITE_LEFT_SIDELINE_X
GOAL_CENTER_Y = NogginConstants.CENTER_FIELD_Y
ELLIPSE_X_SHIFT = 5. # Increase this to account for the goalposts
LARGE_ELLIPSE_HEIGHT = NogginConstants.GOALBOX_DEPTH * 0.65 #radius
LARGE_ELLIPSE_WIDTH = NogginConstants.CROSSBAR_CM_WIDTH / 2.0 #radius
LARGE_ELLIPSE_CENTER_Y = NogginConstants.CENTER_FIELD_Y
LARGE_ELLIPSE_CENTER_X = NogginConstants.FIELD_WHITE_LEFT_SIDELINE_X
GOALIE_HOME_X = NogginConstants.MY_GOALBOX_LEFT_X + LARGE_ELLIPSE_HEIGHT
GOALIE_HOME_Y = NogginConstants.CENTER_FIELD_Y
ELLIPSE_POSITION_LIMIT = BALL_LOC_LIMIT
# Angle limits for moving about ellipse
ELLIPSE_ANGLE_MAX = 80
ELLIPSE_ANGLE_MIN = -80.0
RAD_TO_DEG = 180. / pi
DEG_TO_RAD = pi / 180.
BALL_FOCUS_UNCERT_THRESH = 100.
