from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -----------------------------
    # Application
    # -----------------------------
    app_name: str = Field(
        default="Enterprise AI Compliance Review Platform",
        alias="APP_NAME",
    )

    app_version: str = Field(
        default="0.1.0",
        alias="APP_VERSION",
    )

    app_env: str = Field(
        default="development",
        alias="APP_ENV",
    )

    debug: bool = Field(
        default=True,
        alias="DEBUG",
    )

    app_description: str = Field(
        default="Enterprise AI Compliance Review Platform API",
        alias="APP_DESCRIPTION",
    )

    author_name: str = Field(
        default="Zubeda Abbas",
        alias="AUTHOR_NAME",
    )

    author_url: str = Field(
        default="https://github.com/bzubeda64",
        alias="AUTHOR_URL",
    )

    license_name: str = Field(
        default="MIT",
        alias="LICENSE_NAME",
    )

    # -----------------------------
    # API
    # -----------------------------
    api_v1_prefix: str = Field(
        default="/api/v1",
        alias="API_V1_PREFIX",
    )

    host: str = Field(
        default="0.0.0.0",
        alias="HOST",
    )

    port: int = Field(
        default=8000,
        alias="PORT",
    )

    # -----------------------------
    # Logging
    # -----------------------------
    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.

    Ensures configuration is loaded only once.
    """
    return Settings()


settings = get_settings()