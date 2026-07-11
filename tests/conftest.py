from collections.abc import Iterator
from dataclasses import dataclass

import pytest
from fastapi.testclient import TestClient
from PokePY.api.application import create_app
from PokePY.infrastructure.sqlalchemy.database import create_database_engine, create_session_factory, create_tables
from PokePY.infrastructure.sqlalchemy.leaderboard_repository import SQLAlchemyLeaderboardRepository
from PokePY.infrastructure.sqlalchemy.multiplayer_repository import SQLAlchemyMultiplayerRepository
from PokePY.infrastructure.sqlalchemy.player_progress_repository import SQLAlchemyPlayerProgressRepository
from sqlalchemy.engine import Engine


@dataclass(frozen=True)
class TestRepositories:
    engine: Engine
    leaderboard: SQLAlchemyLeaderboardRepository
    progress: SQLAlchemyPlayerProgressRepository
    multiplayer: SQLAlchemyMultiplayerRepository


@pytest.fixture
def sqlalchemy_repositories() -> Iterator[TestRepositories]:
    engine = create_database_engine("sqlite:///:memory:")
    create_tables(engine)
    session_factory = create_session_factory(engine)
    yield TestRepositories(
        engine=engine,
        leaderboard=SQLAlchemyLeaderboardRepository(session_factory, max_entries=100),
        progress=SQLAlchemyPlayerProgressRepository(session_factory),
        multiplayer=SQLAlchemyMultiplayerRepository(session_factory),
    )
    engine.dispose()


@pytest.fixture
def api_client(sqlalchemy_repositories: TestRepositories) -> Iterator[TestClient]:
    app = create_app(
        leaderboard_repository=sqlalchemy_repositories.leaderboard,
        progress_repository=sqlalchemy_repositories.progress,
        multiplayer_repository=sqlalchemy_repositories.multiplayer,
    )
    with TestClient(app) as client:
        yield client


@pytest.fixture
def multiplayer_player_payload():
    def build(player_id: str, player_name: str, hp: int = 100) -> dict:
        return {
            "player_id": player_id,
            "player_name": player_name,
            "active_pokemon_index": 0,
            "items": {"Poção": 1},
            "team": [
                {
                    "name": "Pikachu" if player_id == "p1" else "Squirtle",
                    "type": "Elétrico" if player_id == "p1" else "Água",
                    "level": 3,
                    "hp": hp,
                    "max_hp": 100,
                    "xp": 0,
                    "attacks": ["Ataque Básico", "Ataque Especial"],
                    "evolution_stage": 0,
                }
            ],
        }

    return build
