from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from PokePY.api.dependencies import create_repository_bundle
from PokePY.api.errors import register_exception_handlers
from PokePY.api.logging import configure_logging
from PokePY.api.routes.health import create_health_router
from PokePY.api.routes.leaderboard import create_leaderboard_router
from PokePY.api.routes.multiplayer import create_multiplayer_router
from PokePY.api.routes.progress import create_progress_router
from PokePY.api.settings import ApiSettings, get_api_settings
from PokePY.services.leaderboard_service import LeaderboardService
from PokePY.services.multiplayer_service import MultiplayerService


def create_app(
    database_url: str | None = None,
    leaderboard_repository=None,
    progress_repository=None,
    multiplayer_repository=None,
    settings: ApiSettings | None = None,
) -> FastAPI:
    resolved_settings = settings or get_api_settings()
    configure_logging(resolved_settings.log_level)
    repository_bundle = None
    if leaderboard_repository is None or progress_repository is None or multiplayer_repository is None:
        repository_bundle = create_repository_bundle(resolved_settings, database_url)
        leaderboard_repository = leaderboard_repository or repository_bundle.leaderboard_repository
        progress_repository = progress_repository or repository_bundle.progress_repository
        multiplayer_repository = multiplayer_repository or repository_bundle.multiplayer_repository

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        if repository_bundle and repository_bundle.engine:
            repository_bundle.engine.dispose()

    app = FastAPI(
        title=resolved_settings.api_title,
        version=resolved_settings.api_version,
        description=resolved_settings.api_description,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(create_health_router(repository_bundle.engine if repository_bundle else None))
    app.include_router(create_leaderboard_router(LeaderboardService(leaderboard_repository)))
    app.include_router(create_progress_router(progress_repository))
    app.include_router(create_multiplayer_router(MultiplayerService(multiplayer_repository)))
    register_exception_handlers(app)
    return app
