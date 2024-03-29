from fastapi import APIRouter, HTTPException, Path
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, DatabaseSession
from app.crud.crud_article import articles
from app.models.article import Article
from app.schemas.articles import SingleArticleResponse

router = APIRouter()


def _get_article_from_slug(
    db: Session,
    slug: str,
) -> Article:
    db_article = articles.get_by_slug(db, slug=slug)
    if not db_article:
        raise HTTPException(status_code=404, detail="No article found")
    return db_article


@router.post(
    "",
    operation_id="CreateArticleFavorite",
    summary="Favorite an article",
    description="Favorite an article. Auth is required",
    response_model=SingleArticleResponse,
)
def favorite(
    db: DatabaseSession,
    current_user: CurrentUser,
    slug: str = Path(..., title="Slug of the article that you want to favorite"),
) -> SingleArticleResponse:
    article = _get_article_from_slug(db, slug)
    articles.favorite(db, db_obj=article, user=current_user)
    return SingleArticleResponse(article=article.schema(current_user))


@router.delete(
    "",
    operation_id="DeleteArticleFavorite",
    summary="Unfavorite an article",
    description="Unfavorite an article. Auth is required",
    response_model=SingleArticleResponse,
)
def unfavorite(
    db: DatabaseSession,
    current_user: CurrentUser,
    slug: str = Path(..., title="Slug of the article that you want to unfavorite"),
) -> SingleArticleResponse:
    article = _get_article_from_slug(db, slug)
    articles.favorite(db, db_obj=article, user=current_user, favorite=False)
    return SingleArticleResponse(article=article.schema(current_user))
