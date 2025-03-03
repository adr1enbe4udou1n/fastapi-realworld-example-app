from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.security import get_password_hash, verify_password
from app.db.session import SessionLocal, SessionLocalRo
from app.models.user import User
from app.schemas.users import NewUser, UpdateUser


class UsersRepository:
    async def get(self, id: int) -> User | None:
        async with SessionLocalRo() as db:
            return await db.scalar(select(User).filter_by(id=id))

    async def get_by_name(self, *, name: str) -> User | None:
        async with SessionLocalRo() as db:
            return await db.scalar(select(User).options(joinedload(User.followers)).filter_by(name=name))

    async def get_by_email(self, *, email: str) -> User | None:
        async with SessionLocalRo() as db:
            return await db.scalar(select(User).filter_by(email=email))

    async def create(self, *, obj_in: NewUser) -> User:
        async with SessionLocal() as db:
            db_obj = User(
                name=obj_in.username,
                email=obj_in.email,
                password=get_password_hash(obj_in.password),
            )
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj

    async def update(self, *, db_obj: User, obj_in: UpdateUser) -> User:
        async with SessionLocal() as db:
            db_obj.name = obj_in.username or db_obj.name
            db_obj.email = obj_in.email or db_obj.email
            db_obj.bio = obj_in.bio or db_obj.bio
            db_obj.image = obj_in.image or db_obj.image

            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj

    async def authenticate(self, *, email: str, password: str) -> User | None:
        user = await self.get_by_email(email=email)
        if not user or not user.password:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def follow(self, *, db_obj: User, follower: User, follow: bool = True) -> None:
        async with SessionLocal() as db:
            if follow:
                db_obj.followers.append(follower)
            else:
                db_obj.followers.remove(follower)

            await db.commit()
            await db.refresh(db_obj)


users = UsersRepository()
