from dataclasses import dataclass

from sqlalchemy.engine import Engine

from PokePY.api.settings import ApiSettings
from PokePY.infrastructure.sqlalchemy.database import create_database_engine, create_session_factory, create_tables
from PokePY.infrastructure.sqlalchemy.leaderboard_repository import SQLAlchemyLeaderboardRepository
from PokePY.infrastructure.sqlalchemy.multiplayer_repository import SQLAlchemyMultiplayerRepository
from PokePY.infrastructure.sqlalchemy.player_progress_repository import SQLAlchemyPlayerProgressRepository


@dataclass(frozen=True)
class RepositoryBundle:
    leaderboard_repository: SQLAlchemyLeaderboardRepository
    progress_repository: SQLAlchemyPlayerProgressRepository
    multiplayer_repository: SQLAlchemyMultiplayerRepository
    engine: Engine | None = None


def create_repository_bundle(settings: ApiSettings, database_url: str | None = None) -> RepositoryBundle:
    engine = create_database_engine(database_url or settings.database_url)
    if settings.auto_create_tables:
        create_tables(engine)
    session_factory = create_session_factory(engine)
    return RepositoryBundle(
        leaderboard_repository=SQLAlchemyLeaderboardRepository(session_factory, settings.leaderboard_max_entries),
        progress_repository=SQLAlchemyPlayerProgressRepository(session_factory),
        multiplayer_repository=SQLAlchemyMultiplayerRepository(session_factory),
        engine=engine,
    )
