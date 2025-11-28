"""
Config - Configuracoes da aplicacao
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """configuracoes da aplicacao"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # app
    app_name: str = "Python Template"
    app_version: str = "1.0.0"
    debug: bool = False

    # server
    host: str = "0.0.0.0"
    port: int = 8000

    # database (exemplo)
    database_url: str = "sqlite:///./app.db"

    # cors
    cors_origins: list[str] = ["*"]

    # auth (exemplo)
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30


@lru_cache
def get_settings() -> Settings:
    """retorna configuracoes cacheadas"""
    return Settings()

