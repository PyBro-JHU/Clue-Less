

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
