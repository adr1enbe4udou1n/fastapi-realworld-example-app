"""
test_favorites.py — Módulo Favorites
=======================================
CP-FAV-A-001 : Marcar favorito incrementa favoritesCount en 1   (BUG-05)
CP-FAV-A-002 : Desmarcar favorito decrementa favoritesCount en 1 (BUG-05)
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import auth_header, create_article, create_john


# ---------------------------------------------------------------------------
# CP-FAV-A-001
# Nombre   : Marcar artículo como favorito incrementa favoritesCount en 1
# Técnica  : Transición de estados (favorited=false, count=0 → POST favorite → favorited=true, count=1)
# Bug      : BUG-05 — el endpoint llama favorite=False, invirtiendo la lógica
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_marcar_favorito_incrementa_contador(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-FAV-A-001: POST /api/articles/{slug}/favorite debe poner favorited=true y count=1."""
    john = await create_john(db)
    await create_article(db, author=john, title="Test Article", slug="test-article")
    headers = auth_header(john)

    # Verificar estado inicial
    initial_response = client.get("/api/articles/test-article")
    initial_body = initial_response.json()
    assert initial_body["article"]["favoritesCount"] == 0, (
        "[CP-FAV-A-001] El artículo recién creado debería tener favoritesCount=0."
    )

    # Marcar como favorito
    response = client.post("/api/articles/test-article/favorite", headers=headers)
    body = response.json()

    assert response.status_code == 200, (
        f"[CP-FAV-A-001] Se esperaba HTTP 200, se obtuvo {response.status_code}. Body: {body}"
    )
    assert body["article"]["favorited"] is True, (
        f"[CP-FAV-A-001] Se esperaba favorited=true, se obtuvo {body['article'].get('favorited')}. "
        "Posible BUG-05: la lógica de favoritos está invertida."
    )
    assert body["article"]["favoritesCount"] == 1, (
        f"[CP-FAV-A-001] Se esperaba favoritesCount=1, "
        f"se obtuvo {body['article'].get('favoritesCount')}. "
        "Posible BUG-05: marcar como favorito no incrementó el contador."
    )


# ---------------------------------------------------------------------------
# CP-FAV-A-002
# Nombre   : Desmarcar favorito decrementa favoritesCount en 1
# Técnica  : Transición de estados (favorited=true, count=1 → DELETE favorite → favorited=false, count=0)
# Bug      : BUG-05 — el endpoint llama favorite=False invirtiendo la lógica
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_desmarcar_favorito_decrementa_contador(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-FAV-A-002: DELETE /api/articles/{slug}/favorite debe poner favorited=false y count=0."""
    john = await create_john(db)
    await create_article(db, author=john, title="Test Article", slug="test-article")
    headers = auth_header(john)

    # Precondición: marcar como favorito primero
    fav_response = client.post("/api/articles/test-article/favorite", headers=headers)
    assert fav_response.status_code == 200, (
        f"[CP-FAV-A-002] Error en setup de favorito: {fav_response.status_code}."
    )
    assert fav_response.json()["article"]["favorited"] is True, (
        "[CP-FAV-A-002] El setup de favorito no dejó favorited=true. "
        "No se puede validar el desmarcar."
    )

    # Desmarcar favorito
    response = client.delete("/api/articles/test-article/favorite", headers=headers)
    body = response.json()

    assert response.status_code == 200, (
        f"[CP-FAV-A-002] Se esperaba HTTP 200, se obtuvo {response.status_code}. Body: {body}"
    )
    assert body["article"]["favorited"] is False, (
        f"[CP-FAV-A-002] Se esperaba favorited=false después de desmarcar, "
        f"se obtuvo {body['article'].get('favorited')}."
    )
    assert body["article"]["favoritesCount"] == 0, (
        f"[CP-FAV-A-002] Se esperaba favoritesCount=0 después de desmarcar, "
        f"se obtuvo {body['article'].get('favoritesCount')}."
    )

