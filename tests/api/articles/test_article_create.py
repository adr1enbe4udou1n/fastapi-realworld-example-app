from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app.models.tag import Tag
from tests.conftest import acting_as_john, generate_article
from app.models.article import Article


def test_guest_cannot_create_article(client: TestClient) -> None:
    r = client.post("/api/articles")
    assert r.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "data",
    (
        {
            "title": "",
            "description": "Test Description",
            "body": "Test Body",
        },
        {
            "title": "Test Title",
            "description": "",
            "body": "Test Body",
        },
        {
            "title": "Test Title",
            "description": "Test Description",
            "body": "",
        },
    ),
)
def test_cannot_create_article_with_invalid_data(
    client: TestClient, db: Session, data: Dict[str, str]
) -> None:
    acting_as_john(db, client)
    r = client.post("/api/articles", json={"article": data})
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_cannot_create_article_with_same_title(client: TestClient, db: Session) -> None:
    john = acting_as_john(db, client)

    db_obj = generate_article(john)
    db.add(db_obj)
    db.commit()

    r = client.post(
        "/api/articles",
        json={
            "article": {
                "title": "Test Title",
                "description": "Test Description",
                "body": "Test Body",
            }
        },
    )
    assert r.status_code == status.HTTP_400_BAD_REQUEST


def test_can_create_article(client: TestClient, db: Session) -> None:
    db.add(Tag(name="Existing Tag"))
    db.commit()

    acting_as_john(db, client)

    r = client.post(
        "/api/articles",
        json={
            "article": {
                "title": "Test Title",
                "description": "Test Description",
                "body": "Test Body",
                "tagList": ["Tag 1", "Tag 2", "Existing Tag"],
            }
        },
    )
    assert r.status_code == status.HTTP_200_OK
    assert {
        "title": "Test Title",
        "slug": "test-title",
        "description": "Test Description",
        "body": "Test Body",
        "author": {
            "username": "John Doe",
            "bio": "John Bio",
            "image": "https://randomuser.me/api/portraits/men/1.jpg",
            "following": False,
        },
        "tagList": ["Existing Tag", "Tag 1", "Tag 2"],
        "favorited": False,
        "favoritesCount": 0,
    }.items() <= r.json()["article"].items()
    assert db.query(Article).filter_by(slug="test-title").count() == 1
    assert db.query(Tag).count() == 3
