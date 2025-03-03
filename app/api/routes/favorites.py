from fastapi import APIRouter, HTTPException, Path

from app.api.deps import CurrentUser
from app.crud.crud_article import articles
from app.models.article import Article
from app.schemas.articles import SingleArticleResponse

router = APIRouter()


async def _get_article_from_slug(
    slug: str,
) -> Article:
    db_article = await articles.get_by_slug(slug=slug)
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
async def favorite(
    current_user: CurrentUser,
    slug: str = Path(..., title="Slug of the article that you want to favorite"),
) -> SingleArticleResponse:
    article = await _get_article_from_slug(slug)
    await articles.favorite(db_obj=article, user=current_user)
    return SingleArticleResponse(article=article.schema(current_user))


@router.delete(
    "",
    operation_id="DeleteArticleFavorite",
    summary="Unfavorite an article",
    description="Unfavorite an article. Auth is required",
    response_model=SingleArticleResponse,
)
async def unfavorite(
    current_user: CurrentUser,
    slug: str = Path(..., title="Slug of the article that you want to unfavorite"),
) -> SingleArticleResponse:
    article = await _get_article_from_slug(slug)
    await articles.favorite(db_obj=article, user=current_user, favorite=False)
    return SingleArticleResponse(article=article.schema(current_user))
