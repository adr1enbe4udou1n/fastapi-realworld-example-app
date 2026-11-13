"""
test_comments.py — Módulo Comments
=====================================
CP-COM-A-001 : Crear comentario en artículo existente retorna comentario
CP-COM-A-002 : Crear comentario sin autenticación retorna 401
CP-COM-A-003 : Eliminar comentario propio retorna 200/204
CP-COM-A-004 : GET comentarios de artículo inexistente retorna 404
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import auth_header, create_article, create_john


# ---------------------------------------------------------------------------
# CP-COM-A-001
# Nombre   : Crear comentario en artículo existente retorna el comentario creado
# Técnica  : EP (partición válida: artículo existente + usuario autenticado)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_crear_comentario_en_articulo_existente(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-COM-A-001: POST /api/articles/{slug}/comments debe retornar el comentario creado."""
    john = await create_john(db)
    await create_article(db, author=john, title="Test Article", slug="test-article")
    headers = auth_header(john)

    payload = {"comment": {"body": "Este es mi comentario de prueba."}}

    response = client.post(
        "/api/articles/test-article/comments", json=payload, headers=headers
    )
    body = response.json()

    assert response.status_code == 200, (
        f"[CP-COM-A-001] Se esperaba HTTP 200, se obtuvo {response.status_code}. Body: {body}"
    )
    assert "comment" in body, "[CP-COM-A-001] La respuesta no contiene la clave 'comment'."
    assert body["comment"]["body"] == "Este es mi comentario de prueba.", (
        f"[CP-COM-A-001] El cuerpo del comentario no coincide: {body['comment'].get('body')}."
    )
    assert "id" in body["comment"], (
        "[CP-COM-A-001] El comentario creado no tiene 'id' en la respuesta."
    )
    assert body["comment"]["author"]["username"] == "John Doe", (
        f"[CP-COM-A-001] Autor del comentario incorrecto: {body['comment']['author'].get('username')}."
    )


# ---------------------------------------------------------------------------
# CP-COM-A-002
# Nombre   : Crear comentario sin autenticación retorna HTTP 401
# Técnica  : Tabla de decisión (no autenticado × endpoint protegido)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_crear_comentario_sin_auth_retorna_401(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-COM-A-002: POST /api/articles/{slug}/comments sin Authorization retorna HTTP 401."""
    john = await create_john(db)
    await create_article(db, author=john, title="Test Article", slug="test-article")

    payload = {"comment": {"body": "Comentario sin autenticación."}}

    response = client.post(
        "/api/articles/test-article/comments", json=payload  # Sin headers
    )

    assert response.status_code == 401, (
        f"[CP-COM-A-002] Se esperaba HTTP 401, se obtuvo {response.status_code}."
    )


# ---------------------------------------------------------------------------
# CP-COM-A-003
# Nombre   : Eliminar comentario propio retorna éxito (200 o 204)
# Técnica  : EP (partición válida: comentario propio + autor autenticado)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_eliminar_comentario_propio(client: TestClient, db: AsyncSession) -> None:
    """CP-COM-A-003: DELETE /api/articles/{slug}/comments/{id} como autor retorna éxito."""
    john = await create_john(db)
    await create_article(db, author=john, title="Test Article", slug="test-article")
    headers = auth_header(john)

    # Crear comentario primero
    create_payload = {"comment": {"body": "Comentario a eliminar."}}
    create_response = client.post(
        "/api/articles/test-article/comments", json=create_payload, headers=headers
    )
    assert create_response.status_code == 200, (
        f"[CP-COM-A-003] Error al crear el comentario de setup: {create_response.status_code}."
    )
    comment_id = create_response.json()["comment"]["id"]

    # Eliminar el comentario
    delete_response = client.delete(
        f"/api/articles/test-article/comments/{comment_id}", headers=headers
    )

    assert delete_response.status_code in (200, 204), (
        f"[CP-COM-A-003] Se esperaba HTTP 200 o 204, se obtuvo {delete_response.status_code}."
    )

    # Verificar que el comentario ya no existe
    list_response = client.get("/api/articles/test-article/comments")
    comments = list_response.json().get("comments", [])
    ids = [c["id"] for c in comments]
    assert comment_id not in ids, (
        f"[CP-COM-A-003] El comentario {comment_id} sigue presente después de eliminarlo."
    )


# ---------------------------------------------------------------------------
# CP-COM-A-004
# Nombre   : GET comentarios de artículo inexistente retorna HTTP 404
# Técnica  : EP (partición inválida: slug que no existe en BD)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_comentarios_articulo_inexistente_retorna_404(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-COM-A-004: GET /api/articles/{slug}/comments con slug inexistente retorna HTTP 404."""
    response = client.get("/api/articles/no-existe-este-articulo/comments")

    assert response.status_code == 404, (
        f"[CP-COM-A-004] Se esperaba HTTP 404, se obtuvo {response.status_code}."
    )

