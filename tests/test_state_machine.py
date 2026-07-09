import pytest

from PokePY.domain.game_state import GameState
from PokePY.game.state_machine import StateMachine


class DummyHandler:
    def __init__(self):
        self.called = False

    def update(self, game, current_time_ms: int, current_time_seconds: float) -> None:
        self.called = True


class DummyGame:
    state = GameState.EXPLORE


def test_state_machine_delegates_to_registered_handler():
    handler = DummyHandler()
    machine = StateMachine({GameState.EXPLORE: handler})
    machine.update(DummyGame(), 1, 1.0)
    assert handler.called is True


def test_state_machine_rejects_unregistered_state():
    machine = StateMachine({})
    with pytest.raises(RuntimeError):
        machine.update(DummyGame(), 1, 1.0)
