from fastapi import FastAPI
from fastapi.routing import APIRouter

from fastapi.openapi.utils import get_openapi

from app.config import DEBUG

from .routers import user, auth

app = FastAPI(debug=DEBUG)

router = APIRouter()

router.include_router(auth.router)
router.include_router(user.router)

app.include_router(
    router,
    prefix="/api",
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Conduit API",
        version="1.0.0",
        description="Conduit API",
        contact={"name": "RealWorld - Website",
                 "url": "https://realworld.io/"},
        license_info={"name": "MIT License",
                      "url": "https://opensource.org/licenses/MIT"},
        routes=router.routes,
        servers=[{"url": "/api"}],
        tags=[
            {"name": "Articles"},
            {"name": "Favorites"},
            {"name": "Profile"},
            {"name": "Tags"},
            {"name": "User and Authentication"},
        ]
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
