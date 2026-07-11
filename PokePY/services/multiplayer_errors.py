class MultiplayerError(Exception):
    pass


class MatchNotFoundError(MultiplayerError):
    pass


class InvalidTurnError(MultiplayerError):
    pass


class PlayerNotInMatchError(MultiplayerError):
    pass


class InvalidActionError(MultiplayerError):
    pass


class TicketNotFoundError(MultiplayerError):
    pass
