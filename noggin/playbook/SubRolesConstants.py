
USE_FANCY_GOALIE = True

# dictionary of subRoles
NUM_SUB_ROLES = 26
SUB_ROLES = dict(zip(range(NUM_SUB_ROLES), ("INIT_SUB_ROLE",
                                            "PENALTY_SUB_ROLE",
                                            #OFFENDER SUB ROLES 2-4
                                            "LEFT_WING",
                                            "RIGHT_WING",
                                            "DUBD_OFFENDER",

                                            # MIDDIE SUB ROLES 5-6
                                            "DEFENSIVE_MIDDIE",
                                            "OFFENSIVE_MIDDIE",

                                            # DEFENDER SUB ROLES 7-12
                                            "STOPPER",
                                            "BOTTOM_STOPPER",
                                            "TOP_STOPPER",
                                            "SWEEPER",
                                            "LEFT_DEEP_BACK",
                                            "RIGHT_DEEP_BACK",

                                            # CHASER SUB ROLES 13
                                            "CHASE_NORMAL",

                                            # GOALIE SUB ROLE 14-15
                                            "GOALIE_NORMAL",
                                            "GOALIE_CHASER",

                                            # FINDER SUB ROLES 16-19
                                            "FRONT_FINDER",
                                            "LEFT_FINDER",
                                            "RIGHT_FINDER",
                                            "OTHER_FINDER",

                                            # KICKOFF SUB ROLES 20-21
                                            "KICKOFF_SWEEPER",
                                            "KICKOFF_STRIKER",

                                            # READY SUB ROLES 22-25
                                            "READY_GOALIE",
                                            "READY_CHASER",
                                            "READY_DEFENDER",
                                            "READY_OFFENDER" )))
# tuple of subRoles
(INIT_SUB_ROLE,
 PENALTY_SUB_ROLE,

 LEFT_WING,
 RIGHT_WING,
 DUBD_OFFENDER,

 DEFENSIVE_MIDDIE,
 OFFENSIVE_MIDDIE,

 STOPPER,
 BOTTOM_STOPPER,
 TOP_STOPPER,
 SWEEPER,
 LEFT_DEEP_BACK,
 RIGHT_DEEP_BACK,

 CHASE_NORMAL,

 GOALIE_NORMAL,
 GOALIE_CHASER,

 FRONT_FINDER,
 LEFT_FINDER,
 RIGHT_FINDER,
 OTHER_FINDER,

 KICKOFF_SWEEPER,
 KICKOFF_STRIKER,

 READY_GOALIE,
 READY_CHASER,
 READY_DEFENDER,
 READY_OFFENDER
 ) = range(NUM_SUB_ROLES)
