from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class LeaderboardEntry:
    player_name: str
    elapsed_seconds: int
    created_at: str

class LeaderboardRepository(Protocol):
    def save_score(self, entry: LeaderboardEntry) -> LeaderboardEntry:
        ...

    def top_scores(self, limit: int = 10) -> list[LeaderboardEntry]:
        ...
