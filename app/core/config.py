import os
import secrets
from typing import Any

from pydantic import ValidationInfo, field_validator
from pydantic.networks import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False

    API_PREFIX: str = "/api"
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_EXPIRE: int = 60 * 24 * 8

    DB_HOST: str = "localhost"
    DB_PORT: int = 5433
    DB_DATABASE: str = "main"
    DB_USERNAME: str = "main"
    DB_PASSWORD: str = "main"
    DATABASE_URL: PostgresDsn | None = None
    DATABASE_RO_URL: PostgresDsn | None = None

    @field_validator("DATABASE_URL")
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn(
            f"""postgresql+psycopg://{info.data["DB_USERNAME"]}:{info.data["DB_PASSWORD"]}@
{info.data["DB_HOST"]}:{info.data["DB_PORT"]}/{info.data["DB_DATABASE"]}"""
        )

    model_config = SettingsConfigDict(
        env_file=(".env.testing" if os.getenv("PYTHON_ENVIRONNEMENT") == "testing" else ".env")
    )


class SettingsReadOnly(BaseSettings):
    DB_HOST: str = "localhost"
    DB_RO_HOST: str | None = None
    DB_PORT: int = 5433
    DB_DATABASE: str = "main"
    DB_USERNAME: str = "main"
    DB_PASSWORD: str = "main"
    DATABASE_RO_URL: PostgresDsn | None = None

    @field_validator("DATABASE_RO_URL")
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn(
            f"""postgresql+psycopg://{info.data["DB_USERNAME"]}:{info.data["DB_PASSWORD"]}@
{info.data["DB_HOST"] or info.data["DB_RO_HOST"]}:{info.data["DB_PORT"]}/{info.data["DB_DATABASE"]}"""
        )

    model_config = SettingsConfigDict(
        env_file=(".env.testing" if os.getenv("PYTHON_ENVIRONNEMENT") == "testing" else ".env"),
        extra="allow",
    )


settings = Settings()
settingsReadOnly = SettingsReadOnly()
