import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app.models.comment import Comment
from tests.conftest import acting_as_john, generate_article


def test_guest_cannot_create_comment(client: TestClient) -> None:
    r = client.post("/api/articles/test-title/comments")
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_cannot_create_comment_to_non_existent_article(client: TestClient, db: Session) -> None:
    acting_as_john(db, client)
    r = client.post("/api/articles/test-title/comments", json={"comment": {"body": "Test Comment"}})
    assert r.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "data",
    (
        {
            "body": "",
        },
    ),
)
def test_cannot_create_comment_with_invalid_data(client: TestClient, db: Session, data: dict[str, str]) -> None:
    john = acting_as_john(db, client)

    db_obj = generate_article(john)
    db.add(db_obj)
    db.commit()

    r = client.post("/api/articles/test-title/comments", json={"comment": data})
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_can_create_comment(client: TestClient, db: Session) -> None:
    john = acting_as_john(db, client)

    db_obj = generate_article(john)
    db.add(db_obj)
    db.commit()

    r = client.post("/api/articles/test-title/comments", json={"comment": {"body": "Test Comment"}})
    assert r.status_code == status.HTTP_200_OK
    assert r.json()["comment"]["body"] == "Test Comment"
    assert db.query(Comment).filter_by(body="Test Comment").count() == 1
