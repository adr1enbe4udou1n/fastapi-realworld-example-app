from typing import Any, List, Optional

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.expression import desc

from app.models.article import Article
from app.models.comment import Comment
from app.models.user import User
from app.schemas.comments import NewComment


class CommentsRepository:
    def get(self, db: Session, id: Any) -> Optional[Comment]:
        return db.query(Comment).filter_by(id=id).first()

    def get_list(self, db: Session, article: Article) -> List[Comment]:
        return (
            db.query(Comment)
            .options(joinedload(Comment.author))
            .filter_by(article=article)
            .order_by(desc(Comment.id))
            .all()
        )

    def create(
        self, db: Session, *, obj_in: NewComment, article: Article, author: User
    ) -> Comment:
        db_obj = Comment(
            article=article,
            author=author,
            body=obj_in.body,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, db_obj: Comment) -> None:
        db.delete(db_obj)
        db.commit()


comments = CommentsRepository()
