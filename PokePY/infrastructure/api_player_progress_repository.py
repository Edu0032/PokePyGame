from typing import Any, cast

from PokePY.domain.models import Player
from PokePY.infrastructure.http.json_client import HttpJsonClient
from PokePY.services.player_progress_service import PlayerProgress, PlayerProgressService


class ApiPlayerProgressRepository:
    def __init__(self, client: HttpJsonClient):
        self.client = client
        self.serializer = PlayerProgressService(None)

    def save(self, player_id: str, player: Player) -> None:
        self.save_progress(self.serializer.to_progress(player_id, player_id, player))

    def load(self, player_id: str) -> Player | None:
        progress = self.load_progress(player_id)
        return self.serializer.from_progress(progress) if progress else None

    def save_progress(self, progress: PlayerProgress) -> PlayerProgress:
        payload = self.serializer.to_dict(progress)
        response = cast(dict[str, Any], self.client.put(f"/players/{progress.player_id}/progress", payload))
        return self.serializer.from_dict(cast(dict[str, Any], response["progress"]))

    def load_progress(self, player_id: str) -> PlayerProgress | None:
        response = self.client.request(
            "GET",
            f"/players/{player_id}/progress",
            allow_not_found=True,
        )
        if response is None:
            return None
        return self.serializer.from_dict(cast(dict[str, Any], response))
