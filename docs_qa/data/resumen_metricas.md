# Resumen de Métricas Consolidadas de Ejecución — Taller de Pruebas de Software
## API: FastAPI RealWorld Example App (Conduit)
### Entorno: Python 3.14 + PostgreSQL (Docker) — Rama: uggy-version

---

## 1. Tabla de Métricas Globales Consolidadas (41 Casos: 26 Automatizados + 15 Manuales)

| # | Métrica | Fórmula aplicada | Valor Real | Meta del Proyecto | Cumplimiento |
|---|---------|------------------|------------|-------------------|--------------|
| 1 | **Tasa de ejecución global** | (41 casos ejecutados / 41 planificados) × 100 | (41 / 41) × 100 = **100.0%** | ≥ 95% | ✅ Superada |
| 2 | **Tasa de ejecución automatizada** | (26 automatizados ejecutados / 26 planificados) × 100 | (26 / 26) × 100 = **100.0%** | 100% | ✅ Conforme |
| 3 | **Tasa de ejecución manual** | (15 manuales ejecutados / 15 planificados) × 100 | (15 / 15) × 100 = **100.0%** | 100% | ✅ Conforme |
| 4 | **Tasa global de casos aprobados (Pass)** | (24 casos pasaron / 41 ejecutados) × 100 | (24 / 41) × 100 = **58.54%** | ~55% - 60% | ✅ Conforme (suite detectora) |
| 5 | **Tasa global de casos fallidos (Fail)** | (17 casos fallaron / 41 ejecutados) × 100 | (17 / 41) × 100 = **41.46%** | ~40% - 45% | ✅ Alta efectividad |
| 6 | **Tasa de aprobación en automatizados** | (15 pasaron / 26 ejecutados) × 100 | (15 / 26) × 100 = **57.69%** | ~55% | ✅ Conforme |
| 7 | **Tasa de aprobación en manuales** | (9 pasaron / 15 ejecutados) × 100 | (9 / 15) × 100 = **60.00%** | ~60% | ✅ Conforme |
| 8 | **Tasa de detección de bugs inyectados** | (9 bugs detectados / 9 inyectados) × 100 | (9 / 9) × 100 = **100.0%** | 100% | ✅ Óptimo (100% detección) |
| 9 | **Densidad de defectos (Global)** | Total defectos únicos / Total casos ejecutados | 9 / 41 = **0.220** | ~0.20 – 0.35 | ✅ Conforme |
| 10 | **Cobertura de código backend** | pytest-cov (líneas ejecutadas / total) | **82.78%** (553 / 668 líneas) | ≥ 70% | ✅ Superada (+12.78%) |
| 11 | **Cobertura de endpoints API** | (19 endpoints ejercitados / 19 existentes) × 100 | (19 / 19) × 100 = **100.0%** | 100% | ✅ Totalidad cubierta |
| 12 | **Defectos críticos detectados** | Conteo directo (Severidad Crítica) | **1** (BUG-04: borrado ajeno no autorizado) | — | 🚨 Máxima criticidad |
| 13 | **Tiempo de ejecución suite automatizada** | pytest runner con HTML y Cobertura | **28.95 segundos** | < 60s | ✅ Alto rendimiento |

---

## 2. Desglose de Ejecución por Modo de Prueba

`
+-------------------------------------------------------------------------+
|                  TOTAL CASOS DE PRUEBA: 41 (100%)                       |
+------------------------------------+------------------------------------+
|   AUTOMATIZADOS: 26 (63.4%)        |        MANUALES: 15 (36.6%)        |
|   - Pasaron: 15 (57.69%)           |        - Pasaron: 9 (60.00%)       |
|   - Fallaron: 11 (42.31%)          |        - Fallaron: 6 (40.00%)      |
+------------------------------------+------------------------------------+
`

---

## 3. Distribución de Defectos por Severidad y Prioridad

| Severidad | Prioridad Alta | Prioridad Media | Prioridad Baja | TOTAL | % Defectos |
|-----------|----------------|-----------------|----------------|-------|------------|
| **Crítica** | 1 (BUG-04) | 0 | 0 | **1** | **11.11%** |
| **Alta** | 3 (BUG-02, BUG-03, BUG-07) | 1 (BUG-05) | 0 | **4** | **44.44%** |
| **Media** | 0 | 3 (BUG-06, BUG-08, BUG-09) | 0 | **3** | **33.33%** |
| **Baja** | 0 | 0 | 1 (BUG-01) | **1** | **11.11%** |
| **TOTAL** | **4 (44.44%)** | **4 (44.44%)** | **1 (11.11%)** | **9** | **100.0%** |

---

## 4. Matriz Completa de Trazabilidad Cruzada: Defecto vs. Pruebas

| Bug ID | Módulo | Severidad / Prioridad | Caso Automatizado (pytest) | Caso Manual (Swagger UI) | Evidencia de Soporte |
|--------|--------|-----------------------|----------------------------|--------------------------|----------------------|
| **BUG-01** | Auth | Baja / Baja | CP-AUTH-A-001 (retorna 200) | CP-EXP-M-001 | CP-EXP-M-001_registro- Codigo 200 Error Creacion de Usuario.png |
| **BUG-02** | Articles | Alta / Alta | CP-ART-A-002 (título vacío) | — | Reporte HTML pytest |
| **BUG-03** | Articles | Alta / Alta | CP-ART-A-005 (edición ajena) | CP-QUAL-M-003 | P-QUAL-M-003_edit_ajeno_bug03.png |
| **BUG-04** | Articles | **Crítica / Alta** | CP-ART-A-006 (borrado ajeno) | CP-QUAL-M-004 | CP-QUAL-M-004_delete_ajeno_bug04.png |
| **BUG-05** | Favorites | Alta / Media | CP-FAV-A-001, CP-FAV-A-002 | CP-EXP-M-001, CP-EST-M-002 | CP-EST-M-002_favorite_500_bug05.png |
| **BUG-06** | Profiles | Media / Media | CP-PRF-A-001, CP-PRF-A-002 | CP-EXP-M-001, CP-EST-M-001 | CP-EST-M-001_follow_false_bug06.png |
| **BUG-07** | Articles | Alta / Alta | CP-ART-A-007 (feed sin auth) | CP-EXP-M-001 | Reporte HTML pytest |
| **BUG-08** | Articles | Media / Media | CP-ART-A-008 (filtro tag) | — | Reporte HTML pytest |
| **BUG-09** | Articles | Media / Media | CP-ART-A-009 (limit=100) | CP-EXP-M-004 | CP-EXP-M-004_limit_100_bug09.png..png |

---

## 5. Archivos de Respaldo y Entregables del Ciclo de Prueba

1. **Plan de Pruebas Maestro:** docs_qa/plan_pruebas (1).md
2. **Especificación y Registro de 41 Casos:** docs_qa/Casos_De_Prueba.md
3. **Fichas de Reporte MantisBT (9 Defectos):** docs_qa/Fichas_De_Bugs_MantisBT.md
4. **Análisis de Calidad del Software:** docs_qa/Analisis_Calidad.md
5. **Reporte HTML Interactivo:** docs_qa/reports/test_report.html
6. **Resultados Automatizados JSON:** docs_qa/data/pytest_results.json
7. **Resultados Cobertura JSON:** docs_qa/data/coverage.json
8. **Evidencias Gráficas Manuales:** Directorio docs_qa/evidencias/
