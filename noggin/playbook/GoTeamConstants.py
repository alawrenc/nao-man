# Test switches to force one role to always be given out
TEST_DEFENDER = False
TEST_OFFENDER = False
TEST_CHASER = False

# Print information as to how the chaser is determined
DEBUG_DET_CHASER = False
DEBUG_DETERMINE_CHASE_TIME = False

PULL_THE_GOALIE = False

SEC_TO_MILLIS = 1000.0
####
#### Role Switching / Tie Breaking ####
####

# penalty is: (ball_dist*heading)/scale
PLAYER_HEADING_PENALTY_SCALE = 300.0 # max 60% of distance
# penalty is: (ball_dist*ball_bearing)/scale
BALL_BEARING_PENALTY_SCALE = 200.0 # max 90% of distance
NO_VISUAL_BALL_PENALTY = 2 # centimeter penalty for not seeing the ball
TEAMMATE_CHASING_PENALTY = 3 # adds standard penalty for teammates (buffer)
TEAMMATE_CHASER_USE_NUMBERS_BUFFER = 20.0 # cm
TEAMMATE_POSITIONING_USE_NUMBERS_BUFFER = 25.0 # cm
# Determine chaser junk
BALL_DIVERGENCE_THRESH = 2000.0
# Special cases for waiting for the ball at half field
CENTER_FIELD_DIST_THRESH = 125.

# role switching constants
CALL_OFF_THRESH = 125.
LISTEN_THRESH = 250.
STOP_CALLING_THRESH = 275.
BEARING_BONUS = 300.
BALL_NOT_SUPER_OFF_BONUS = 300.
BALL_CAPTURE_BONUS = 1000.
KICKOFF_PLAY_BONUS = 1000.
BEARING_SMOOTHNESS = 500.
BALL_ON_BONUS = 1000.

# Velocity bonus constants
VB_MIN_REL_VEL_Y = -100.
VB_MAX_REL_VEL_Y = -20.
VB_MAX_REL_Y = 200.
VB_X_THRESH = 30.
VELOCITY_BONUS = 250.

CHASE_SPEED = 7.00
CHASE_SPIN = 20.00
SUPPORT_SPEED = CHASE_SPEED
SUPPORT_SPIN = CHASE_SPIN
