from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.article import Article
from app.schemas.articles import (MultipleArticlesResponse,
                                  SingleArticleResponse)

router = APIRouter()


@router.get(
    "",
    summary="Get recent articles globally",
    description="Get most recent articles globally. Use query parameters to filter results. Auth is optional",
    response_model=MultipleArticlesResponse,
)
def get_list(
    db: Session = Depends(get_db),
    limit: int = Query(..., title="Limit number of articles returned (default is 20)"),
    offset: int = Query(..., title="Offset/skip number of articles (default is 0)"),
    author: str = Path(..., title="Filter by author (username)"),
    favorited: str = Path(..., title="Filter by favorites of a user (username)"),
    tag: str = Path(..., title="Filter by tag"),
) -> MultipleArticlesResponse:
    articles = map(lambda a: a, db.query(Article).order_by(desc(Article.id)).all())
    return MultipleArticlesResponse(
        articles=list(articles), articles_count=len(articles)
    )


@router.get(
    "/feed",
    summary="Get recent articles from users you follow",
    description="Get most recent articles from users you follow. Use query parameters to limit. Auth is required",
    response_model=MultipleArticlesResponse,
)
def get_feed(
    db: Session = Depends(get_db),
    limit: int = Query(..., title="Limit number of articles returned (default is 20)"),
    offset: int = Query(..., title="Offset/skip number of articles (default is 0)"),
) -> MultipleArticlesResponse:
    articles = map(lambda a: a, db.query(Article).order_by(desc(Article.id)).all())
    return MultipleArticlesResponse(
        articles=list(articles), articles_count=len(articles)
    )


@router.post(
    "",
    summary="Create an article",
    description="Create an article. Auth is required",
    response_model=MultipleArticlesResponse,
)
def create(
    db: Session = Depends(get_db),
) -> SingleArticleResponse:
    article = db.query(Article).first()
    return SingleArticleResponse(article=article)


@router.get(
    "/{slug}",
    summary="Get an article",
    description="Get an article. Auth not required",
    response_model=MultipleArticlesResponse,
)
def update(
    db: Session = Depends(get_db),
    slug: str = Path(..., title="Slug of the article to get"),
) -> SingleArticleResponse:
    article = db.query(Article).first()
    return SingleArticleResponse(article=article)


@router.put(
    "/{slug}",
    summary="Update an article",
    description="Update an article. Auth is required",
    response_model=MultipleArticlesResponse,
)
def update(
    db: Session = Depends(get_db),
    slug: str = Path(..., title="Slug of the article to update"),
) -> SingleArticleResponse:
    article = db.query(Article).first()
    return SingleArticleResponse(article=article)


@router.delete(
    "/{slug}",
    summary="Delete an article",
    description="Delete an article. Auth is required",
    response_model=MultipleArticlesResponse,
)
def delete(
    db: Session = Depends(get_db),
    slug: str = Path(..., title="Slug of the article to delete"),
) -> SingleArticleResponse:
    article = db.query(Article).first()
    return SingleArticleResponse(article=article)
