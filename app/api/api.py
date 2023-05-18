from fastapi import APIRouter

from app.api.routes import articles, auth, comments, favorites, profiles, tags, user

router = APIRouter()

router.include_router(
    articles.router,
    prefix="/articles",
    tags=["Articles"],
)
router.include_router(
    comments.router,
    prefix="/articles/{slug}/comments",
    tags=["Comments"],
)
router.include_router(
    favorites.router,
    prefix="/articles/{slug}/favorite",
    tags=["Favorites"],
)
router.include_router(
    profiles.router,
    prefix="/profiles/{username}",
    tags=["Profile"],
)
router.include_router(
    tags.router,
    prefix="/tags",
    tags=["Tags"],
)
router.include_router(auth.router, prefix="/users", tags=["User and Authentication"])
router.include_router(
    user.router,
    prefix="/user",
    tags=["User and Authentication"],
)
