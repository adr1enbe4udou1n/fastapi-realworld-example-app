from typing import Any, Dict, Optional
from pydantic.networks import PostgresDsn
from starlette.datastructures import Secret

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    API_PREFIX = "/api"
    DEBUG: bool = False
    JWT_SECRET_KEY: str = None
    JWT_EXPIRE: int = 60 * 24 * 8

    DB_HOST: str
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DATABASE_URL: Optional[PostgresDsn] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USERNAME"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            path=f"/{values.get('DB_DATABASE') or ''}",
        )

    class Config:
        env_file = ".env"


settings = Settings()
