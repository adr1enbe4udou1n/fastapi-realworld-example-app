"""
test_articles.py — Módulo Articles
====================================
CP-ART-A-001 : Crear artículo válido retorna 200 y estructura correcta
CP-ART-A-002 : Crear artículo con título vacío retorna 422            (BUG-02)
CP-ART-A-003 : Crear artículo sin autenticación retorna 401
CP-ART-A-004 : Editar artículo como autor retorna artículo actualizado
CP-ART-A-005 : Editar artículo ajeno retorna 400                      (BUG-03)
CP-ART-A-006 : Eliminar artículo ajeno retorna 400                    (BUG-04)
CP-ART-A-007 : GET /feed sin autenticación retorna 401                (BUG-07)
CP-ART-A-008 : Filtrar artículos por tag devuelve solo los correctos  (BUG-08)
CP-ART-A-009 : limit=100 retorna máximo 20 artículos (BVA)           (BUG-09)
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import auth_header, create_article, create_jane, create_john


# ---------------------------------------------------------------------------
# CP-ART-A-001
# Nombre   : Crear artículo con datos válidos retorna HTTP 200 con estructura correcta
# Técnica  : EP (partición válida: todos los campos presentes y correctos)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_crear_articulo_valido(client: TestClient, db: AsyncSession) -> None:
    """CP-ART-A-001: POST /api/articles con datos válidos retorna 200 y estructura correcta."""
    john = await create_john(db)
    headers = auth_header(john)

    payload = {
        "article": {
            "title": "Test Title",
            "description": "Test Description",
            "body": "Test Body",
            "tagList": ["tag1", "tag2"],
        }
    }

    response = client.post("/api/articles", json=payload, headers=headers)
    body = response.json()

    assert response.status_code == 200, (
        f"[CP-ART-A-001] Se esperaba HTTP 200, se obtuvo {response.status_code}. Body: {body}"
    )
    assert "article" in body, "[CP-ART-A-001] La respuesta no contiene la clave 'article'."

    article = body["article"]
    assert article["slug"] == "test-title", (
        f"[CP-ART-A-001] Slug esperado 'test-title', obtenido '{article.get('slug')}'."
    )
    assert article["title"] == "Test Title", (
        f"[CP-ART-A-001] Título esperado 'Test Title', obtenido '{article.get('title')}'."
    )
    assert article["favorited"] is False, (
        "[CP-ART-A-001] Un artículo recién creado no debe estar marcado como favorito."
    )
    assert article["favoritesCount"] == 0, (
        "[CP-ART-A-001] Un artículo recién creado debe tener favoritesCount = 0."
    )
    assert "tag1" in article["tagList"] and "tag2" in article["tagList"], (
        f"[CP-ART-A-001] Los tags enviados no aparecen en la respuesta: {article.get('tagList')}."
    )
    assert article["author"]["username"] == "John Doe", (
        f"[CP-ART-A-001] Autor esperado 'John Doe', obtenido '{article['author'].get('username')}'."
    )


# ---------------------------------------------------------------------------
# CP-ART-A-002
# Nombre   : Crear artículo con título vacío retorna HTTP 422 Unprocessable Entity
# Técnica  : BVA (límite inferior: string vacío = longitud 0, mínimo permitido = 1)
# Bug      : BUG-02 — se elimina min_length=1 del campo title en el schema
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_crear_articulo_titulo_vacio_retorna_422(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-ART-A-002: POST /api/articles con title='' debe retornar HTTP 422."""
    john = await create_john(db)
    headers = auth_header(john)

    payload = {
        "article": {
            "title": "",  # BVA: valor en el límite inferior (0 < mínimo de 1)
            "description": "Test Description",
            "body": "Test Body",
            "tagList": [],
        }
    }

    response = client.post("/api/articles", json=payload, headers=headers)

    assert response.status_code == 422, (
        f"[CP-ART-A-002] Se esperaba HTTP 422, se obtuvo {response.status_code}. "
        "Posible BUG-02: la validación min_length=1 en el campo 'title' fue eliminada."
    )


