from functools import lru_cache

from pydantic import Field, computed_field
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

    # -----------------------------
    # PostgreSQL
    # -----------------------------
    postgres_host: str = Field(
        default="localhost",
        alias="POSTGRES_HOST",
    )

    postgres_port: int = Field(
        default=5432,
        alias="POSTGRES_PORT",
    )

    postgres_db: str = Field(
        default="compliance_db",
        alias="POSTGRES_DB",
    )

    postgres_user: str = Field(
        default="postgres",
        alias="POSTGRES_USER",
    )

    postgres_password: str = Field(
        default="postgres",
        alias="POSTGRES_PASSWORD",
    )

    # -----------------------------
    # JWT
    # -----------------------------
    jwt_secret_key: str = Field(
        alias="JWT_SECRET_KEY",
    )

    jwt_algorithm: str = Field(
        default="HS256",
        alias="JWT_ALGORITHM",
    )

    jwt_access_token_expire_minutes: int = Field(
        default=30,
        alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    # -----------------------------
    # AWS
    # -----------------------------
    aws_region: str = Field(
        default="eu-north-1",
        alias="AWS_REGION",
    )

    aws_s3_bucket_name: str = Field(
        alias="AWS_S3_BUCKET_NAME",
    )

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    """
    Return one cached settings instance.
    """

    return Settings()


settings = get_settings()