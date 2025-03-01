from fastapi import APIRouter, Body, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    CurrentUser,
    DatabaseRoSession,
    DatabaseSession,
    OptionalCurrentUser,
)
from app.crud.crud_article import articles
from app.crud.crud_comment import comments
from app.models.article import Article
from app.models.comment import Comment
from app.schemas.comments import (
    MultipleCommentsResponse,
    NewCommentRequest,
    SingleCommentResponse,
)

router = APIRouter()


async def _get_article_from_slug(
    db: AsyncSession,
    slug: str,
) -> Article:
    db_article = await articles.get_by_slug(db, slug=slug)
    if not db_article:
        raise HTTPException(status_code=404, detail="No article found")
    return db_article


async def _get_comment_from_id(
    db: AsyncSession,
    id: int,
) -> Comment:
    db_comment = await comments.get(db, id=id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="No comment found")
    return db_comment


@router.get(
    "",
    operation_id="GetArticleComments",
    summary="Get comments for an article",
    description="Get the comments for an article. Auth is optional",
    response_model=MultipleCommentsResponse,
)
async def get_list(
    db: DatabaseRoSession,
    current_user: OptionalCurrentUser,
    slug: str = Path(..., title="Slug of the article that you want to get comments for"),
) -> MultipleCommentsResponse:
    article = await _get_article_from_slug(db, slug)
    return MultipleCommentsResponse(
        comments=[await comment.schema(current_user) for comment in await comments.get_list(db, article=article)]
    )


@router.post(
    "",
    operation_id="CreateArticleComment",
    summary="Create a comment for an article",
    description="Create a comment for an article. Auth is required",
    response_model=SingleCommentResponse,
)
async def create(
    db: DatabaseSession,
    current_user: CurrentUser,
    slug: str = Path(..., title="Slug of the article that you want to create a comment for"),
    new_comment: NewCommentRequest = Body(...),
) -> SingleCommentResponse:
    article = await _get_article_from_slug(db, slug)
    comment = await comments.create(db, obj_in=new_comment.comment, article=article, author=current_user)
    return SingleCommentResponse(comment=await comment.schema(current_user))


@router.delete(
    "/{commentId}",
    operation_id="DeleteArticleComment",
    summary="Delete a comment for an article",
    description="Delete a comment for an article. Auth is required",
)
async def delete(
    db: DatabaseSession,
    current_user: CurrentUser,
    slug: str = Path(..., title="Slug of the article that you want to delete a comment for"),
    comment_id: int = Path(..., title="ID of the comment you want to delete", alias="commentId"),
) -> None:
    article = await _get_article_from_slug(db, slug)
    comment = await _get_comment_from_id(db, comment_id)

    if comment.article != article:
        raise HTTPException(status_code=400, detail="Comment does not belong to this article")

    if comment.author != current_user and article.author != current_user:
        raise HTTPException(status_code=400, detail="Comment does not belong to this user")

    await comments.delete(db, db_obj=comment)