# ---------------------------------------------------------------------------
# CP-ART-A-003
# Nombre   : Crear artículo sin token de autenticación retorna HTTP 401
# Técnica  : Tabla de decisión (no autenticado × endpoint protegido)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_crear_articulo_sin_auth_retorna_401(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-ART-A-003: POST /api/articles sin Authorization header debe retornar HTTP 401."""
    payload = {
        "article": {
            "title": "Test",
            "description": "Test",
            "body": "Test",
        }
    }

    response = client.post("/api/articles", json=payload)  # Sin headers de auth

    assert response.status_code == 401, (
        f"[CP-ART-A-003] Se esperaba HTTP 401, se obtuvo {response.status_code}."
    )


# ---------------------------------------------------------------------------
# CP-ART-A-004
# Nombre   : Editar artículo como autor legítimo retorna HTTP 200 con artículo actualizado
# Técnica  : Tabla de decisión (autenticado × autor del artículo)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_editar_articulo_como_autor(client: TestClient, db: AsyncSession) -> None:
    """CP-ART-A-004: PUT /api/articles/{slug} como autor retorna 200 con datos actualizados."""
    john = await create_john(db)
    await create_article(db, author=john, title="Test Title", slug="test-title")
    headers = auth_header(john)

    update_payload = {"article": {"title": "New Title"}}

    response = client.put(
        "/api/articles/test-title", json=update_payload, headers=headers
    )
    body = response.json()

    assert response.status_code == 200, (
        f"[CP-ART-A-004] Se esperaba HTTP 200, se obtuvo {response.status_code}. Body: {body}"
    )
    assert body["article"]["title"] == "New Title", (
        f"[CP-ART-A-004] Se esperaba título 'New Title', obtenido '{body['article'].get('title')}'."
    )


