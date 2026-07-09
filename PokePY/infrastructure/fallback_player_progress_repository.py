from PokePY.services.player_progress_service import PlayerProgress


class FallbackPlayerProgressRepository:
    def __init__(self, primary_repository, fallback_repository):
        self.primary_repository = primary_repository
        self.fallback_repository = fallback_repository

    def save(self, player_id: str, player) -> None:
        try:
            self.primary_repository.save(player_id, player)
        except Exception:
            self.fallback_repository.save(player_id, player)

    def load(self, player_id: str):
        try:
            player = self.primary_repository.load(player_id)
        except Exception:
            player = None
        return player if player is not None else self.fallback_repository.load(player_id)

    def save_progress(self, progress: PlayerProgress) -> PlayerProgress:
        try:
            return self.primary_repository.save_progress(progress)
        except Exception:
            return self.fallback_repository.save_progress(progress)

    def load_progress(self, player_id: str) -> PlayerProgress | None:
        try:
            progress = self.primary_repository.load_progress(player_id)
        except Exception:
            progress = None
        return progress if progress is not None else self.fallback_repository.load_progress(player_id)
