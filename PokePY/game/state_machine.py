from typing import Protocol

from PokePY.domain.game_state import GameState


class GameStateHandler(Protocol):
    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        ...


class StateMachine:
    def __init__(self, handlers: dict[GameState, GameStateHandler]):
        self.handlers = handlers

    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        try:
            handler = self.handlers[game.state]
        except KeyError as error:
            raise RuntimeError(f"Estado de jogo sem handler registrado: {game.state}") from error
        handler.update(game, current_time_ms, current_time_seconds)
