from PokePY.services.leaderboard_contracts import LeaderboardEntry, LeaderboardRepository


class FallbackLeaderboardRepository:
    def __init__(self, primary: LeaderboardRepository, fallback: LeaderboardRepository):
        self.primary = primary
        self.fallback = fallback

    def save_score(self, entry: LeaderboardEntry) -> LeaderboardEntry:
        try:
            return self.primary.save_score(entry)
        except Exception:
            return self.fallback.save_score(entry)

    def top_scores(self, limit: int = 10) -> list[LeaderboardEntry]:
        try:
            return self.primary.top_scores(limit)
        except Exception:
            return self.fallback.top_scores(limit)
