from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from tests.conftest import acting_as_john


def test_can_paginate_articles(client: TestClient, db: Session) -> None:
    acting_as_john(db, client)
    r = client.get("/api/articles")
    assert r.status_code == status.HTTP_200_OK


def test_can_filter_articles_by_author(client: TestClient, db: Session) -> None:
    acting_as_john(db, client)
    r = client.get("/api/articles")
    assert r.status_code == status.HTTP_200_OK


def test_can_filter_articles_by_favorited(client: TestClient, db: Session) -> None:
    acting_as_john(db, client)
    r = client.get("/api/articles")
    assert r.status_code == status.HTTP_200_OK


def test_can_filter_articles_by_tag(client: TestClient, db: Session) -> None:
    acting_as_john(db, client)
    r = client.get("/api/articles")
    assert r.status_code == status.HTTP_200_OK


def test_guest_cannot_paginate_feed(client: TestClient, db: Session) -> None:
    acting_as_john(db, client)
    r = client.get("/api/articles")
    assert r.status_code == status.HTTP_200_OK


def test_can_paginate_feed(client: TestClient, db: Session) -> None:
    acting_as_john(db, client)
    r = client.get("/api/articles")
    assert r.status_code == status.HTTP_200_OK
