from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from tests.conftest import acting_as_john


def test_cannot_get_non_existent_article(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.get("/api/articles/test-title")
    assert r.status_code == status.HTTP_200_OK


def test_can_get_article(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.get("/api/articles/test-title")
    assert r.status_code == status.HTTP_200_OK
