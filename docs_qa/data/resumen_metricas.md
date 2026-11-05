# Resumen de Métricas de Ejecución — Taller de Pruebas de Software
## API: FastAPI RealWorld Example App (Conduit)
### Entorno: Python 3.14 + PostgreSQL (Docker) — Rama: `buggy-version`

---

## 1. Tabla de Métricas Consolidadas

| # | Métrica | Fórmula aplicada | Valor Real | Meta del Proyecto | Cumplimiento |
|---|---------|------------------|------------|-------------------|--------------|
| 1 | **Tasa de ejecución de casos** | (Casos ejecutados / Total planificados) × 100 | (26 / 26) × 100 = **100%** | ≥ 95% | ✅ Superada |
| 2 | **Tasa de casos aprobados** | (Casos Pasaron / Casos ejecutados) × 100 | (15 / 26) × 100 = **57.69%** | ≥ 50% (en buggy-version) | ✅ Esperado (detectando bugs) |
| 3 | **Densidad de defectos** | Defectos encontrados / Casos ejecutados | 9 / 26 = **0.346** | ~0.20 – 0.35 | ✅ Conforme |
| 4 | **Cobertura de código** | pytest-cov (líneas ejecutadas / total) | **82.78%** (553 / 668 líneas) | ≥ 70% | ✅ Superada (+12.78%) |
| 5 | **Tasa de detección de bugs inyectados** | (Bugs detectados / Bugs inyectados) × 100 | (9 / 9) × 100 = **100.0%** | 100% | ✅ Óptimo (9 de 9) |
| 6 | **Defectos críticos detectados** | Conteo directo (Severidad Crítica) | **1** (BUG-04: borrado no autorizado) | — | 🚨 Prioridad inmediata |
| 7 | **Defectos por severidad** | Agrupación | Crítica: 1, Alta: 4, Media: 3, Baja: 1 | — | Matriz balanceada |
| 8 | **Tiempo total de ejecución de la suite** | pytest runner | **28.95 segundos** | < 60s | ✅ Alta velocidad |

---

## 2. Distribución de Defectos por Severidad y Prioridad

| Severidad | Prioridad Alta | Prioridad Media | Prioridad Baja | TOTAL |
|-----------|----------------|-----------------|----------------|-------|
| **Crítica** | 1 (BUG-04) | 0 | 0 | **1** |
| **Alta** | 3 (BUG-02, BUG-03, BUG-07) | 1 (BUG-05) | 0 | **4** |
| **Media** | 0 | 3 (BUG-06, BUG-08, BUG-09) | 0 | **3** |
| **Baja** | 0 | 0 | 1 (BUG-01) | **1** |
| **TOTAL** | **4** | **4** | **1** | **9** |

---

## 3. Matriz de Trazabilidad: Bug inyectado vs. Test Automatizado

| Bug ID | Módulo | Severidad | Prioridad | Script de Test en `tests/` | Caso ID | Resultado en `buggy-version` |
|--------|--------|-----------|-----------|---------------------------|---------|------------------------------|
| **BUG-01** | Auth | Baja | Baja | `test_auth.py::test_registro_retorna_201` | CP-AUTH-A-001 | ❌ FAILED (retorna 200) |
| **BUG-02** | Articles | Alta | Alta | `test_articles.py::test_crear_articulo_titulo_vacio_retorna_422` | CP-ART-A-002 | ❌ FAILED (retorna 200) |
| **BUG-03** | Articles | Alta | Alta | `test_articles.py::test_editar_articulo_ajeno_retorna_400` | CP-ART-A-005 | ❌ FAILED (retorna 200) |
| **BUG-04** | Articles | **Crítica** | **Alta** | `test_articles.py::test_eliminar_articulo_ajeno_retorna_400` | CP-ART-A-006 | ❌ FAILED (retorna 200) |
| **BUG-05** | Favorites | Alta | Media | `test_favorites.py::test_marcar_favorito_incrementa_contador`<br>`test_favorites.py::test_desmarcar_favorito_decrementa_contador` | CP-FAV-A-001<br>CP-FAV-A-002 | ❌ FAILED (ValueError: not in list) |
| **BUG-06** | Profiles | Media | Media | `test_profiles.py::test_seguir_usuario_cambia_following_a_true`<br>`test_profiles.py::test_dejar_de_seguir_cambia_following_a_false` | CP-PRF-A-001<br>CP-PRF-A-002 | ❌ FAILED (following=False) |
| **BUG-07** | Articles | Alta | Alta | `test_articles.py::test_feed_sin_auth_retorna_401` | CP-ART-A-007 | ❌ FAILED (no retorna 401) |
| **BUG-08** | Articles | Media | Media | `test_articles.py::test_filtrar_articulos_por_tag` | CP-ART-A-008 | ❌ FAILED (articlesCount=3 en vez de 2) |
| **BUG-09** | Articles | Media | Media | `test_articles.py::test_limit_capeado_en_20_articulos` | CP-ART-A-009 | ❌ FAILED (devuelve 25 > 20) |

---

## 4. Archivos de Datos Generados para el Dashboard

1. **Reporte HTML interactivo:** `docs_qa/reports/test_report.html`
2. **Resultados de ejecución en JSON:** `docs_qa/data/pytest_results.json`
3. **Reporte de cobertura en JSON:** `docs_qa/data/coverage.json`
4. **Fichas de bugs para MantisBT:** `docs_qa/Fichas_De_Bugs_MantisBT.md`
