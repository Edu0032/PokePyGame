from pathlib import Path

from PokePY.infrastructure.json_leaderboard_repository import JsonLeaderboardRepository
from PokePY.services.leaderboard_contracts import LeaderboardEntry
from PokePY.services.leaderboard_service import LeaderboardService
from PokePY.services.time_formatter import format_seconds


def test_repository_keeps_scores_sorted_by_time(tmp_path: Path):
    repository = JsonLeaderboardRepository(tmp_path / "leaderboard.json")
    repository.save_score(LeaderboardEntry("B", 80, "2026-01-01T00:00:02+00:00"))
    repository.save_score(LeaderboardEntry("A", 50, "2026-01-01T00:00:01+00:00"))
    repository.save_score(LeaderboardEntry("C", 120, "2026-01-01T00:00:03+00:00"))
    assert [entry.player_name for entry in repository.top_scores()] == ["A", "B", "C"]


def test_service_normalizes_empty_name(tmp_path: Path):
    service = LeaderboardService(JsonLeaderboardRepository(tmp_path / "leaderboard.json"))
    result = service.register_completion("   ", 12)
    assert result.entry.player_name == "Treinador"
    assert result.position == 1


def test_time_formatter():
    assert format_seconds(65) == "01:05"
    assert format_seconds(3661) == "01:01:01"
