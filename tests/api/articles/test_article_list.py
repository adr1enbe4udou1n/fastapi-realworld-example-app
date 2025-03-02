from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app.models.article import Article
from app.models.tag import Tag
from app.models.user import User
from tests.conftest import acting_as_user


def generate_articles(db: Session) -> User:
    tag1 = Tag(name="Tag 1")
    tag2 = Tag(name="Tag 2")
    johnTag = Tag(name="John Tag")
    janeTag = Tag(name="Jane Tag")

    john = User(
        name="John Doe",
        email="john.doe@example.com",
        bio="John Bio",
        image="https://randomuser.me/api/portraits/men/1.jpg",
    )
    jane = User(
        name="Jane Doe",
        email="jane.doe@example.com",
        bio="Jane Bio",
        image="https://randomuser.me/api/portraits/women/1.jpg",
    )

    jane.followers.append(john)

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
        article.tags.append(johnTag)
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
        article.tags.append(janeTag)

        if article.slug in john_favorited_articles:
            article.favorited_by.append(john)

        db.add(article)

    db.commit()
    return john


def test_can_paginate_articles(client: TestClient, db: Session) -> None:
    generate_articles(db)
    r = client.get("/api/articles?limit=10&offset=20")
    assert r.status_code == status.HTTP_200_OK
    assert len(r.json()["articles"]) == 10
    assert r.json()["articlesCount"] == 50
    assert {
        "title": "John Article 30",
        "slug": "john-article-30",
        "description": "Test Description",
        "body": "Test Body",
        "author": {
            "username": "John Doe",
            "bio": "John Bio",
            "image": "https://randomuser.me/api/portraits/men/1.jpg",
            "following": False,
        },
        "tagList": ["John Tag", "Tag 1", "Tag 2"],
        "favorited": False,
        "favoritesCount": 0,
    }.items() <= r.json()["articles"][0].items()


def test_can_filter_articles_by_author(client: TestClient, db: Session) -> None:
    generate_articles(db)
    r = client.get("/api/articles?limit=10&offset=0&author=john")
    assert r.status_code == status.HTTP_200_OK
    assert len(r.json()["articles"]) == 10
    assert r.json()["articlesCount"] == 30
    assert {
        "title": "John Article 30",
        "slug": "john-article-30",
        "description": "Test Description",
        "body": "Test Body",
        "author": {
            "username": "John Doe",
            "bio": "John Bio",
            "image": "https://randomuser.me/api/portraits/men/1.jpg",
            "following": False,
        },
        "tagList": ["John Tag", "Tag 1", "Tag 2"],
        "favorited": False,
        "favoritesCount": 0,
    }.items() <= r.json()["articles"][0].items()


def test_can_filter_articles_by_tag(client: TestClient, db: Session) -> None:
    generate_articles(db)
    r = client.get("/api/articles?limit=10&offset=0&tag=jane")
    assert r.status_code == status.HTTP_200_OK
    assert len(r.json()["articles"]) == 10
    assert r.json()["articlesCount"] == 20
    assert {
        "title": "Jane Article 20",
        "slug": "jane-article-20",
        "description": "Test Description",
        "body": "Test Body",
        "author": {
            "username": "Jane Doe",
            "bio": "Jane Bio",
            "image": "https://randomuser.me/api/portraits/women/1.jpg",
            "following": False,
        },
        "tagList": ["Jane Tag", "Tag 1", "Tag 2"],
        "favorited": False,
        "favoritesCount": 0,
    }.items() <= r.json()["articles"][0].items()


def test_can_filter_articles_by_favorited(client: TestClient, db: Session) -> None:
    john = generate_articles(db)
    acting_as_user(john, client)

    r = client.get("/api/articles?limit=10&offset=0&favorited=john")
    assert r.status_code == status.HTTP_200_OK
    assert len(r.json()["articles"]) == 5
    assert r.json()["articlesCount"] == 5
    assert {
        "title": "Jane Article 16",
        "slug": "jane-article-16",
        "description": "Test Description",
        "body": "Test Body",
        "author": {
            "username": "Jane Doe",
            "bio": "Jane Bio",
            "image": "https://randomuser.me/api/portraits/women/1.jpg",
            "following": True,
        },
        "tagList": ["Jane Tag", "Tag 1", "Tag 2"],
        "favorited": True,
        "favoritesCount": 1,
    }.items() <= r.json()["articles"][0].items()


def test_guest_cannot_paginate_feed(client: TestClient) -> None:
    r = client.get("/api/articles/feed")
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_can_paginate_feed(client: TestClient, db: Session) -> None:
    john = generate_articles(db)
    acting_as_user(john, client)

    r = client.get("/api/articles/feed?limit=10&offset=0")
    assert r.status_code == status.HTTP_200_OK
    assert len(r.json()["articles"]) == 10
    assert r.json()["articlesCount"] == 20
    assert {
        "title": "Jane Article 20",
        "slug": "jane-article-20",
        "description": "Test Description",
        "body": "Test Body",
        "author": {
            "username": "Jane Doe",
            "bio": "Jane Bio",
            "image": "https://randomuser.me/api/portraits/women/1.jpg",
            "following": True,
        },
        "tagList": ["Jane Tag", "Tag 1", "Tag 2"],
        "favorited": False,
        "favoritesCount": 0,
    }.items() <= r.json()["articles"][0].items()
