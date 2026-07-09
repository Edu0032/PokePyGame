from typing import Protocol

from PokePY.domain.models import Player

class PlayerProgressRepository(Protocol):
    def save(self, player_id: str, player: Player) -> None:
        ...

    def load(self, player_id: str) -> Player | None:
        ...
