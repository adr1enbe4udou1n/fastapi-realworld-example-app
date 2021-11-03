from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.article import Article
from app.schemas.articles import SingleArticleResponse

router = APIRouter()


@router.post(
    "",
    summary="Favorite an article",
    description="Favorite an article. Auth is required",
    response_model=SingleArticleResponse,
)
def favorite(
    db: Session = Depends(get_db),
    slug: str = Path(..., title="Slug of the article that you want to favorite"),
) -> SingleArticleResponse:
    article = db.query(Article).first()
    return SingleArticleResponse(article=article)


@router.delete(
    "",
    summary="Unfavorite an article",
    description="Unfavorite an article. Auth is required",
    response_model=SingleArticleResponse,
)
def unfavorite(
    db: Session = Depends(get_db),
    slug: str = Path(..., title="Slug of the article that you want to unfavorite"),
) -> SingleArticleResponse:
    article = db.query(Article).first()
    return SingleArticleResponse(article=article)
