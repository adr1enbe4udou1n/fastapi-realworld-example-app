from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, get_optional_current_user
from app.crud.crud_article import articles
from app.crud.crud_comment import comments
from app.models.comment import Comment
from app.models.user import User
from app.schemas.comments import (MultipleCommentsResponse, NewCommentRequest,
                                  SingleCommentResponse)

router = APIRouter()


def _get_article_from_slug(
    db: Session,
    slug: str,
) -> User:
    db_article = articles.get_by_slug(db, slug=slug)
    if not db_article:
        raise HTTPException(status_code=404, detail="No article found")
    return db_article


def _get_comment_from_id(
    db: Session,
    id: str,
) -> User:
    db_comment = comments.get(db, id=id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="No comment found")
    return db_comment


@router.get(
    "",
    summary="Get comments for an article",
    description="Get the comments for an article. Auth is optional",
    response_model=MultipleCommentsResponse,
)
def get_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_optional_current_user),
    slug: str = Path(
        ..., title="Slug of the article that you want to get comments for"
    ),
) -> MultipleCommentsResponse:
    comments = map(lambda c: c, db.query(Comment).all())
    return MultipleCommentsResponse(comments=list(comments))


@router.post(
    "",
    summary="Create a comment for an article",
    description="Create a comment for an article. Auth is required",
    response_model=SingleCommentResponse,
)
def create(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    slug: str = Path(
        ..., title="Slug of the article that you want to create a comment for"
    ),
    new_comment: NewCommentRequest = Body(...),
) -> SingleCommentResponse:
    comment = db.query(Comment).first()
    return SingleCommentResponse(comment=comment)


@router.delete(
    "{commentId}",
    summary="Delete a comment for an article",
    description="Delete a comment for an article. Auth is required",
    response_model=SingleCommentResponse,
)
def delete(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    slug: str = Path(
        ..., title="Slug of the article that you want to delete a comment for"
    ),
    comment_id: int = Path(
        ..., title="ID of the comment you want to delete", alias="commentId"
    ),
) -> SingleCommentResponse:
    _get_article_from_slug(slug)
    comment = _get_comment_from_id(comment_id)
    return SingleCommentResponse(comment=comment)
