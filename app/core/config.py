import os
import secrets
from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator
from pydantic.networks import PostgresDsn


class Settings(BaseSettings):
    DEBUG: bool = False

    API_PREFIX = "/api"
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_EXPIRE: int = 60 * 24 * 8

    DB_HOST: str
    DB_PORT: int
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DATABASE_URL: Optional[PostgresDsn] = None
    DATABASE_RO_URL: Optional[PostgresDsn] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USERNAME"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=str(values.get("DB_PORT")),
            path=f"/{values.get('DB_DATABASE') or ''}",
        )

    class Config:
        env_file = (
            ".env.testing" if os.getenv("PYTHON_ENVIRONNEMENT") == "testing" else ".env"
        )


class SettingsReadOnly(BaseSettings):

    DB_HOST: str
    DB_RO_HOST: Optional[str] = None
    DB_PORT: int
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DATABASE_RO_URL: Optional[PostgresDsn] = None

    @validator("DATABASE_RO_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USERNAME"),
            password=values.get("DB_PASSWORD"),
            host=f"/{values.get('DB_RO_HOST') or values.get('DB_HOST')}",
            port=str(values.get("DB_PORT")),
            path=f"/{values.get('DB_DATABASE') or ''}",
        )

    class Config:
        env_file = (
            ".env.testing" if os.getenv("PYTHON_ENVIRONNEMENT") == "testing" else ".env"
        )


settings = Settings()
settingsReadOnly = SettingsReadOnly()
