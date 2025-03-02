from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.users import NewUser, UpdateUser


class UsersRepository:
    def get(self, db: Session, id: int) -> User | None:
        return db.query(User).filter_by(id=id).first()

    def get_by_name(self, db: Session, *, name: str) -> User | None:
        return db.query(User).filter_by(name=name).first()

    def get_by_email(self, db: Session, *, email: str) -> User | None:
        return db.query(User).filter_by(email=email).first()

    def create(self, db: Session, *, obj_in: NewUser) -> User:
        db_obj = User(
            name=obj_in.username,
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UpdateUser) -> User:
        db_obj.name = obj_in.username or db_obj.name
        db_obj.email = obj_in.email or db_obj.email
        db_obj.bio = obj_in.bio or db_obj.bio
        db_obj.image = obj_in.image or db_obj.image

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> User | None:
        user = self.get_by_email(db, email=email)
        if not user or not user.password:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def follow(self, db: Session, *, db_obj: User, follower: User, follow: bool = True) -> None:
        if follow:
            db_obj.followers.append(follower)
        else:
            db_obj.followers.remove(follower)

        db.merge(db_obj)
        db.commit()


users = UsersRepository()
