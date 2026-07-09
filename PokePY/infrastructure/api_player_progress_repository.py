from PokePY.domain.models import Player
from PokePY.infrastructure.http.json_client import HttpJsonClient
from PokePY.services.player_progress_service import PlayerProgress, PlayerProgressService

class ApiPlayerProgressRepository:
    def __init__(self, client: HttpJsonClient):
        self.client = client
        self.serializer = PlayerProgressService(self)

    def save(self, player_id: str, player: Player) -> None:
        self.save_progress(self.serializer.to_progress(player_id, player_id, player))

    def load(self, player_id: str) -> Player | None:
        progress = self.load_progress(player_id)
        return self.serializer.from_progress(progress) if progress else None

    def save_progress(self, progress: PlayerProgress) -> PlayerProgress:
        payload = self.serializer.to_dict(progress)
        response = self.client.put(f"/players/{progress.player_id}/progress", payload)
        return self.serializer.from_dict(response["progress"])

    def load_progress(self, player_id: str) -> PlayerProgress | None:
        try:
            response = self.client.get(f"/players/{player_id}/progress")
        except Exception:
            return None
        return self.serializer.from_dict(response)
