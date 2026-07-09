class MultiplayerError(Exception):
    pass


class MatchNotFoundError(MultiplayerError):
    pass


class InvalidTurnError(MultiplayerError):
    pass


class PlayerNotInMatchError(MultiplayerError):
    pass
