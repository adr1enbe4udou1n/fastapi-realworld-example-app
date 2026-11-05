"""
conftest.py — Configuración base de la suite de pruebas automatizadas
======================================================================
Proyecto : FastAPI RealWorld Example App (Conduit)
Suite    : 26 casos automatizados (CP-AUTH-A-001 … CP-TAG-A-002)
Entorno  : pytest + pytest-asyncio + FastAPI TestClient
BD       : PostgreSQL de test (puerto 5434, ver .env.testing)
"""

import asyncio
import os
import sys
from collections.abc import AsyncGenerator

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Forzar entorno de testing ANTES de importar cualquier módulo de la app
os.environ["PYTHON_ENVIRONNEMENT"] = "testing"

from app.core.config import settings  # noqa: E402
from app.core.security import create_access_token, get_password_hash  # noqa: E402
from app.db.base_class import Base  # noqa: E402
from app.main import app  # noqa: E402
from app.models.article import Article, article_favorite, article_tag  # noqa: E402
from app.models.comment import Comment  # noqa: E402
from app.models.tag import Tag  # noqa: E402
from app.models.user import User, follower_user  # noqa: E402

# ---------------------------------------------------------------------------
# Motor de BD de pruebas
# ---------------------------------------------------------------------------
engine = create_async_engine(settings.DATABASE_URL.__str__(), pool_pre_ping=True)
TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True, expire_on_commit=False
)


async def _init_db() -> None:
    """Crea todas las tablas en la BD de test al iniciar la sesión."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(_init_db())


# ---------------------------------------------------------------------------
# Fixtures principales
# ---------------------------------------------------------------------------


@pytest.fixture()
async def db() -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture de sesión de BD.
    Limpia TODAS las tablas después de cada test usando una sesión limpia
    para garantizar aislamiento total y evitar MissingGreenlet.
    """
    async with TestingSessionLocal() as session:
        yield session

    # Teardown en una sesión separada para no arrastrar IdentityMap
    async with TestingSessionLocal() as clean_session:
        await clean_session.execute(delete(follower_user))
        await clean_session.execute(delete(article_tag))
        await clean_session.execute(delete(article_favorite))
        await clean_session.execute(delete(Comment))
        await clean_session.execute(delete(Article))
        await clean_session.execute(delete(Tag))
        await clean_session.execute(delete(User))
        await clean_session.commit()


@pytest.fixture()
def client() -> TestClient:
    """
    Cliente HTTP síncrono de FastAPI.
    Cada test recibe un cliente fresco.
    """
    return TestClient(app, raise_server_exceptions=True)


# ---------------------------------------------------------------------------
# Helpers de creación de usuarios
# ---------------------------------------------------------------------------


async def create_user(
    db: AsyncSession,
    *,
    username: str,
    email: str,
    password: str = "password123",
) -> User:
    """Crea un usuario en la BD con la contraseña hasheada y cierra la sesión."""
    user = User(
        name=username,
        email=email,
        password=get_password_hash(password),
        bio=f"Bio de {username}",
        image=None,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user, ["followers"])
    await db.close()
    return user


async def create_john(db: AsyncSession) -> User:
    return await create_user(db, username="John Doe", email="john@test.com")


async def create_jane(db: AsyncSession) -> User:
    return await create_user(db, username="Jane Doe", email="jane@test.com")


# ---------------------------------------------------------------------------
# Helper de autenticación
# ---------------------------------------------------------------------------


def auth_header(user: User) -> dict[str, str]:
    """Devuelve el header Authorization con el token JWT del usuario."""
    token = create_access_token(user.id)
    return {"Authorization": f"Bearer {token}"}


def acting_as_user(user: User, client: TestClient) -> User:
    token = create_access_token(user.id)
    client.headers["Authorization"] = f"Bearer {token}"
    return user


# ---------------------------------------------------------------------------
# Helper de creación de artículos
# ---------------------------------------------------------------------------


async def create_article(
    db: AsyncSession,
    *,
    author: User,
    title: str = "Test Title",
    description: str = "Test Description",
    body: str = "Test Body",
    slug: str = "test-title",
    tags: list[str] | None = None,
) -> Article:
    """
    Crea un artículo en la BD directamente (sin pasar por la API).
    """
    article = Article(
        title=title,
        description=description,
        body=body,
        slug=slug,
        author_id=author.id,
    )

    if tags:
        for tag_name in tags:
            result = await db.execute(select(Tag).where(Tag.name == tag_name))
            tag_obj = result.scalar_one_or_none()
            if not tag_obj:
                tag_obj = Tag(name=tag_name)
                db.add(tag_obj)
                await db.flush()
            article.tags.append(tag_obj)

    db.add(article)
    await db.commit()
    await db.refresh(article)
    await db.close()
    return article
