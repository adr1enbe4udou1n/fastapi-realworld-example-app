from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from slugify import slugify

from app.api.deps import (
    CurrentUser,
    OptionalCurrentUser,
    get_articles_service,
)
from app.crud.crud_article import ArticlesRepository
from app.models.article import Article
from app.schemas.articles import (
    MultipleArticlesResponse,
    NewArticleRequest,
    SingleArticleResponse,
    UpdateArticleRequest,
)

router = APIRouter()

max_limit: int = 20


async def _get_article_from_slug(
    slug: str,
    articles: ArticlesRepository,
) -> Article:
    db_article = await articles.get_by_slug(slug=slug)
    if not db_article:
        raise HTTPException(status_code=404, detail="No article found")
    return db_article


@router.get(
    "",
    operation_id="GetArticles",
    summary="Get recent articles globally",
    description="Get most recent articles globally. Use query parameters to filter results. Auth is optional",
    response_model=MultipleArticlesResponse,
)
async def get_list(
    current_user: OptionalCurrentUser,
    limit: int = Query(max_limit, title="Limit number of articles returned (default is 20)"),
    offset: int = Query(0, title="Offset/skip number of articles (default is 0)"),
    author: str = Query(None, title="Filter by author (username)"),
    tag: str = Query(None, title="Filter by tag"),
    favorited: str = Query(None, title="Filter by favorites of a user (username)"),
    articles: ArticlesRepository = Depends(get_articles_service),
) -> MultipleArticlesResponse:
    result, count = await articles.get_list(
        min(limit, max_limit),
        offset,
        author=author,
        favorited=favorited,
        tag=tag,
    )
    return MultipleArticlesResponse(
        articles=[article.schema(current_user) for article in result],
        articles_count=count,
    )


@router.get(
    "/feed",
    operation_id="GetArticlesFeed",
    summary="Get recent articles from users you follow",
    description="Get most recent articles from users you follow. Use query parameters to limit. Auth is required",
    response_model=MultipleArticlesResponse,
)
async def get_feed(
    current_user: CurrentUser,
    limit: int = Query(20, title="Limit number of articles returned (default is 20)"),
    offset: int = Query(0, title="Offset/skip number of articles (default is 0)"),
    articles: ArticlesRepository = Depends(get_articles_service),
) -> MultipleArticlesResponse:
    result, count = await articles.get_feed(min(limit, max_limit), offset, user=current_user)
    return MultipleArticlesResponse(
        articles=[article.schema(current_user) for article in result],
        articles_count=count,
    )


@router.post(
    "",
    operation_id="CreateArticle",
    summary="Create an article",
    description="Create an article. Auth is required",
    response_model=SingleArticleResponse,
)
async def create(
    current_user: CurrentUser,
    new_article: NewArticleRequest = Body(...),
    articles: ArticlesRepository = Depends(get_articles_service),
) -> SingleArticleResponse:
    existing_article = await articles.get_by_slug(slug=slugify(new_article.article.title))
    if existing_article:
        raise HTTPException(status_code=400, detail="Article with this title already exists")

    article = await articles.create(obj_in=new_article.article, author=current_user)
    return SingleArticleResponse(article=article.schema(current_user))


@router.get(
    "/{slug}",
    operation_id="GetArticle",
    summary="Get an article",
    description="Get an article. Auth not required",
    response_model=SingleArticleResponse,
)
async def get(
    current_user: OptionalCurrentUser,
    slug: str = Path(..., title="Slug of the article to get"),
    articles: ArticlesRepository = Depends(get_articles_service),
) -> SingleArticleResponse:
    article = await _get_article_from_slug(slug, articles)
    return SingleArticleResponse(article=article.schema(current_user))


@router.put(
    "/{slug}",
    operation_id="UpdateArticle",
    summary="Update an article",
    description="Update an article. Auth is required",
    response_model=SingleArticleResponse,
)
async def update(
    current_user: CurrentUser,
    slug: str = Path(..., title="Slug of the article to update"),
    update_article: UpdateArticleRequest = Body(...),
    articles: ArticlesRepository = Depends(get_articles_service),
) -> SingleArticleResponse:
    article = await _get_article_from_slug(slug, articles)

    if article.author != current_user:
        raise HTTPException(status_code=400, detail="You are not the author of this article")
    article = await articles.update(db_obj=article, obj_in=update_article.article)
    return SingleArticleResponse(article=article.schema(current_user))


@router.delete(
    "/{slug}",
    operation_id="DeleteArticle",
    summary="Delete an article",
    description="Delete an article. Auth is required",
)
async def delete(
    current_user: CurrentUser,
    slug: str = Path(..., title="Slug of the article to delete"),
    articles: ArticlesRepository = Depends(get_articles_service),
) -> None:
    article = await _get_article_from_slug(slug, articles)

    if article.author != current_user:
        raise HTTPException(status_code=400, detail="You are not the author of this article")
    await articles.delete(db_obj=article)
