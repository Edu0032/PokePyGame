import json
from pathlib import Path

from PokePY.domain.models import Player
from PokePY.services.player_progress_service import PlayerProgress, PlayerProgressService


class JsonPlayerProgressRepository:
    def __init__(self, directory: Path):
        self.directory = directory
        self.serializer = PlayerProgressService(self)

    def save(self, player_id: str, player: Player) -> None:
        self.save_progress(self.serializer.to_progress(player_id, player_id, player))

    def load(self, player_id: str) -> Player | None:
        progress = self.load_progress(player_id)
        return self.serializer.from_progress(progress) if progress else None

    def save_progress(self, progress: PlayerProgress) -> PlayerProgress:
        self.directory.mkdir(parents=True, exist_ok=True)
        with self._file_path(progress.player_id).open("w", encoding="utf-8") as file:
            json.dump(self.serializer.to_dict(progress), file, ensure_ascii=False, indent=2)
        return progress

    def load_progress(self, player_id: str) -> PlayerProgress | None:
        file_path = self._file_path(player_id)
        if not file_path.exists():
            return None
        try:
            with file_path.open("r", encoding="utf-8") as file:
                payload = json.load(file)
            return self.serializer.from_dict(payload)
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
            return None

    def _file_path(self, player_id: str) -> Path:
        safe_id = "".join(char for char in player_id.lower() if char.isalnum() or char in {"-", "_"}) or "treinador"
        return self.directory / f"{safe_id}.json"
