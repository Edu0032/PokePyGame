from PokePY.domain.models import Player, Pokemon
from PokePY.services.leaderboard_contracts import LeaderboardEntry
from PokePY.services.player_progress_service import PlayerProgressService


def test_sqlalchemy_leaderboard_orders_scores(sqlalchemy_repositories):
    leaderboard = sqlalchemy_repositories.leaderboard
    leaderboard.save_score(LeaderboardEntry("B", 90, "2026-01-01T00:00:02+00:00"))
    leaderboard.save_score(LeaderboardEntry("A", 40, "2026-01-01T00:00:01+00:00"))
    assert [entry.player_name for entry in leaderboard.top_scores(10)] == ["A", "B"]


def test_sqlalchemy_progress_roundtrip(sqlalchemy_repositories):
    service = PlayerProgressService(sqlalchemy_repositories.progress)
    player = Player(team=[Pokemon("Pikachu", "Elétrico", level=3, hp=80, max_hp=120, xp=20)], items={"Poção": 2}, x=15, y=30, zone_index=1)
    service.save("player-1", player, "Jogador 1")
    restored = service.load("player-1")
    assert restored is not None
    assert restored.team[0].level == 3
    assert restored.items["Poção"] == 2
    assert restored.zone_index == 1


def test_api_saves_and_lists_leaderboard(api_client):
    response = api_client.post("/leaderboard", json={"player_name": "Ana", "elapsed_seconds": 50})
    assert response.status_code == 201
    assert response.json()["position"] == 1
    response = api_client.get("/leaderboard", params={"limit": 10})
    assert response.status_code == 200
    assert response.json()[0]["player_name"] == "Ana"


def test_api_saves_and_loads_progress(api_client):
    payload = {
        "player_id": "player-1",
        "player_name": "Jogador 1",
        "zone_index": 2,
        "x": 100,
        "y": 250,
        "items": {"Poção": 1},
        "team": [
            {
                "name": "Squirtle",
                "type": "Água",
                "level": 4,
                "hp": 75,
                "max_hp": 120,
                "xp": 45,
                "attacks": ["Ataque Básico"],
                "evolution_stage": 0,
            }
        ],
    }
    response = api_client.put("/players/player-1/progress", json=payload)
    assert response.status_code == 200
    response = api_client.get("/players/player-1/progress")
    assert response.status_code == 200
    assert response.json()["team"][0]["level"] == 4


def test_api_returns_paginated_leaderboard(api_client):
    api_client.post("/leaderboard", json={"player_name": "Ana", "elapsed_seconds": 30})
    api_client.post("/leaderboard", json={"player_name": "Bruno", "elapsed_seconds": 40})
    response = api_client.get("/leaderboard/page", params={"limit": 1, "offset": 1})
    assert response.status_code == 200
    assert response.json()["returned"] == 1
    assert response.json()["items"][0]["player_name"] == "Bruno"
