from starlette.config import Config
from starlette.datastructures import Secret

from databases import DatabaseURL

API_PREFIX = "/api"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL)

SECRET_KEY: Secret = config("JWT_SECRET_KEY", cast=Secret)
