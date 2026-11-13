import asyncio
import sys
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import router
from app.core.config import settings
from app.db.base_class import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    debug=settings.DEBUG,
    docs_url=None,
    openapi_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

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
