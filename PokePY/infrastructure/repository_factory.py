from PokePY.config import API_CONFIG, BACKEND_CONFIG, LEADERBOARD_CONFIG, LEADERBOARD_FILE, PROGRESS_DIR
from PokePY.infrastructure.api_leaderboard_repository import ApiLeaderboardRepository
from PokePY.infrastructure.api_multiplayer_gateway import ApiMultiplayerGateway
from PokePY.infrastructure.api_player_progress_repository import ApiPlayerProgressRepository
from PokePY.infrastructure.fallback_leaderboard_repository import FallbackLeaderboardRepository
from PokePY.infrastructure.fallback_player_progress_repository import FallbackPlayerProgressRepository
from PokePY.infrastructure.http.json_client import HttpJsonClient
from PokePY.infrastructure.json_leaderboard_repository import JsonLeaderboardRepository
from PokePY.infrastructure.json_player_progress_repository import JsonPlayerProgressRepository


def create_http_client() -> HttpJsonClient:
    return HttpJsonClient(API_CONFIG.base_url, API_CONFIG.timeout_seconds)


def create_local_leaderboard_repository() -> JsonLeaderboardRepository:
    return JsonLeaderboardRepository(LEADERBOARD_FILE, LEADERBOARD_CONFIG.max_entries)


def create_api_leaderboard_repository() -> ApiLeaderboardRepository:
    return ApiLeaderboardRepository(create_http_client())


def create_leaderboard_repository():
    local_repository = create_local_leaderboard_repository()
    if BACKEND_CONFIG.leaderboard_backend != "api":
        return local_repository
    api_repository = create_api_leaderboard_repository()
    if API_CONFIG.use_json_fallback:
        return FallbackLeaderboardRepository(api_repository, local_repository)
    return api_repository


def create_player_progress_repository():
    local_repository = JsonPlayerProgressRepository(PROGRESS_DIR)
    if BACKEND_CONFIG.progress_backend != "api":
        return local_repository
    api_repository = ApiPlayerProgressRepository(create_http_client())
    if API_CONFIG.use_json_fallback:
        return FallbackPlayerProgressRepository(api_repository, local_repository)
    return api_repository


def create_multiplayer_gateway() -> ApiMultiplayerGateway:
    return ApiMultiplayerGateway(create_http_client())
