"""Configuration management using Pydantic settings."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Supabase Configuration
    supabase_url: str
    supabase_key: str

    # Optional nflreadpy cache configuration
    nflreadpy_cache_dir: Optional[str] = ".nflreadpy_cache"
    nflreadpy_cache_type: Optional[str] = "filesystem"

    # Database table names (can be customized)
    table_pbp: str = "play_by_play"
    table_player_stats: str = "player_stats"
    table_team_stats: str = "team_stats"
    table_rosters: str = "rosters"
    table_schedules: str = "schedules"
    table_players: str = "players"
    table_teams: str = "teams"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
