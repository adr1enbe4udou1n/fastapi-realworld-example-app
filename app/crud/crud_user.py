from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.users import NewUser, UpdateUser


class UsersRepository:
    async def get(self, db: AsyncSession, id: int) -> User | None:
        return await db.scalar(select(User).filter_by(id=id))

    async def get_by_name(self, db: AsyncSession, *, name: str) -> User | None:
        return await db.scalar(select(User).filter_by(name=name))

    async def get_by_email(self, db: AsyncSession, *, email: str) -> User | None:
        return await db.scalar(select(User).filter_by(email=email))

    async def create(self, db: AsyncSession, *, obj_in: NewUser) -> User:
        db_obj = User(
            name=obj_in.username,
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: User, obj_in: UpdateUser) -> User:
        db_obj.name = obj_in.username or db_obj.name
        db_obj.email = obj_in.email or db_obj.email
        db_obj.bio = obj_in.bio or db_obj.bio
        db_obj.image = obj_in.image or db_obj.image

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> User | None:
        user = await self.get_by_email(db, email=email)
        if not user or not user.password:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def follow(self, db: AsyncSession, *, db_obj: User, follower: User, follow: bool = True) -> None:
        if follow:
            (await db_obj.awaitable_attrs.followers).append(follower)
        else:
            (await db_obj.awaitable_attrs.followers).remove(follower)

        await db.merge(db_obj)
        await db.commit()


users = UsersRepository()
