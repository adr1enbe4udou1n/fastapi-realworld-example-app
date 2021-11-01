from fastapi import FastAPI

from fastapi.openapi.utils import get_openapi

from app.core.config import settings

from app.api.api import router

app = FastAPI(debug=settings.DEBUG)

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
