from .. import NogginConstants

USE_DUB_D = False
# Length of time to spend in the kickoff play
KICKOFF_FORMATION_TIME = 3
# Time limit for moving into the finder routine
FINDER_TIME_THRESH = 5
S_MIDDIE_DEFENDER_THRESH = NogginConstants.CENTER_FIELD_X * 1.5
USE_FINDER = False
NUM_STRATEGIES = 13

STRATEGIES = dict(zip(range(NUM_STRATEGIES), ("INIT_STRATEGY",
                                              "PENALTY_STRATEGY",
                                             "READY_STRATEGY",

                                             # field player number strategies
                                             "NO_FIELD_PLAYERS",
                                             "ONE_FIELD_PLAYER",
                                             "TWO_FIELD_PLAYERS",
                                             "THREE_FIELD_PLAYERS",

                                             # More 2 field player strats
                                             "TWO_PLAYER_ZONE",
                                             "sWIN",

                                             # Test strategies
                                             "TEST_DEFENDER",
                                             "TEST_OFFENDER",
                                             "TEST_MIDDIE",
                                             "TEST_CHASER"
                                             )))
(INIT_STRATEGY,
 PENALTY_STRATEGY,
 S_READY,
 S_NO_FIELD_PLAYERS,
 S_ONE_FIELD_PLAYER,
 S_TWO_FIELD_PLAYERS,
 S_THREE_FIELD_PLAYERS,

 S_TWO_ZONE,
 S_WIN,

 S_TEST_DEFENDER,
 S_TEST_OFFENDER,
 S_TESET_MIDDIE,
 S_TEST_CHASER) = range(NUM_STRATEGIES)
