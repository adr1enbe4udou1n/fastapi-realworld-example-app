"""
test_tags.py — Módulo Tags
============================
CP-TAG-A-001 : GET /api/tags retorna lista de tags existentes
CP-TAG-A-002 : Tags de artículo creado aparecen en GET /api/tags
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import auth_header, create_article, create_john


# ---------------------------------------------------------------------------
# CP-TAG-A-001
# Nombre   : GET /api/tags retorna lista de tags existentes
# Técnica  : EP (partición válida: hay tags en BD)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_tags_retorna_lista(client: TestClient, db: AsyncSession) -> None:
    """CP-TAG-A-001: GET /api/tags debe retornar HTTP 200 con una lista de tags."""
    john = await create_john(db)

    # Crear artículo con tags para que haya algo en la BD
    await create_article(
        db, author=john, title="Tagged Article", slug="tagged-article",
        tags=["python", "fastapi"]
    )

    response = client.get("/api/tags")
    body = response.json()

    assert response.status_code == 200, (
        f"[CP-TAG-A-001] Se esperaba HTTP 200, se obtuvo {response.status_code}."
    )
    assert "tags" in body, (
        "[CP-TAG-A-001] La respuesta no contiene la clave 'tags'."
    )
    assert isinstance(body["tags"], list), (
        f"[CP-TAG-A-001] Se esperaba que 'tags' fuera una lista, "
        f"se obtuvo {type(body['tags']).__name__}."
    )
    assert len(body["tags"]) >= 1, (
        "[CP-TAG-A-001] La lista de tags está vacía, pero se crearon tags."
    )


# ---------------------------------------------------------------------------
# CP-TAG-A-002
# Nombre   : Tags de un artículo recién creado aparecen en GET /api/tags
# Técnica  : EP (verificar integración: crear artículo → ver tag en listado global)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_tags_de_articulo_creado_aparecen_en_get_tags(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-TAG-A-002: Tags del artículo creado vía API deben aparecer en GET /api/tags."""
    john = await create_john(db)
    headers = auth_header(john)

    # Crear artículo con un tag único vía API
    unique_tag = "qa-automation-tag-unique"
    payload = {
        "article": {
            "title": "Article With Unique Tag",
            "description": "Test description",
            "body": "Test body",
            "tagList": [unique_tag],
        }
    }

    create_response = client.post("/api/articles", json=payload, headers=headers)
    assert create_response.status_code == 200, (
        f"[CP-TAG-A-002] Error al crear artículo: {create_response.status_code}."
    )

    # Verificar que el tag aparece en GET /api/tags
    tags_response = client.get("/api/tags")
    body = tags_response.json()

    assert tags_response.status_code == 200, (
        f"[CP-TAG-A-002] GET /api/tags falló con {tags_response.status_code}."
    )
    assert unique_tag in body["tags"], (
        f"[CP-TAG-A-002] El tag '{unique_tag}' no aparece en GET /api/tags. "
        f"Tags disponibles: {body['tags']}."
    )

