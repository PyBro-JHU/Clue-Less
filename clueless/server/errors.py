

class GameEngineException(Exception):
    pass


class PlayerInvalidException(GameEngineException):
    def __init__(self):
        msg = "Player specified does not exist"
        super(PlayerInvalidException, self).__init__(msg)


class PlayerOperationOutOfTurnException(GameEngineException):
    def __init__(self):
        msg = "Player operation attempted out of turn"
        super(PlayerOperationOutOfTurnException, self).__init__(msg)


class PlayerInvalidSuspectException(GameEngineException):
    def __init__(self):
        msg = "Player does not own this supsect"
        super(PlayerInvalidSuspectException, self).__init__(msg)


class GameSpaceInvalidException(GameEngineException):
    def __init__(self):
        msg = "GameSpace specified does not exist"
        super(GameSpaceInvalidException, self).__init__(msg)


class GameSpaceUnavilableException(GameEngineException):
    def __init__(self):
        msg = "GameSpace specified is occupied or unavailable for move"
        super(GameSpaceUnavilableException, self).__init__(msg)


class GameSpaceNotConnectedException(GameEngineException):
    def __init__(self):
        msg = "GameSpace specified is adjacent to the player's current space"
        super(GameSpaceNotConnectedException, self).__init__(msg)


class SuspectInvalidException(GameEngineException):
    def __init__(self):
        msg = "Invalid Suspect"
        super(SuspectInvalidException, self).__init__(msg)


class WeaponInvalidException(GameEngineException):
    def __init__(self):
        msg = "Invalid Weapon"
        super(WeaponInvalidException, self).__init__(msg)


class RoomInvalidException(GameEngineException):
    def __init__(self):
        msg = "Invalid Room"
        super(RoomInvalidException, self).__init__(msg)


class SuggestionTurnStatusException(GameEngineException):
    def __init__(self):
        msg = "Suggestion can not be made when awaiting a move or accusation"
        super(SuggestionTurnStatusException, self).__init__(msg)


class SuggestionInvalidRoomException(GameEngineException):
    def __init__(self):
        msg = "Suggestion invalid, player must be in room used in suggestion"
        super(SuggestionInvalidRoomException, self).__init__(msg)


class SuggestionResponsePlayerInvalidException(GameEngineException):
    def __init__(self):
        msg = "Invalid, not the correct player to respond to suggestion"
        super(SuggestionResponsePlayerInvalidException, self).__init__(msg)
