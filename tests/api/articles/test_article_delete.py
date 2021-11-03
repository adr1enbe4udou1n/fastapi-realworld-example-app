from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.conftest import acting_as_john
from starlette import status


def test_guest_cannot_delete_article(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.delete("/api/articles/test-title")
    assert r.status_code == status.HTTP_200_OK


def test_cannot_delete_non_existent_article(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.delete("/api/articles/test-title")
    assert r.status_code == status.HTTP_200_OK


def test_cannot_delete_article_of_other_author(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.delete("/api/articles/test-title")
    assert r.status_code == status.HTTP_200_OK


def test_can_delete_own_article_with_all_comments(
    client: TestClient, db: Session
) -> None:
    acting_as_john(db)
    r = client.delete("/api/articles/test-title")
    assert r.status_code == status.HTTP_200_OK
