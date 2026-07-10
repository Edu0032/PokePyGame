from functools import lru_cache
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POKEPY_", env_file=".env", extra="ignore")

    api_title: str = "PokePY API"
    api_version: str = "4.1.0"
    api_description: str = "API REST para ranking, progresso de jogador e multiplayer do PokePY."
    database_url: str = "mysql+pymysql://pokepy_user:pokepy_password@127.0.0.1:3306/pokepy"
    leaderboard_max_entries: int = Field(default=100, ge=1, le=1000)
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    log_level: str = "INFO"
    auto_create_tables: bool = True


@lru_cache
def get_api_settings() -> ApiSettings:
    settings = ApiSettings()
    database_url = os.getenv("POKEPY_DATABASE_URL") or os.getenv("DATABASE_URL") or settings.database_url
    return settings.model_copy(update={"database_url": database_url})
