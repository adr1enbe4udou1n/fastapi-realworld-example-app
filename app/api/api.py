from fastapi import APIRouter

from app.api.routes import auth, user

router = APIRouter()

router.include_router(auth.router, prefix="/users", tags=["User and Authentication"])
router.include_router(
    user.router,
    prefix="/user",
    tags=["User and Authentication"],
)
