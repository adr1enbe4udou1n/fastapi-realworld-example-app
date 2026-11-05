"""
test_profiles.py — Módulo Profiles
=====================================
CP-PRF-A-001 : Seguir usuario cambia following a true    (BUG-06)
CP-PRF-A-002 : Dejar de seguir cambia following a false  (BUG-06)
CP-PRF-A-003 : GET perfil inexistente retorna 404
CP-PRF-A-004 : Seguir usuario sin autenticación retorna 401
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import auth_header, create_jane, create_john


# ---------------------------------------------------------------------------
# CP-PRF-A-001
# Nombre   : Seguir usuario cambia el campo following a true
# Técnica  : Transición de estados (estado inicial: following=false → POST follow → following=true)
# Bug      : BUG-06 — profile() siempre retorna following=False
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_seguir_usuario_cambia_following_a_true(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-PRF-A-001: POST /api/profiles/{username}/follow debe retornar following=true."""
    john = await create_john(db)
    jane = await create_jane(db)

    # John sigue a Jane
    headers = auth_header(john)
    response = client.post(
        "/api/profiles/Jane Doe/follow", headers=headers
    )
    body = response.json()

    assert response.status_code == 200, (
        f"[CP-PRF-A-001] Se esperaba HTTP 200, se obtuvo {response.status_code}. Body: {body}"
    )
    assert "profile" in body, "[CP-PRF-A-001] La respuesta no contiene la clave 'profile'."
    assert body["profile"]["following"] is True, (
        f"[CP-PRF-A-001] Se esperaba following=true después de seguir, "
        f"se obtuvo {body['profile'].get('following')}. "
        "Posible BUG-06: el método profile() siempre retorna following=False."
    )


# ---------------------------------------------------------------------------
# CP-PRF-A-002
# Nombre   : Dejar de seguir cambia el campo following a false
# Técnica  : Transición de estados (following=true → DELETE follow → following=false)
# Bug      : BUG-06 — profile() siempre retorna following=False
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_dejar_de_seguir_cambia_following_a_false(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-PRF-A-002: DELETE /api/profiles/{username}/follow debe retornar following=false."""
    john = await create_john(db)
    jane = await create_jane(db)
    headers = auth_header(john)

    # Precondición: John ya sigue a Jane
    follow_response = client.post("/api/profiles/Jane Doe/follow", headers=headers)
    assert follow_response.status_code == 200, (
        f"[CP-PRF-A-002] Error en el setup de follow: {follow_response.status_code}."
    )
    # Verificar que el follow funcionó (precondición del estado)
    assert follow_response.json()["profile"]["following"] is True, (
        "[CP-PRF-A-002] El follow inicial no dejó following=true. No se puede validar el unfollow."
    )

    # Acción: John deja de seguir a Jane
    unfollow_response = client.delete(
        "/api/profiles/Jane Doe/follow", headers=headers
    )
    body = unfollow_response.json()

    assert unfollow_response.status_code == 200, (
        f"[CP-PRF-A-002] Se esperaba HTTP 200, se obtuvo {unfollow_response.status_code}. Body: {body}"
    )
    assert body["profile"]["following"] is False, (
        f"[CP-PRF-A-002] Se esperaba following=false después de dejar de seguir, "
        f"se obtuvo {body['profile'].get('following')}."
    )


# ---------------------------------------------------------------------------
# CP-PRF-A-003
# Nombre   : Obtener perfil de usuario inexistente retorna HTTP 404
# Técnica  : EP (partición inválida: username que no existe)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_perfil_inexistente_retorna_404(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-PRF-A-003: GET /api/profiles/{username} con username inexistente retorna HTTP 404."""
    response = client.get("/api/profiles/usuarionoeexiste12345")

    assert response.status_code == 404, (
        f"[CP-PRF-A-003] Se esperaba HTTP 404, se obtuvo {response.status_code}."
    )


# ---------------------------------------------------------------------------
# CP-PRF-A-004
# Nombre   : Seguir usuario sin autenticación retorna HTTP 401
# Técnica  : Tabla de decisión (no autenticado × endpoint protegido)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_seguir_usuario_sin_auth_retorna_401(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-PRF-A-004: POST /api/profiles/{username}/follow sin Authorization retorna HTTP 401."""
    john = await create_john(db)

    response = client.post(
        f"/api/profiles/{john.name}/follow"  # Sin headers de auth
    )

    assert response.status_code == 401, (
        f"[CP-PRF-A-004] Se esperaba HTTP 401, se obtuvo {response.status_code}."
    )

