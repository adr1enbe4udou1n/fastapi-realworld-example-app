import os
from collections.abc import Generator

import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Transaction
from sqlalchemy.orm import Session, sessionmaker

os.environ["PYTHON_ENVIRONNEMENT"] = "testing"

from app.api.deps import _get_db, _get_db_ro
from app.core.config import settings
from app.core.security import create_access_token
from app.db.base_class import Base
from app.main import app
from app.models.article import Article
from app.models.user import User

engine = create_engine(settings.DATABASE_URL.__str__(), pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db() -> Generator:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    nested = connection.begin_nested()

    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session: Session, transaction: Transaction) -> None:
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db: Session) -> Generator:
    def override_get_db() -> Generator:
        yield db

    app.dependency_overrides[_get_db] = override_get_db
    app.dependency_overrides[_get_db_ro] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[_get_db]
    del app.dependency_overrides[_get_db_ro]


def create_john_user(db: Session) -> User:
    db_obj = User(
        name="John Doe",
        email="john.doe@example.com",
        bio="John Bio",
        image="https://randomuser.me/api/portraits/men/1.jpg",
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_jane_user(db: Session) -> User:
    db_obj = User(
        name="Jane Doe",
        email="jane.doe@example.com",
        bio="Jane Bio",
        image="https://randomuser.me/api/portraits/women/1.jpg",
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def acting_as_user(user: User, client: TestClient) -> User:
    token = create_access_token(user.id)

    client.headers["Authorization"] = f"Bearer {token}"
    return user


def acting_as_john(db: Session, client: TestClient) -> User:
    user = create_john_user(db)
    return acting_as_user(user, client)


def acting_as_jane(db: Session, client: TestClient) -> User:
    user = create_jane_user(db)
    return acting_as_user(user, client)


def generate_article(author: User, slug: str = "test-title") -> Article:
    return Article(
        title="Test Title",
        description="Test Description",
        body="Test Body",
        slug=slug,
        author=author,
    )
