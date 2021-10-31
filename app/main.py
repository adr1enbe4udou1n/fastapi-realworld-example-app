from fastapi import FastAPI
from fastapi.routing import APIRouter

from app.config import DEBUG

from .routers import users, auth

app = FastAPI(debug=DEBUG)

router = APIRouter()

router.include_router(users.router)
router.include_router(auth.router)

app.include_router(
    router,
    prefix="/api",
)
