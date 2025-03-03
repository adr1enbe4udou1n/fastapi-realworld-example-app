import asyncio
import os
from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models.comment import Comment
from app.models.tag import Tag

os.environ["PYTHON_ENVIRONNEMENT"] = "testing"

from app.core.config import settings
from app.core.security import create_access_token
from app.db.base_class import Base
from app.main import app
from app.models.article import Article
from app.models.user import User

engine = create_async_engine(settings.DATABASE_URL.__str__(), pool_pre_ping=True)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_db())


@pytest.fixture()
async def db() -> AsyncGenerator:
    async with TestingSessionLocal() as db:
        yield db

        await db.execute(delete(Tag))
        await db.execute(delete(Comment))
        await db.execute(delete(Article))
        await db.execute(delete(User))
        await db.commit()


@pytest.fixture()
async def client() -> AsyncGenerator:
    yield TestClient(app)


async def create_john_user(db: AsyncSession) -> User:
    db_obj = User(
        name="John Doe",
        email="john.doe@example.com",
        bio="John Bio",
        image="https://randomuser.me/api/portraits/men/1.jpg",
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj, ["followers"])
    await db.close()
    return db_obj


async def create_jane_user(db: AsyncSession) -> User:
    db_obj = User(
        name="Jane Doe",
        email="jane.doe@example.com",
        bio="Jane Bio",
        image="https://randomuser.me/api/portraits/women/1.jpg",
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj, ["followers"])
    await db.close()
    return db_obj


def acting_as_user(user: User, client: TestClient) -> User:
    token = create_access_token(user.id)

    client.headers["Authorization"] = f"Bearer {token}"
    return user


async def acting_as_john(db: AsyncSession, client: TestClient) -> User:
    user = await create_john_user(db)
    return acting_as_user(user, client)


async def acting_as_jane(db: AsyncSession, client: TestClient) -> User:
    user = await create_jane_user(db)
    return acting_as_user(user, client)


def generate_article(author: User, slug: str = "test-title") -> Article:
    return Article(
        title="Test Title",
        description="Test Description",
        body="Test Body",
        slug=slug,
        author=author,
    )
