from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comments import NewComment


class CommentsRepository:
    def get(self, db: Session, id: Any) -> Optional[Comment]:
        return db.query(Comment).filter(Comment.id == id).first()

    def create(self, db: Session, *, obj_in: NewComment) -> Comment:
        db_obj = Comment()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, db_obj: Comment) -> None:
        db.delete(db_obj)
        db.commit()
        return db_obj


comments = CommentsRepository()
