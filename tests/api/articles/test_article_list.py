import pytest
from typing import Generator, List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from tests.conftest import acting_as_john, create_jane_user, create_john_user

from app.models.article import Article
from app.models.tag import Tag


def generate_articles(db: Session) -> None:
    tag1 = Tag(name="Tag 1")
    tag2 = Tag(name="Tag 2")
    tagJohn = Tag(name="Tag 1")
    tagJane = Tag(name="Tag 1")
    db.add_all([tag1, tag2, tagJohn, tagJane])
    db.commit()

    john = create_john_user(db)
    jane = create_jane_user(db)

    jane.followers.append(john)
    db.merge(jane)
    db.commit()

    john_favorited_articles = [
        "jane-article-1",
        "jane-article-2",
        "jane-article-4",
        "jane-article-8",
        "jane-article-16",
    ]

    for i in range(1, 31):
        article = Article(
            title=f"John Article {i}",
            description="Test Description",
            body="Test Body",
            slug=f"john-article-{i}",
            author=john,
        )
        article.tags.append(tag1)
        article.tags.append(tag2)
        article.tags.append(tagJohn)
        db.add(article)

    for i in range(1, 21):
        article = Article(
            title=f"Jane Article {i}",
            description="Test Description",
            body="Test Body",
            slug=f"jane-article-{i}",
            author=jane,
        )
        article.tags.append(tag1)
        article.tags.append(tag2)
        article.tags.append(tagJane)

        if article.slug in john_favorited_articles:
            article.favorited_by.append(john)

        db.add(article)

    db.commit()


def test_can_paginate_articles(client: TestClient, db: Session) -> None:
    generate_articles(db)
    r = client.get("/api/articles?limit=10&offset=20")
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


def test_guest_cannot_paginate_feed(client: TestClient) -> None:
    r = client.get("/api/articles/feed")
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_can_paginate_feed(client: TestClient, db: Session) -> None:
    acting_as_john(db, client)
    r = client.get("/api/articles/feed")
    assert r.status_code == status.HTTP_200_OK
