from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from tests.conftest import acting_as_john


def test_guest_cannot_delete_comment(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.delete("/api/articles/test-title/comments/1")
    assert r.status_code == status.HTTP_200_OK


def test_cannot_delete_comment_with_non_existent_article(
    client: TestClient, db: Session
) -> None:
    acting_as_john(db)
    r = client.delete("/api/articles/test-title/comments/1")
    assert r.status_code == status.HTTP_200_OK


def test_cannot_delete_non_existent_comment(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.delete("/api/articles/test-title/comments/1")
    assert r.status_code == status.HTTP_200_OK


def test_cannot_delete_comment_of_other_author(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.delete("/api/articles/test-title/comments/1")
    assert r.status_code == status.HTTP_200_OK


def test_cannot_delete_comment_with_bad_article(
    client: TestClient, db: Session
) -> None:
    acting_as_john(db)
    r = client.delete("/api/articles/test-title/comments/1")
    assert r.status_code == status.HTTP_200_OK


def test_can_delete_all_comments_of_own_article(
    client: TestClient, db: Session
) -> None:
    acting_as_john(db)
    r = client.delete("/api/articles/test-title/comments/1")
    assert r.status_code == status.HTTP_200_OK


def test_can_delete_own_comment(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.delete("/api/articles/test-title/comments/1")
    assert r.status_code == status.HTTP_200_OK
