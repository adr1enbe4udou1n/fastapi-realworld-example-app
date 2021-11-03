from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.conftest import acting_as_john
from starlette import status


def test_guest_cannot_favorite_article(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.post("/api/articles/test-title/favorite")
    assert r.status_code == status.HTTP_200_OK


def test_cannot_favorite_non_existent_article(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.post("/api/articles/test-title/favorite")
    assert r.status_code == status.HTTP_200_OK


def test_can_favorite_article(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.post("/api/articles/test-title/favorite")
    assert r.status_code == status.HTTP_200_OK


def test_can_unfavorite_article(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.delete("/api/articles/test-title/favorite")
    assert r.status_code == status.HTTP_200_OK
