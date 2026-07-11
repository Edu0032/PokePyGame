from typing import Any, cast

from PokePY.infrastructure.http.json_client import HttpJsonClient
from PokePY.services.leaderboard_contracts import LeaderboardEntry


class ApiLeaderboardRepository:
    def __init__(self, client: HttpJsonClient):
        self.client = client

    def save_score(self, entry: LeaderboardEntry) -> LeaderboardEntry:
        payload = {
            "player_name": entry.player_name,
            "elapsed_seconds": entry.elapsed_seconds,
        }
        response = self.client.post("/leaderboard", payload)
        response_dict = cast(dict[str, Any], response)
        return self._entry_from_payload(cast(dict[str, Any], response_dict["entry"]))

    def top_scores(self, limit: int = 10) -> list[LeaderboardEntry]:
        response = self.client.get("/leaderboard", params={"limit": limit})
        rows = cast(list[dict[str, Any]], response)
        return [self._entry_from_payload(item) for item in rows]

    def _entry_from_payload(self, payload: dict[str, Any]) -> LeaderboardEntry:
        return LeaderboardEntry(
            player_name=str(payload["player_name"]),
            elapsed_seconds=int(payload["elapsed_seconds"]),
            created_at=str(payload["created_at"]),
        )
