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
        return self._entry_from_payload(response["entry"])

    def top_scores(self, limit: int = 10) -> list[LeaderboardEntry]:
        response = self.client.get("/leaderboard", params={"limit": limit})
        return [self._entry_from_payload(item) for item in response]

    def _entry_from_payload(self, payload: dict) -> LeaderboardEntry:
        return LeaderboardEntry(
            player_name=str(payload["player_name"]),
            elapsed_seconds=int(payload["elapsed_seconds"]),
            created_at=str(payload["created_at"]),
        )
