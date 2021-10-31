from starlette.config import Config
from starlette.datastructures import Secret

API_PREFIX = "/api"

JWT_TOKEN_PREFIX = "Token"
VERSION = "0.0.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

# DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL)

SECRET_KEY: Secret = config("JWT_SECRET_KEY", cast=Secret)
