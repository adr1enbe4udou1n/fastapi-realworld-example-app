from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, get_optional_current_user
from app.models.comment import Comment
from app.schemas.comments import MultipleCommentsResponse, SingleCommentResponse
from app.models.user import User

router = APIRouter()


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
    comment_id: int = Path(..., title="ID of the comment you want to delete"),
) -> SingleCommentResponse:
    comment = db.query(Comment).first()
    return SingleCommentResponse(comment=comment)
