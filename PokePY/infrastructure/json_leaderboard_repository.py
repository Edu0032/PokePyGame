import json
from pathlib import Path

from PokePY.services.leaderboard_contracts import LeaderboardEntry


class JsonLeaderboardRepository:
    def __init__(self, file_path: Path, max_entries: int = 100):
        self.file_path = file_path
        self.max_entries = max_entries

    def save_score(self, entry: LeaderboardEntry) -> LeaderboardEntry:
        entries = self._read_entries()
        entries.append(entry)
        entries = self._sort_entries(entries)[: self.max_entries]
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump([entry.__dict__ for entry in entries], file, ensure_ascii=False, indent=2)
        return entry

    def top_scores(self, limit: int = 10) -> list[LeaderboardEntry]:
        return self._sort_entries(self._read_entries())[: max(0, int(limit))]

    def _read_entries(self) -> list[LeaderboardEntry]:
        if not self.file_path.exists():
            return []
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                payload = json.load(file)
            return [self._entry_from_dict(item) for item in payload]
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
            return []

    def _entry_from_dict(self, payload: dict) -> LeaderboardEntry:
        return LeaderboardEntry(
            player_name=str(payload["player_name"]),
            elapsed_seconds=int(payload["elapsed_seconds"]),
            created_at=str(payload["created_at"]),
        )

    def _sort_entries(self, entries: list[LeaderboardEntry]) -> list[LeaderboardEntry]:
        return sorted(entries, key=lambda entry: (entry.elapsed_seconds, entry.created_at, entry.player_name.lower()))
