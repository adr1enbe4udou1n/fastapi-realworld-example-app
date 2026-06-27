from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import router
from app.core.config import settings

app = FastAPI(debug=settings.DEBUG, docs_url=None, openapi_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = FastAPI(
    title="Conduit API",
    version="1.0.0",
    description="Conduit API",
    contact={"name": "RealWorld - Website", "url": "https://realworld.io/"},
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[{"url": "/api"}],
    docs_url="/",
    openapi_url="/docs.json",
    redoc_url=None,
)
api.include_router(router)

app.mount("/api", api)