# ---------------------------------------------------------------------------
# CP-ART-A-005
# Nombre   : Editar artículo de otro usuario retorna HTTP 400 Bad Request
# Técnica  : Tabla de decisión (autenticado × no-autor)
# Bug      : BUG-03 — se elimina la verificación de autoría en PUT /{slug}
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_editar_articulo_ajeno_retorna_400(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-ART-A-005: PUT /api/articles/{slug} como no-autor debe retornar HTTP 400."""
    john = await create_john(db)
    jane = await create_jane(db)

    # Jane crea un artículo
    await create_article(db, author=jane, title="Jane Article", slug="jane-article")

    # John (no-autor) intenta editar el artículo de Jane
    headers = auth_header(john)
    payload = {"article": {"title": "Modificado por John"}}

    response = client.put(
        "/api/articles/jane-article", json=payload, headers=headers
    )

    assert response.status_code == 400, (
        f"[CP-ART-A-005] Se esperaba HTTP 400, se obtuvo {response.status_code}. "
        "Posible BUG-03: la verificación de autoría en PUT fue eliminada. "
        "Cualquier usuario autenticado puede editar artículos ajenos."
    )


# ---------------------------------------------------------------------------
# CP-ART-A-006
# Nombre   : Eliminar artículo de otro usuario retorna HTTP 400 Bad Request
# Técnica  : Tabla de decisión (autenticado × no-autor)
# Bug      : BUG-04 — se elimina la verificación de autoría en DELETE /{slug}
# Prioridad: CRÍTICA — brecha de seguridad
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_eliminar_articulo_ajeno_retorna_400(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-ART-A-006: DELETE /api/articles/{slug} como no-autor debe retornar HTTP 400."""
    john = await create_john(db)
    jane = await create_jane(db)

    # Jane crea un artículo
    await create_article(db, author=jane, title="Jane Article", slug="jane-article")

    # John (no-autor) intenta eliminar el artículo de Jane
    headers = auth_header(john)

    response = client.delete("/api/articles/jane-article", headers=headers)

    assert response.status_code == 400, (
        f"[CP-ART-A-006] Se esperaba HTTP 400, se obtuvo {response.status_code}. "
        "ALERTA DE SEGURIDAD (BUG-04): la verificación de autoría en DELETE fue eliminada. "
        "Cualquier usuario autenticado puede eliminar artículos ajenos."
    )

    # Verificación adicional: el artículo de Jane aún debe existir en la BD
    verify_response = client.get("/api/articles/jane-article")
    assert verify_response.status_code == 200, (
        "[CP-ART-A-006] El artículo de Jane fue eliminado por John — confirmado el BUG-04."
    )


# ---------------------------------------------------------------------------
# CP-ART-A-007
# Nombre   : GET /api/articles/feed sin autenticación retorna HTTP 401
# Técnica  : Tabla de decisión (no autenticado × endpoint protegido con auth obligatoria)
# Bug      : BUG-07 — se cambia CurrentUser por OptionalCurrentUser en get_feed()
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_feed_sin_auth_retorna_401(client: TestClient, db: AsyncSession) -> None:
    """CP-ART-A-007: GET /api/articles/feed sin token debe retornar HTTP 401."""
    response = client.get("/api/articles/feed")  # Sin Authorization

    assert response.status_code == 401, (
        f"[CP-ART-A-007] Se esperaba HTTP 401, se obtuvo {response.status_code}. "
        "Posible BUG-07: el feed acepta peticiones sin autenticación (retorna 200 vacío)."
    )


# ---------------------------------------------------------------------------
# CP-ART-A-008
# Nombre   : Filtrar artículos por tag retorna únicamente los artículos con ese tag
# Técnica  : EP (partición: con filtro ?tag= activo)
# Bug      : BUG-08 — el filtro por tag es ignorado, retorna todos los artículos
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_filtrar_articulos_por_tag(client: TestClient, db: AsyncSession) -> None:
    """CP-ART-A-008: GET /api/articles?tag=python debe retornar solo artículos con ese tag."""
    john = await create_john(db)

    # Crear artículos con tags distintos
    await create_article(
        db, author=john, title="Python Article 1", slug="python-article-1",
        tags=["python"]
    )
    await create_article(
        db, author=john, title="Python Article 2", slug="python-article-2",
        tags=["python"]
    )
    await create_article(
        db, author=john, title="Java Article", slug="java-article",
        tags=["java"]
    )

    response = client.get("/api/articles?tag=python")
    body = response.json()

    assert response.status_code == 200, (
        f"[CP-ART-A-008] Se esperaba HTTP 200, se obtuvo {response.status_code}."
    )
    assert body["articlesCount"] == 2, (
        f"[CP-ART-A-008] Se esperaban 2 artículos con tag 'python', "
        f"se obtuvieron {body['articlesCount']}. "
        "Posible BUG-08: el filtro por tag está siendo ignorado (retorna todos los artículos)."
    )
    for article in body["articles"]:
        assert "python" in article["tagList"], (
            f"[CP-ART-A-008] Artículo '{article['title']}' no contiene el tag 'python'. "
            "El filtro no está funcionando correctamente."
        )


# ---------------------------------------------------------------------------
# CP-ART-A-009
# Nombre   : Solicitar ?limit=100 retorna máximo 20 artículos (BVA)
# Técnica  : BVA (límite máximo = 20; valor de prueba = 100, muy por encima del límite)
# Bug      : BUG-09 — se pasa limit directamente sin capar al máximo de 20
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_limit_capeado_en_20_articulos(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-ART-A-009: GET /api/articles?limit=100 debe retornar máximo 20 artículos."""
    john = await create_john(db)

    # Crear 25 artículos para superar el límite
    for i in range(1, 26):
        await create_article(
            db,
            author=john,
            title=f"Article {i:02d}",
            slug=f"article-{i:02d}",
        )

    response = client.get("/api/articles?limit=100")
    body = response.json()

    assert response.status_code == 200, (
        f"[CP-ART-A-009] Se esperaba HTTP 200, se obtuvo {response.status_code}."
    )

    articles_returned = len(body["articles"])
    assert articles_returned <= 20, (
        f"[CP-ART-A-009] Se esperaban máximo 20 artículos, se obtuvieron {articles_returned}. "
        "Posible BUG-09: el parámetro limit no está siendo capado al máximo de 20."
    )

    total_count = body["articlesCount"]
    assert total_count == 25, (
        f"[CP-ART-A-009] articlesCount debe reflejar el total real (25), "
        f"se obtuvo {total_count}."
    )

