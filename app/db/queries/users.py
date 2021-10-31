from sqlalchemy.orm import Session
from .. import models
from app.schemas import users


def get_user(db: Session, user_id: int):

    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: users.NewUser):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        name=user.username,
        email=user.email,
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
