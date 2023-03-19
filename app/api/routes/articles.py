from fastapi import APIRouter, Body, HTTPException, Path, Query
from slugify import slugify
from sqlalchemy.orm import Session

from app.api.deps import (
    CurrentUser,
    DatabaseRoSession,
    DatabaseSession,
    OptionalCurrentUser,
)
from app.crud.crud_article import articles
from app.models.article import Article
from app.schemas.articles import (
    MultipleArticlesResponse,
    NewArticleRequest,
    SingleArticleResponse,
    UpdateArticleRequest,
)

router = APIRouter()

max_limit: int = 20


def _get_article_from_slug(
    db: Session,
    slug: str,
) -> Article:
    db_article = articles.get_by_slug(db, slug=slug)
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
def get_list(
    db: DatabaseRoSession,
    current_user: OptionalCurrentUser,
    limit: int = Query(
        max_limit, title="Limit number of articles returned (default is 20)"
    ),
    offset: int = Query(0, title="Offset/skip number of articles (default is 0)"),
    author: str = Query(None, title="Filter by author (username)"),
    tag: str = Query(None, title="Filter by tag"),
    favorited: str = Query(None, title="Filter by favorites of a user (username)"),
) -> MultipleArticlesResponse:
    result, count = articles.get_list(
        db,
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
def get_feed(
    db: DatabaseRoSession,
    current_user: CurrentUser,
    limit: int = Query(20, title="Limit number of articles returned (default is 20)"),
    offset: int = Query(0, title="Offset/skip number of articles (default is 0)"),
) -> MultipleArticlesResponse:
    result, count = articles.get_feed(
        db, min(limit, max_limit), offset, user=current_user
    )
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
def create(
    db: DatabaseSession,
    current_user: CurrentUser,
    new_article: NewArticleRequest = Body(...),
) -> SingleArticleResponse:
    existing_article = articles.get_by_slug(db, slug=slugify(new_article.article.title))
    if existing_article:
        raise HTTPException(
            status_code=400, detail="Article with this title already exists"
        )

    article = articles.create(db, obj_in=new_article.article, author=current_user)
    return SingleArticleResponse(article=article.schema(current_user))


@router.get(
    "/{slug}",
    operation_id="GetArticle",
    summary="Get an article",
    description="Get an article. Auth not required",
    response_model=SingleArticleResponse,
)
def get(
    db: DatabaseRoSession,
    current_user: OptionalCurrentUser,
    slug: str = Path(..., title="Slug of the article to get"),
) -> SingleArticleResponse:
    article = _get_article_from_slug(db, slug)
    return SingleArticleResponse(article=article.schema(current_user))


@router.put(
    "/{slug}",
    operation_id="UpdateArticle",
    summary="Update an article",
    description="Update an article. Auth is required",
    response_model=SingleArticleResponse,
)
def update(
    db: DatabaseSession,
    current_user: CurrentUser,
    slug: str = Path(..., title="Slug of the article to update"),
    update_article: UpdateArticleRequest = Body(...),
) -> SingleArticleResponse:
    article = _get_article_from_slug(db, slug)

    if article.author != current_user:
        raise HTTPException(
            status_code=400, detail="You are not the author of this article"
        )
    article = articles.update(db, db_obj=article, obj_in=update_article.article)
    return SingleArticleResponse(article=article.schema(current_user))


@router.delete(
    "/{slug}",
    operation_id="DeleteArticle",
    summary="Delete an article",
    description="Delete an article. Auth is required",
)
def delete(
    db: DatabaseSession,
    current_user: CurrentUser,
    slug: str = Path(..., title="Slug of the article to delete"),
) -> None:
    article = _get_article_from_slug(db, slug)

    if article.author != current_user:
        raise HTTPException(
            status_code=400, detail="You are not the author of this article"
        )
    articles.delete(db, db_obj=article)
