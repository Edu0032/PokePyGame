from dataclasses import dataclass
from datetime import datetime, timezone

from PokePY.services.leaderboard_contracts import LeaderboardEntry, LeaderboardRepository

@dataclass
class LeaderboardSaveResult:
    entry: LeaderboardEntry
    position: int | None

class LeaderboardService:
    def __init__(self, repository: LeaderboardRepository):
        self.repository = repository

    def register_completion(self, player_name: str, elapsed_seconds: int) -> LeaderboardSaveResult:
        entry = LeaderboardEntry(
            player_name=self._normalize_player_name(player_name),
            elapsed_seconds=max(0, int(elapsed_seconds)),
            created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )
        saved_entry = self.repository.save_score(entry)
        return LeaderboardSaveResult(entry=saved_entry, position=self.find_position(saved_entry))

    def top_scores(self, limit: int = 10) -> list[LeaderboardEntry]:
        return self.repository.top_scores(limit)

    def find_position(self, entry: LeaderboardEntry) -> int | None:
        scores = self.repository.top_scores(1000)
        for index, score in enumerate(scores, start=1):
            if score == entry:
                return index
        return None

    def _normalize_player_name(self, name: str) -> str:
        clean_name = " ".join(name.strip().split())
        return clean_name or "Treinador"
