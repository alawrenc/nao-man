from . import TrackingConstants as constants
import man.motion.HeadMoves as HeadMoves

TIME_TO_LOOK_TO_TARGET = 1.0

def lookToPoint(tracker):
    tracker.helper.lookToPoint(tracker.target)
    return tracker.stay()

def lookToTarget(tracker):
    """looks to best guess of where target is"""
    #should only be called by states that have already set activeLocOn=False

    if tracker.target.framesOn > constants.TRACKER_FRAMES_ON_TRACK_THRESH:
        return tracker.goNow('targetTracking')

    elif tracker.stateTime >= TIME_TO_LOOK_TO_TARGET:
        return tracker.goLater('scanForTarget')

    tracker.helper.lookToPoint()

    return tracker.stay()

def scanForTarget(tracker):
    """performs naive scan for target"""
    if tracker.target.framesOn > constants.TRACKER_FRAMES_ON_TRACK_THRESH:
        return tracker.goNow('targetTracking')

    if not tracker.brain.motion.isHeadActive():
        targetDist = tracker.target.locDist

        if targetDist > HeadMoves.HIGH_SCAN_CLOSE_BOUND:
            tracker.helper.executeHeadMove(HeadMoves.HIGH_SCAN_BALL)

        elif ( targetDist > HeadMoves.MID_SCAN_CLOSE_BOUND and
               targetDist < HeadMoves.MID_SCAN_FAR_BOUND ):
            tracker.helper.executeHeadMove(HeadMoves.MID_UP_SCAN_BALL)

        else:
            tracker.helper.executeHeadMove(HeadMoves.LOW_SCAN_BALL)

    return tracker.stay()

def targetTracking(tracker):
    """
    state askes it's parent (the tracker) for an object or angles to track
    while the object is on screen, or angles are passed, we track it.
    Otherwise, we continually write the current values into motion via setHeads.

    If a sweet move is begun while we are tracking, the current setup is to let
    the sweet move conclude and then resume tracking afterward.
    """

    if tracker.firstFrame():
        tracker.activeLocOn = False

    tracker.helper.trackObject()

    if tracker.target.framesOff > constants.TRACKER_FRAMES_OFF_REFIND_THRESH:
        return tracker.goLater('lookToTarget')

    return tracker.stay()
