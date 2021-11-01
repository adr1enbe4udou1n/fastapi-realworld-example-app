from typing import Generator

import pytest
from fastapi.testclient import TestClient

from alembic.config import Config as AlembicConfig
from alembic.command import upgrade as alembic_upgrade

from app.db.session import SessionLocal
from app.main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    session = SessionLocal()

    alembic_config = AlembicConfig('alembic.ini')
    alembic_upgrade(alembic_config, 'head')
    return session


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
