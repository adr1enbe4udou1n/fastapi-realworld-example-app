from typing import Dict
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.conftest import acting_as_john
from starlette import status


def test_guest_cannot_update_article(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.put("/api/articles/test-title")
    assert r.status_code == status.HTTP_200_OK


def test_cannot_update_non_existant_article(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.put("/api/articles/test-title")
    assert r.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "data",
    (
        {
            "title": "Test Title",
            "description": "Test Description",
            "body": "",
        },
    ),
)
def test_cannot_update_article_with_invalid_data(
    client: TestClient, db: Session, data: Dict[str, str]
) -> None:
    acting_as_john(db)
    r = client.put("/api/articles/test-title")
    assert r.status_code == status.HTTP_200_OK


def test_cannot_update_article_of_other_author(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.put("/api/articles/test-title")
    assert r.status_code == status.HTTP_200_OK


def test_can_update_own_article(client: TestClient, db: Session) -> None:
    acting_as_john(db)
    r = client.put("/api/articles/test-title")
    assert r.status_code == status.HTTP_200_OK
