from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.api import router
from app.core.config import settings

app = FastAPI(debug=settings.DEBUG)

app.include_router(
    router,
    prefix="/api",
)


app.openapi_schema = get_openapi(
    title="Conduit API",
    version="1.0.0",
    description="Conduit API",
    contact={"name": "RealWorld - Website", "url": "https://realworld.io/"},
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    routes=router.routes,
    servers=[{"url": "/api"}],
)
