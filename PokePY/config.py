from dataclasses import dataclass, field
from pathlib import Path

from PokePY.distribution.runtime_config import config_bool, config_float, config_int, config_value, project_base_dir, save_dir

BASE_DIR = project_base_dir()
ASSET_DIR = BASE_DIR
SAVE_DIR = save_dir()
LEADERBOARD_FILE = SAVE_DIR / "leaderboard.json"
PROGRESS_DIR = SAVE_DIR / "players"


@dataclass(frozen=True)
class ScreenConfig:
    width: int = 800
    height: int = 640
    fps: int = 60
    title: str = "PokePY"


@dataclass(frozen=True)
class PlayerConfig:
    start_x: int = 50
    start_y: int = 320
    move_speed: int = 5
    sprite_size: int = 64
    animation_interval_ms: int = 200
    animation_first_frame: int = 2
    animation_last_frame: int = 4
    boundary_padding: int = 10
    team_size: int = 3


@dataclass(frozen=True)
class BattleConfig:
    basic_damage_min: int = 10
    basic_damage_max: int = 30
    special_damage_min: int = 25
    special_damage_max: int = 45
    enemy_damage_min: int = 5
    enemy_damage_max: int = 20
    boss_damage_multiplier: int = 5
    potion_heal: int = 50
    flee_chance: float = 0.5
    xp_multiplier: int = 50


@dataclass(frozen=True)
class ItemConfig:
    message_duration_ms: int = 1500
    pickup_cooldown_seconds: float = 1.5
    repel_duration_ms: int = 5000
    initial_items: dict[str, int] = field(default_factory=lambda: {"Poção": 5, "Repelente": 1})
    item_caps: dict[str, int] = field(default_factory=lambda: {"Poção": 5, "Repelente": 1})


@dataclass(frozen=True)
class WorldConfig:
    transition_edge_x: int = 780
    zone_entry_x: int = 20
    blocked_entry_x: int = 770
    boss_trigger_distance_from_right: int = 180
    boss_path_half_height: int = 50


@dataclass(frozen=True)
class BackendConfig:
    mode: str = config_value("BACKEND_MODE", "json").strip().lower()
    leaderboard_backend: str = config_value("LEADERBOARD_BACKEND", mode).strip().lower()
    progress_backend: str = config_value("PROGRESS_BACKEND", mode).strip().lower()
    multiplayer_backend: str = config_value("MULTIPLAYER_BACKEND", "api").strip().lower()


@dataclass(frozen=True)
class LeaderboardConfig:
    max_entries: int = config_int("LEADERBOARD_MAX_ENTRIES", 100)
    display_limit: int = config_int("LEADERBOARD_DISPLAY_LIMIT", 10)


@dataclass(frozen=True)
class ApiConfig:
    base_url: str = config_value("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    timeout_seconds: float = config_float("API_TIMEOUT_SECONDS", 5.0)
    host: str = config_value("API_HOST", "127.0.0.1")
    port: int = config_int("API_PORT", 8000)
    use_json_fallback: bool = config_bool("API_JSON_FALLBACK", True)


@dataclass(frozen=True)
class DatabaseConfig:
    url: str = config_value("DATABASE_URL", "mysql+pymysql://pokepy_user:pokepy_password@127.0.0.1:3306/pokepy")


@dataclass(frozen=True)
class UIConfig:
    team_menu_width: int = 450
    team_button_height: int = 50
    team_button_padding: int = 15
    inventory_width: int = 500
    inventory_height: int = 400
    modal_width: int = 500
    modal_height: int = 150
    backpack_button_radius: int = 22


SCREEN_CONFIG = ScreenConfig()
PLAYER_CONFIG = PlayerConfig(start_y=SCREEN_CONFIG.height // 2)
BATTLE_CONFIG = BattleConfig()
ITEM_CONFIG = ItemConfig()
WORLD_CONFIG = WorldConfig()
UI_CONFIG = UIConfig()
BACKEND_CONFIG = BackendConfig()
LEADERBOARD_CONFIG = LeaderboardConfig()
API_CONFIG = ApiConfig()
DATABASE_CONFIG = DatabaseConfig()
