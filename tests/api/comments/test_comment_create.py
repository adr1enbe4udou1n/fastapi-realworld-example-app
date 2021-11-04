from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from tests.conftest import acting_as_john


def test_guest_cannot_create_comment(client: TestClient) -> None:
    r = client.post("/api/articles/test-title/comments")
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_cannot_create_comment_to_non_existent_article(
    client: TestClient, db: Session
) -> None:
    acting_as_john(db, client)
    r = client.post(
        "/api/articles/test-title/comments", json={"comment": {"body": "Test Comment"}}
    )
    assert r.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "data",
    (
        {
            "body": "",
        },
    ),
)
def test_cannot_create_comment_with_invalid_data(
    client: TestClient, db: Session, data: Dict[str, str]
) -> None:
    acting_as_john(db, client)
    r = client.post("/api/articles/test-title/comments", json={"comment": data})
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_can_create_comment(client: TestClient, db: Session) -> None:
    acting_as_john(db, client)
    r = client.post("/api/articles/test-title/comments")
    assert r.status_code == status.HTTP_200_OK
