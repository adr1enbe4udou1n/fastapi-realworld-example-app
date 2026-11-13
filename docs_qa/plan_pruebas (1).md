# **PLAN DE PRUEBAS**
`
_FastAPI RealWorld Example App — Conduit (Backend API)_
`
| **Proyecto:** | FastAPI RealWorld Example App — Conduit (Backend API) |
|---|---|
| **Versión:** | 2.0 |
| **Fecha:** | 09/11/2026 |
| **Elaborado por:** | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas |
| **Revisado por:** | Niurka Liseth Mejía Vargas / Juan Pablo Velásquez Ramírez |
| **Aprobado por:** | Yury Montoya Pérez |
| **Estado:** | [ ] Borrador  [ ] En revisión  [x] Finalizado / Entregado |
`
---
`
## **1. Historial de Cambios**
`
| **Versión** | **Fecha** | **Descripción del Cambio** | **Autor** | **Aprobado por** |
|---|---|---|---|---|
| 1.0 | 26/10/2025 | Versión inicial del plan de pruebas | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas | Yury Montoya Pérez |
| 2.0 | 09/11/2026 | Ejecución integral del STLC, métricas reales y cierre formal | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas | Yury Montoya Pérez |
`
---
`
## **2. Introducción**
`
### **2.1 Propósito**
`
Este documento describe la estrategia, alcance, recursos, técnicas y actividades de prueba para el sistema **FastAPI RealWorld Example App (Conduit)**, en el marco del taller universitario de la materia Pruebas de Software. El propósito es garantizar que la API cumpla con los contratos de comportamiento esperados, y validar que los mecanismos de prueba diseñados son efectivos para detectar defectos reales en el sistema.
`
El proceso de pruebas combina ejecución manual exploratoria (Swagger UI / Postman) con automatización a nivel de integración (pytest), buscando detectar defectos en los módulos de autenticación, gestión de artículos, comentarios, perfiles, favoritos y tags. Los hallazgos se documentan en MantisBT y se analizan mediante métricas cuantitativas al cierre del ciclo.
`
### **2.2 Alcance**
`
| **En alcance** | **Fuera de alcance** |
|---|---|
| Autenticación: registro y login de usuarios (JWT) | Interfaz gráfica (UI/Frontend) — la aplicación es backend-only |
| Gestión del usuario autenticado (GET/PUT /api/user) | Pruebas de rendimiento y carga |
| Perfiles públicos: ver, seguir y dejar de seguir usuarios | Pruebas de infraestructura (Docker, red, BD) |
| CRUD completo de artículos | Migraciones de base de datos (Alembic) |
| Feed de artículos de usuarios seguidos | Pipeline CI/CD |
| Filtros de artículos por autor, tag y favoritos | Módulos de pago, notificaciones u otros no existentes |
| Gestión de comentarios en artículos | |
| Sistema de favoritos y contador | |
| Listado de tags disponibles | |
| Control de acceso: solo el autor puede editar/eliminar sus recursos | |
| Validación de entradas: campos requeridos, formatos, rangos | |
| Verificación de códigos de estado HTTP (200, 201, 400, 401, 404, 422) | |
| Verificación de la estructura del JSON de respuesta (contrato de la API) | |
`
### **2.3 Referencias**
`
- RealWorld Spec (especificación funcional de la API Conduit): https://realworld-docs.netlify.app/docs/specs/backend-specs/endpoints
- Repositorio público del SUT: FastAPI RealWorld Example App (GitHub)
- `docs_qa/Plan_De_Accion.md` — Hoja de ruta interna del equipo QA
- `docs_qa/Contexto_Clase.md` — Compendio técnico ISTQB (apuntes de clase)
- Directrices del Taller de Pruebas de Software (Docente Yury Montoya Pérez)
`
### **2.4 Contexto de Negocio e Impacto Operacional**
`
El Sistema Bajo Prueba (SUT) constituye el núcleo transaccional backend de una **plataforma social de publicación y consumo de contenidos editoriales (estilo Medium / Substack)**. En este modelo de negocio digital, el valor de la empresa, la retención de usuarios y la monetización dependen directamente de la **propiedad intelectual de los autores**, la **privacidad editorial** y la **confianza transaccional**.
`
Desde la perspectiva de aseguramiento de calidad (QA), el testing no es un ejercicio abstracto de verificación sintáctica, sino una salvaguarda de los activos críticos del negocio:
`
`
+------------------------------------------------------------------------------------------+
|                        PIRÁMIDE DE IMPACTO EN EL MODELO DE NEGOCIO                       |
+------------------------------------------------------------------------------------------+
| 1. PROPIEDAD INTELECTUAL E INTEGRIDAD:                                                   |
|    - Autoría inviolable: Un usuario jamás debe alterar o borrar contenido ajeno.        |
|    - Riesgo de Negocio: Demandas por plagio, sabotaje editorial y fuga masiva de autores|
|      (Riesgo Extremo / Severidad Crítica -> BUG-03, BUG-04).                             |
+------------------------------------------------------------------------------------------+
| 2. DISPONIBILIDAD Y CONTROL DE ACCESO (GATEWAY):                                         |
|    - Acceso continuo (Auth JWT) y protección de feeds privados.                          |
|    - Riesgo de Negocio: Suplantación de identidad, consumo indebido de APIs y caída de   |
|      infraestructura por abuso de peticiones masivas (BVA limit=100 -> BUG-09, BUG-07).  |
+------------------------------------------------------------------------------------------+
| 3. ENGAGEMENT Y DINÁMICA SOCIAL:                                                         |
|    - Interacciones: Favoritos, contadores, seguimiento de autores (Follow/Unfollow).     |
|    - Riesgo de Negocio: Pérdida de tracción algorítmica y frustración de la comunidad    |
|      (Severidad Media -> BUG-05, BUG-06, BUG-08).                                        |
+------------------------------------------------------------------------------------------+
| 4. CONFORMIDAD TÉCNICA Y ESTÁNDARES REST:                                                |
|    - Códigos HTTP semánticos (201 Created vs 200 OK).                                    |
|    - Riesgo de Negocio: Inconsistencia menor en clientes frontend (Baja severidad -> 01) |
+------------------------------------------------------------------------------------------+
`
`
Esta jerarquización de impacto en el negocio determina y justifica analíticamente la asignación objetiva de **Severidad técnica** y **Prioridad de negocio** en cada defecto documentado.
`
---
`
## **3. Objetivos de Prueba**
`
| **#** | **Objetivo** | **Criterio de Éxito** |
|---|---|---|
| **1** | Verificar que los 19 endpoints de la API operan conforme al contrato de la especificación RealWorld. | ≥ 95% de los 41 casos de prueba ejecutados. |
| **2** | Identificar y documentar todos los defectos presentes en el sistema mediante la ejecución de la suite de pruebas. | Todos los defectos encontrados registrados y clasificados en MantisBT al cierre del ciclo. |
| **3** | Validar los mecanismos de autorización: solo los recursos propios pueden ser modificados o eliminados por su autor. | 0 defectos de seguridad/autorización abiertos al cierre del ciclo. |
| **4** | Verificar que las validaciones de entrada rechazan correctamente datos inválidos con el código HTTP apropiado. | Los casos de validación (EP/BVA) retornan el status code esperado en el 100% de los casos. |
| **5** | Generar métricas cuantitativas del proceso de pruebas para el análisis de calidad del software. | Dashboard de métricas generado con datos reales de pytest-cov y pytest-json-report. |
`
---
`
## **4. Roles y Responsabilidades del Equipo de Pruebas**
`
| **Rol** | **Nombre / Asignado a** | **Responsabilidades** | **Participación** |
|---|---|---|---|
| **QA Lead / Automatizador** | Juan Pablo Velásquez Ramírez | Planificar y coordinar las actividades de prueba. Co-diseñar los casos de prueba. Desarrollar y ejecutar los 26 scripts de prueba automatizados (pytest). Configurar el ambiente de pruebas (Docker, PostgreSQL). Ejecutar pruebas manuales técnicas (flujos de autorización, tokens JWT). Generar los archivos de datos para el dashboard (pytest-json-report, pytest-cov) y el análisis técnico de cierre. | 100% |
| **QA Analyst / Bug Manager** | Niurka Liseth Mejía Vargas | Co-elaborar y estructurar la documentación maestra del Plan de Pruebas. Co-diseñar, revisar y validar el catálogo de 41 casos de prueba (Casos_De_Prueba.md). Co-ejecutar pruebas manuales exploratorias (Swagger UI y Postman). Registrar, clasificar y gestionar los defectos en MantisBT adjuntando evidencias. Construir el dashboard de métricas y co-redactar el informe de análisis de calidad. | 100% |
| **Supervisora / Aprobadora** | Yury Montoya Pérez | Revisar y aprobar el plan de pruebas. Validar que los entregables cumplen los criterios académicos. Aprobar el cierre del ciclo de pruebas. | Según cronograma académico |
`
### **4.1 Matriz RACI**
`
La siguiente matriz define quién es Responsable (R), Aprobador (A), Consultado (C) e Informado (I) en cada actividad clave del proceso de pruebas.
`
| **Actividad** | **QA Lead / Automatizador** | **QA Analyst / Bug Manager** | **Docente** |
|---|---|---|---|
| Planificación y redacción del plan de pruebas | **R/A** | **R** | **C** |
| Diseño y documentación de casos de prueba | **R** | **R/A** | **C** |
| Revisión y validación de casos de prueba | **C** | **R/A** | **I** |
| Preparación del ambiente (Docker, pytest) | **R/A** | **I** | **I** |
| Ejecución de pruebas manuales exploratorias | **C** | **R** | **I** |
| Ejecución de pruebas manuales técnicas | **R** | **C** | **I** |
| Ejecución de pruebas automatizadas | **R/A** | **I** | **I** |
| Registro de defectos en MantisBT | **C** | **R/A** | **I** |
| Generación de datos para dashboard | **R** | **C** | **I** |
| Construcción del dashboard de métricas | **I** | **R** | **I** |
| Análisis de calidad y cierre | **R** | **R** | **A** |
`
_Leyenda: R = Responsable de ejecutar  A = Aprobador  C = Consultado  I = Informado_
`
---
`
## **5. Estrategia de Pruebas y Ciclo de Vida (STLC)**
`
### **5.1 Alineación Metodológica con el Ciclo de Vida de Pruebas (STLC)**
`
Conforme a las directrices doctrinarias del ISTQB y los fundamentos normativos de aseguramiento de calidad, este proceso de pruebas se estructuró a lo largo de las **cinco fases secuenciales del STLC (Software Testing Life Cycle)** y sus **dos fases transversales de gestión**:
`
`
+-----------------------------------------------------------------------------------------+
|                  FASES METODOLÓGICAS DEL STLC APLICADAS EN ESTE PROYECTO                |
+------------------------------------+----------------------------------------------------+
| Fase del STLC                      | Actividades Concretas y Artefactos Producidos      |
+------------------------------------+----------------------------------------------------+
| 1. Test Analysis (¿Qué probar?)    | - Análisis de la especificación RealWorld (19 eps).|
|                                    | - Delimitación de alcance funcional y bases de test|
|                                    | - Salida: Condiciones de prueba analizadas en §2.2 |
+------------------------------------+----------------------------------------------------+
| 2. Test Design (¿Cómo probar?)     | - Diseño de 41 Casos de Prueba (26 auto + 15 man). |
|                                    | - Aplicación de técnicas: EP, BVA, Tablas, Estados.|
|                                    | - Salida: Especificación en Casos_De_Prueba     |
+------------------------------------+----------------------------------------------------+
| 3. Test Implementation (¿Listo?)   | - Construcción de suite pytest (tests/) + fixtures.|
|                                    | - Aislamiento en Docker (PostgreSQL 5433/5434).    |
|                                    | - Preparación de datos de prueba y colección Postman|
+------------------------------------+----------------------------------------------------+
| 4. Test Execution (Actual vs Exp)  | - Ejecución automatizada con pytest runner (28.95s)|
|                                    | - Ejecución manual interactiva en Swagger UI (15 CP|
|                                    | - Generación de evidencias gráficas y HTML report. |
|                                    | - Salida: pytest_results.json, coverage.json.      |
+------------------------------------+----------------------------------------------------+
| 5. Test Completion (Cierre formal) | - Registro de 9 defectos en MantisBT.              |
|                                    | - Evaluación formal de Criterios de Salida (Exit). |
|                                    | - Test Summary Report y Dictamen Go / No-Go en §14 |
|                                    | - Empaquetado y archivo del testware completo.     |
+------------------------------------+----------------------------------------------------+
| Transversal 1: Test Planning       | - Definición de estrategia y recursos (este doc).  |
| Transversal 2: Monitoring & Control| - Supervisión de métricas (resumen_metricas.md).   |
+------------------------------------+----------------------------------------------------+
`
`
### **5.2 Principios del Testing (ISTQB) Reflejados en la Estrategia**
1. **Las pruebas muestran la presencia de defectos, no su ausencia:** Se demostró la existencia de fallos graves en control de acceso sin asumir corrección absoluta.
2. **Las pruebas exhaustivas son imposibles:** Se emplearon técnicas de caja negra (EP y BVA) para reducir infinitas combinaciones a clases de equivalencia representativas.
3. **Agrupamiento de defectos (*Defect Clustering*):** El módulo de Artículos concentró el 66.7% de los bugs (6 de 9 defectos), validando experimentalmente este principio.
4. **La paradoja del pesticida:** Se combinó la automatización de integración con exploración manual visual en Swagger para evitar puntos ciegos.
5. **Las pruebas dependen del contexto:** La profundidad de evaluación priorizó el modelo de negocio social y editorial de Conduit.
`
### **5.3 Tipos de Prueba**
`
| **Tipo de Prueba** | **Descripción** | **Responsable** | **Incluida** |
|---|---|---|---|
| **Prueba funcional** | Verifica que cada endpoint opera conforme al contrato de la API (status codes, estructura JSON, lógica de negocio). | QA Lead | [x] Sí |
| **Prueba de regresión** | La suite de pytest actúa como suite de regresión: garantiza que las funcionalidades validadas se mantienen estables y que los defectos corregidos no reaparecen en ejecuciones futuras. | QA Lead | [x] Sí |
| **Prueba de integración** | Valida la interacción entre múltiples módulos de la API en un flujo completo (ej. autenticación → creación de artículo → comentario → favorito). | QA Lead | [x] Sí |
| **Prueba de rendimiento** | Evalúa el comportamiento bajo carga y estrés. | N/A | [ ] No — fuera del alcance del proyecto |
| **Prueba de seguridad** | Identifica vulnerabilidades de autorización: acceso no autorizado a recursos ajenos, endpoints que no requieren autenticación debiendo hacerlo. | QA Lead | [x] Sí (alcance parcial) |
| **Prueba de usabilidad** | Para una API REST, se evalúa la usabilidad del contrato: claridad de mensajes de error, documentación de Swagger UI, consistencia de la estructura JSON de respuesta. | QA Lead | [x] Sí (adaptada a API) |
| **Prueba de aceptación (UAT)** | Validación formal con el usuario o cliente final. | N/A | [ ] No|
`
### **5.4 Técnicas de Diseño de Casos de Prueba**
`
- **Partición de equivalencia (EP):** Se aplica en módulos de autenticación y validación de campos (ej. emails válidos vs. inválidos, contraseñas vacías vs. con valor).
- **Análisis de valores límite (BVA):** Se aplica en el parámetro `limit` de `GET /api/articles` (límite máximo = 20) y en longitudes de campos de texto.
- **Tabla de decisión:** Se aplica en pruebas de autorización (usuario autenticado/no autenticado × recurso propio/ajeno) y en combinaciones de filtros de artículos (`?tag`, `?author`, `?favorited`).
- **Prueba de transición de estados:** Se aplica en flujos de follow/unfollow (estado `following`: false → true → false) y favoritos (estado `favorited` + contador `favoritesCount`).
- **Prueba exploratoria:** Se aplica en casos manuales donde se buscan comportamientos no especificados (slugs con caracteres especiales, tokens JWT manipulados, mensajes de error bajo entradas inesperadas).
`
### **5.5 Niveles de Prueba**
`
- **Pruebas unitarias:** No aplica en este plan. El SUT no expone funciones puras aisladas; la lógica de negocio está integrada en los endpoints y repositorios.
- **Pruebas de integración:** Juan Pablo Velásquez Ramírez — pytest 9.x + httpx (FastAPI TestClient). Validan la interacción entre endpoints, ORM (SQLAlchemy), base de datos y capa de seguridad (JWT).
- **Pruebas de sistema:** Juan Pablo Velásquez Ramírez — Swagger UI / Postman. Validan el comportamiento del sistema completo desde la perspectiva de un cliente externo de la API.
- **Pruebas de aceptación:** No aplica en este proyecto académico.
`
### **5.6 Criterios de Suspensión y Requisitos de Reanudación**
`
Los criterios de suspensión definen las condiciones bajo las cuales se suspende la ejecución de pruebas; los criterios de reanudación determinan cuándo puede continuar.
`
| **Criterios de Suspensión** | **Requisitos de Reanudación** |
|---|---|
| La API no levanta correctamente en el entorno local (Docker Compose falla o la aplicación no responde en localhost:8000). | El entorno ha sido restaurado, la API responde con HTTP 200 en `GET /api/tags` (smoke test). |
| Defecto crítico no inyectado intencionalmente que impide la ejecución de casos de prueba. | El defecto ha sido identificado, documentado en MantisBT y aislado para continuar con los casos no bloqueados. |
| Ambiente de pruebas inestable (BD corrompida, fixtures de pytest fallando). | La BD de pruebas ha sido reinicializada y los fixtures validan correctamente. |
| Más del 30% de los casos automatizados fallan por causas no relacionadas con los bugs inyectados. | Se ha identificado la causa raíz (configuración, dependencias) y se ha corregido el entorno. |
| Cambio en la estrategia de bugs inyectados que invalida casos de prueba ya diseñados. | Los casos de prueba afectados han sido actualizados y revisados. |
`
### **5.7 Completitud de las Pruebas (Evaluación Real)**
`
| **Criterio de Completitud** | **Meta / Umbral** | **Valor Actual** | **Cumplido** |
|---|---|---|---|
| Todos los casos de prueba diseñados han sido ejecutados. | **≥ 95%** (39/41 mínimo) | — | [ ] |
| Tasa de casos aprobados sobre los casos que NO involucran bugs inyectados. | **≥ 90%** | — | [ ] |
| Todos los defectos encontrados están registrados en MantisBT con severidad y prioridad asignadas. | **100%** | — | [ ] |
| 0 defectos críticos sin documentar en MantisBT al cierre. | **= 0** | — | [ ] |
| Cobertura de código medida con pytest-cov alcanza el umbral definido. | **≥ 70%** | — | [ ] |
| Archivos de datos para el dashboard generados (`pytest_results.json`, `coverage.json`). | **Generados** | — | [ ] |
| Todos los defectos registrados en MantisBT tienen estado Resolved o Closed. | **100%** | — | [ ] |
| Informe de análisis de calidad (`Analisis_Calidad.md`) redactado y entregado. | **Entregado** | — | [ ] |
`
---
`
## **6. Criterios de Entrada y Salida**
`
| **Criterios de Entrada (para iniciar pruebas)** | **Criterios de Salida (para finalizar pruebas)** |
|---|---|
| La API responde correctamente en `http://localhost:8000` (Docker Compose activo). | ≥ 95% de los 41 casos de prueba ejecutados. |
| El sistema bajo prueba opera de forma estable y todas las funcionalidades principales responden ante las peticiones. | Todos los defectos encontrados registrados y clasificados en MantisBT. |
| Los 41 casos de prueba están documentados en `docs_qa/Casos_De_Prueba.md`. | 0 defectos de severidad Crítica sin documentar. |
| MantisBT está configurado y accesible para el equipo. | Archivos `pytest_results.json` y `coverage.json` generados. |
| Los fixtures de pytest (`tests/conftest.py`) están configurados y la BD de pruebas inicializa correctamente. | Informe de análisis de calidad redactado y entregado. |
| La colección `postman.json` está importada en Postman. | Aprobación del cierre por parte de la docente. |
`
---
`
## **7. Casos de Prueba**

Los 41 casos de prueba (15 manuales + 26 automatizados) se encuentran especificados detalladamente —incluyendo precondiciones, datos de entrada, pasos de ejecución, resultado esperado y evidencias— en el artefacto [docs_qa/Casos_De_Prueba.md](Casos_De_Prueba.md). A continuación se consolida el **Registro Maestro de Ejecución**.

### **7.1 Registro Consolidado de Casos de Prueba**

**Pruebas Manuales (15)**
`
| **ID** | **Nombre del Caso** | **Módulo** | **Prioridad** | **Estado** | **Defecto** |
|---|---|---|---|---|---|
| **CP-EXP-M-001** | Flujo completo happy path: registro → login → crear artículo → seguir usuario → ver feed → comentar → marcar favorito | Exploratorio | Alta | **Falló** | BUG-01, BUG-05, BUG-06, BUG-07 |
| **CP-EXP-M-002** | Enviar títulos con caracteres especiales (emojis, HTML, unicode) y observar slugs generados | Exploratorio | Media | **Pasó** | N/A |
| **CP-EXP-M-003** | Requests con tokens JWT manipulados: expirado, firma inválida, token de otro proyecto | Exploratorio | Alta | **Pasó** | N/A |
| **CP-EXP-M-004** | BVA: crear 25 artículos y solicitar `GET /api/articles?limit=100`; contar resultados manualmente | Exploratorio | Media | **Falló** | BUG-09 |
| **CP-EXP-M-005** | Crear artículos con títulos similares ("Mi Blog" y "mi blog") y observar colisión de slugs | Exploratorio | Baja | **Pasó** | N/A |
| **CP-TOOL-M-001** | Verificar en Swagger UI que los 19 endpoints están documentados correctamente | Herramientas | Media | **Pasó** | N/A |
| **CP-TOOL-M-002** | Usar botón Authorize de Swagger UI con token JWT y ejecutar 3 endpoints autenticados | Herramientas | Alta | **Pasó** | N/A |
| **CP-TOOL-M-003** | Importar `postman.json` en Postman y ejecutar la colección completa end-to-end | Herramientas | Alta | **Pasó** | N/A |
| **CP-QUAL-M-001** | Evaluar calidad y claridad de mensajes de error con datos inválidos en cada módulo | Calidad | Media | **Pasó** | N/A |
| **CP-QUAL-M-002** | Verificar estructura completa del JSON de respuesta de cada módulo vs. RealWorld Spec | Calidad | Alta | **Pasó** | N/A |
| **CP-QUAL-M-003** | Con dos usuarios: intentar editar artículo ajeno autenticado como no-autor (Swagger UI) | Calidad | Alta | **Falló** | BUG-03 |
| **CP-QUAL-M-004** | Con dos usuarios: intentar eliminar artículo ajeno autenticado como no-autor (Swagger UI) | Calidad | Crítica | **Falló** | BUG-04 |
| **CP-EST-M-001** | Flujo follow → unfollow verificando transición de `following`: false → true → false | Estados | Media | **Falló** | BUG-06 |
| **CP-EST-M-002** | Flujo marcar favorito → desmarcar; verificar `favorited` y `favoritesCount` en cada paso | Estados | Media | **Falló** | BUG-05 |
| **CP-EST-M-003** | Eliminar artículo propio y luego solicitar `GET /api/articles/{slug}`; verificar 404 | Estados | Media | **Pasó** | N/A |
`
**Pruebas Automatizadas (26)**
`
| **ID** | **Nombre del Caso** | **Módulo** | **Prioridad** | **Estado** | **Defecto** |
|---|---|---|---|---|---|
| **CP-AUTH-A-001** | Registro exitoso retorna HTTP 201 Created (no 200) | Auth | Alta | **Falló** | BUG-01 |
| **CP-AUTH-A-002** | Registro exitoso retorna token JWT en el body de respuesta | Auth | Alta | **Pasó** | N/A |
| **CP-AUTH-A-003** | Login con credenciales válidas retorna token JWT | Auth | Alta | **Pasó** | N/A |
| **CP-AUTH-A-004** | Login con email inexistente retorna HTTP 400 | Auth | Alta | **Pasó** | N/A |
| **CP-AUTH-A-005** | Registro con email duplicado retorna HTTP 400 | Auth | Alta | **Pasó** | N/A |
| **CP-ART-A-001** | Crear artículo con datos válidos retorna 200 con estructura correcta (slug, author, tagList) | Articles | Alta | **Pasó** | N/A |
| **CP-ART-A-002** | Crear artículo con título vacío (`""`) retorna HTTP 422 Unprocessable Entity | Articles | Alta | **Falló** | BUG-02 |
| **CP-ART-A-003** | Crear artículo sin token de autenticación retorna HTTP 401 | Articles | Alta | **Pasó** | N/A |
| **CP-ART-A-004** | Editar artículo como autor legítimo retorna artículo actualizado | Articles | Alta | **Pasó** | N/A |
| **CP-ART-A-005** | Editar artículo de otro usuario retorna HTTP 400 | Articles | Alta | **Falló** | BUG-03 |
| **CP-ART-A-006** | Eliminar artículo de otro usuario retorna HTTP 400 | Articles | Crítica | **Falló** | BUG-04 |
| **CP-ART-A-007** | Acceder a `GET /api/articles/feed` sin token retorna HTTP 401 | Articles | Alta | **Falló** | BUG-07 |
| **CP-ART-A-008** | `GET /api/articles?tag=X` retorna solo artículos etiquetados con el tag X | Articles | Media | **Falló** | BUG-08 |
| **CP-ART-A-009** | `GET /api/articles?limit=100` con 25+ artículos en BD retorna máximo 20 | Articles | Media | **Falló** | BUG-09 |
| **CP-COM-A-001** | Crear comentario en artículo existente retorna el comentario con autor y body | Comments | Media | **Pasó** | N/A |
| **CP-COM-A-002** | Crear comentario sin autenticación retorna HTTP 401 | Comments | Media | **Pasó** | N/A |
| **CP-COM-A-003** | Eliminar comentario propio retorna HTTP 200 sin errores | Comments | Media | **Pasó** | N/A |
| **CP-COM-A-004** | Obtener comentarios de artículo inexistente retorna HTTP 404 | Comments | Media | **Pasó** | N/A |
| **CP-PRF-A-001** | Seguir a un usuario cambia el campo `following` a `true` en la respuesta | Profiles | Media | **Falló** | BUG-06 |
| **CP-PRF-A-002** | Dejar de seguir a un usuario cambia el campo `following` a `false` | Profiles | Media | **Falló** | BUG-06 |
| **CP-PRF-A-003** | Obtener perfil de usuario inexistente retorna HTTP 404 | Profiles | Media | **Pasó** | N/A |
| **CP-PRF-A-004** | Seguir usuario sin autenticación retorna HTTP 401 | Profiles | Media | **Pasó** | N/A |
| **CP-FAV-A-001** | Marcar artículo como favorito incrementa `favoritesCount` en 1 y `favorited` = true | Favorites | Media | **Falló** | BUG-05 |
| **CP-FAV-A-002** | Desmarcar artículo favorito decrementa `favoritesCount` en 1 y `favorited` = false | Favorites | Media | **Falló** | BUG-05 |
| **CP-TAG-A-001** | `GET /api/tags` retorna una lista de tags existentes en la BD | Tags | Baja | **Pasó** | N/A |
| **CP-TAG-A-002** | Tags asignados al crear un artículo aparecen en `GET /api/tags` | Tags | Baja | **Pasó** | N/A |
`
**Total: 41 casos de prueba (15 manuales + 26 automatizados)**
`
---
`
## **8. Gestión de Defectos**
`
### **8.1 Clasificación de Defectos**
`
La clasificación se define en función del impacto en el negocio de la plataforma (blogs tipo Medium):
`
| **Severidad** | **Descripción aplicada al SUT** | **Tiempo de Resolución** |
|---|---|---|
| **Crítica** | El sistema expone una brecha de seguridad (cualquier usuario puede eliminar contenido ajeno), o un flujo de negocio principal es completamente inutilizable. | Inmediata — mismo día |
| **Alta** | Una funcionalidad importante de negocio no opera correctamente (artículos sin validación de título, feed sin autenticación, autoría ignorada en edición). | 24–48 horas |
| **Media** | Una funcionalidad secundaria falla o el contrato de la API no es el esperado (estado `following` incorrecto, filtro de tags ignorado, límite de paginación ignorado). | 3–5 días hábiles |
| **Baja** | Inconsistencia menor que no afecta funcionalidad: violación del estándar REST en status codes (200 vs 201). | Próxima versión |
`
### **8.2 Trazabilidad de Reportes en MantisBT**

Los 9 defectos detectados durante el ciclo de ejecución se encuentran documentados con su evidencia fotográfica y trazabilidad hacia los casos de prueba en [docs_qa/Fichas_De_Bugs_MantisBT.md](Fichas_De_Bugs_MantisBT.md), y gestionados formalmente en la plataforma **MantisBT** por Niurka Liseth Mejía Vargas con apoyo técnico de Juan Pablo Velásquez Ramírez.

---

## **9. Entregables de Prueba**

| **Entregable** | **Descripción** | **Fase STLC** | **Responsable** | **Fecha Real** |
|---|---|---|---|---|
| **Plan de Pruebas** | Este documento: alcance, contexto de negocio, estrategia STLC, cronograma y cierre formal. | Planificación / Cierre | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas | 09/11/2026 |
| **Plan de Acción** | Hoja de ruta interna con estrategia de bugs, distribución de casos y convenciones (docs_qa/Plan_De_Accion.md). | Planificación | Juan Pablo Velásquez Ramírez | 26/10/2025 |
| **Casos de Prueba** | 41 casos documentados con precondiciones, pasos y resultados reales (docs_qa/Casos_De_Prueba.md). | Diseño / Ejecución | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas | 09/11/2026 |
| **Scripts de Prueba Automatizados** | 26 scripts de integración con pytest en 	ests/ organizados por módulo. | Implementación | Juan Pablo Velásquez Ramírez | 09/11/2026 |
| **Registro de Defectos (MantisBT)** | 9 tickets cargados y clasificados en MantisBT con sus respectivas evidencias (docs_qa/Fichas_De_Bugs_MantisBT.md). | Ejecución | Niurka Liseth Mejía Vargas | 09/11/2026 |
| **Evidencias de Pruebas Manuales** | Capturas de Swagger UI documentando hallazgos y bugs (docs_qa/evidencias/). | Ejecución | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas | 09/11/2026 |
| **Datos de Métricas y Reportes** | Archivos pytest_results.json, coverage.json y 	est_report.html (docs_qa/data/, docs_qa/reports/). | Cierre | Juan Pablo Velásquez Ramírez | 09/11/2026 |
| **Dashboard de Métricas** | Visualización interactiva de los KPIs y severidad de defectos generada a partir de los datos exportados. | Cierre | Niurka Liseth Mejía Vargas / Juan Pablo Velásquez Ramírez | 09/11/2026 |
| **Análisis de Calidad** | Informe ejecutivo (Test Summary Report) sobre madurez y riesgo de negocio (docs_qa/Analisis_Calidad.md). | Cierre | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas | 09/11/2026 |

---

## **10. Recursos y Ambiente de Prueba**
`
### **10.1 Equipo de Pruebas**
`
| **Nombre** | **Rol** | **Responsabilidades** | **Dedicación** |
|---|---|---|---|
| Juan Pablo Velásquez Ramírez | QA Lead / QA Analyst / QA Automatizador | Diseño, ejecución manual, automatización, inyección de bugs, generación de métricas | 100% |
| Niurka Liseth Mejía Vargas | QA Analyst / Bug Manager | Co-diseño de casos de prueba y documentación del Plan, ejecución exploratoria, gestión de tickets en MantisBT y dashboard de métricas | 100% |
`
### **10.2 Herramientas**
`
| **Categoría** | **Herramienta** | **Propósito** |
|---|---|---|
| **Pruebas manuales — Documentación interactiva** | Swagger UI (`http://localhost:8000/api/`) | Explorar y ejecutar endpoints manualmente; verificar documentación de la API |
| **Pruebas manuales — Cliente HTTP** | Postman + colección `postman.json` | Ejecutar y documentar casos manuales; colección pre-existente en el repositorio |
| **Pruebas automatizadas — Framework** | pytest 9.x + pytest-asyncio | Ejecutar la suite de 26 tests automatizados con soporte async |
| **Pruebas automatizadas — Cliente HTTP** | httpx + FastAPI TestClient | Realizar peticiones HTTP dentro de los tests de pytest |
| **Cobertura de código** | pytest-cov | Medir el porcentaje de código fuente ejercitado por los tests |
| **Reporte de resultados** | pytest-json-report | Exportar resultados de ejecución en JSON para el dashboard |
| **Gestión de defectos** | MantisBT | Registro, clasificación y seguimiento de los 9 defectos detectados |
| **Control de versiones** | Git (ramas `main` y `buggy-version`) | Aislar el código con bugs del código limpio |
| **Gestor de dependencias** | uv (pyproject.toml) | Instalar y gestionar dependencias Python de forma reproducible |
| **Entorno de ejecución** | Docker + Docker Compose | Levantar la API y PostgreSQL con un solo comando |
`
### **10.3 Ambiente de Prueba**
`
| **Ambiente** | **URL / Servidor** | **Versión** | **Responsable** |
|---|---|---|---|
| **Local — Desarrollo / QA** | `http://localhost:8000` | Python 3.14, FastAPI 0.115+, PostgreSQL (psycopg3), Docker Compose | Juan Pablo Velásquez Ramírez |
`
_Nota: Este proyecto opera en un entorno local único. No hay ambientes de Staging ni Producción._
| **Documentación interactiva** | `http://localhost:8000/api/` (Swagger UI) | Generada automáticamente por FastAPI | Juan Pablo Velásquez Ramírez |
`
`
`
---
`
## **11. Cronograma Real de Ejecución de Pruebas**

| **Actividad / Hito del STLC** | **Fecha Inicio** | **Fecha Fin** | **Responsable** | **Estado Final** |
|---|---|---|---|---|
| **STLC Fase 1:** Planificación (Plan de Acción + Plan de Pruebas) | 26/10/2025 | 02/11/2026 | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas | ✅ **Completado (100%)** |
| **STLC Fase 2:** Diseño y documentación de los 41 casos de prueba | 03/11/2026 | 06/11/2026 | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas | ✅ **Completado (100%)** |
| **STLC Fase 3:** Preparación del ambiente (Docker, pytest, MantisBT) | 07/11/2026 | 08/11/2026 | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas | ✅ **Completado (100%)** |
| **STLC Fase 4:** Ejecución de 15 pruebas manuales (Swagger / Postman) | 09/11/2026 | 09/11/2026 | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas | ✅ **Completado (100%)** |
| **STLC Fase 4:** Desarrollo y ejecución de 26 pruebas automatizadas (pytest) | 09/11/2026 | 09/11/2026 | Juan Pablo Velásquez Ramírez | ✅ **Completado (100%)** |
| **STLC Fase 4:** Carga y clasificación de defectos en MantisBT | 09/11/2026 | 09/11/2026 | Niurka Liseth Mejía Vargas | ✅ **Completado (100%)** |
| **STLC Fase 5:** Generación de datos JSON y Dashboard de métricas | 09/11/2026 | 09/11/2026 | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas | ✅ **Completado (100%)** |
| **STLC Fase 5:** Redacción del Análisis de Calidad y Cierre formal | 09/11/2026 | 09/11/2026 | Juan Pablo Velásquez Ramírez / Niurka Liseth Mejía Vargas | ✅ **Completado (100%)** |

---

## **12. Riesgos y Mitigación**
`
| **#** | **Riesgo** | **Probabilidad** | **Impacto** | **Plan de Mitigación** |
|---|---|---|---|---|
| **1** | La API no levanta en el entorno local (Docker o PostgreSQL fallan). | Media | Alto | Usar SQLite como BD alternativa para la suite de pytest; documentar la configuración paso a paso en el README de pruebas. |
| **2** | Los bugs inyectados no son detectados por los tests (diseño de casos insuficiente). | Baja | Alto | Verificar antes de ejecutar que cada bug tiene al menos un caso asociado en la columna "Defecto" del §7.2. Ejecutar un smoke test manual de cada bug primero. |
| **3** | Un bug inyectado rompe la aplicación completamente (impide ejecutar el resto de tests). | Baja | Alto | Inyectar y probar los bugs uno por uno antes de hacer el commit conjunto. Mantener la rama `main` intacta como punto de rollback. |
| **4** | Falta de tiempo para completar los 26 scripts automatizados. | Media | Medio | Priorizar módulos Auth y Articles (mayor severidad). Los módulos Tags (2 casos) y Favorites (2 casos) pueden reducirse si hay restricción de tiempo. |
| **5** | Dificultad con la configuración de pytest-asyncio para tests async. | Media | Medio | Revisar la configuración existente en `tests/conftest.py` y `pyproject.toml`; la base de fixtures ya está implementada en el repositorio. |
`
---
`
## **13. Métricas de Calidad**
`
| **Métrica** | **Fórmula / Medición** | **Meta** | **Valor Real (buggy-version)** | **Cumplimiento** |
|---|---|---|---|---|
| **Tasa de ejecución global** | (41 ejecutados / 41 planificados) × 100 | **≥ 95%** | **100.0%** (41 / 41) | ✅ Superada |
| **Tasa de ejecución automatizada** | (26 ejecutados / 26 planificados) × 100 | **100%** | **100.0%** (26 / 26) | ✅ Conforme |
| **Tasa de ejecución manual** | (15 ejecutados / 15 planificados) × 100 | **100%** | **100.0%** (15 / 15) | ✅ Conforme |
| **Tasa de casos aprobados (Global)** | (24 pasaron / 41 ejecutados) × 100 | ~55% - 60% | **58.54%** (24 / 41) | ✅ Conforme (cazando bugs) |
| **Tasa de casos fallidos (Global)** | (17 fallaron / 41 ejecutados) × 100 | ~40% - 45% | **41.46%** (17 / 41) | ✅ Alta capacidad detectora |
| **Tasa de detección de bugs inyectados** | (9 bugs detectados / 9 inyectados) × 100 | **100%** | **100.0%** (9 / 9) | ✅ Óptimo (100% detección) |
| **Densidad de defectos (Global)** | 9 defectos / 41 casos ejecutados | ~0.20 – 0.30 | **0.220** defectos/caso | ✅ Rango normal |
| **Defectos críticos detectados** | Conteo directo (Severidad Crítica) | ≥ 0 | **1** (BUG-04: borrado no autorizado) | 🚨 Prioridad inmediata |
| **Cobertura de código (pytest-cov)** | Líneas ejercitadas / Total líneas backend | **≥ 70%** | **82.78%** (553 / 668 líneas) | ✅ Superada (+12.78%) |
| **Cobertura de endpoints** | (19 probados / 19 existentes) × 100 | **100%** | **100.0%** (19 / 19 endpoints) | ✅ Totalidad cubierta |
| **Tiempo de suite automatizada** | Ejecución en pytest con reportes | **< 60s** | **28.95 segundos** | ✅ Alto rendimiento |
`
---
`
## **14. Cierre Formal del STLC (Test Completion Report) y Dictamen de Negocio**
`
### **14.1 Evaluación de Criterios de Salida (*Exit Criteria*)**
De acuerdo con el estándar ISO/IEC/IEEE 29119 y las pautas de ISTQB, la fase de cierre certifica que:
1. **Completitud Operacional:** Se ejecutaron los 41 casos planificados (100%), satisfaciendo el umbral mínimo exigido ($\ge 95\%$).
2. **Cobertura Estructural:** Se alcanzó un **82.78%** de cobertura de código en el backend mediante pytest-cov, superando la meta fijada del 70%.
3. **Eficacia Detectora:** Se aislaron, clasificaron y documentaron con evidencia gráfica el 100% de los defectos inyectados (9 de 9).
4. **Trazabilidad:** Se garantizó la trazabilidad bidireccional entre Requisitos RealWorld -> Casos de Prueba -> Reportes de MantisBT -> Líneas de código.
`
### **14.2 Dictamen de Negocio para Pase a Producción (Go / No-Go)**
> ### 🛑 DICTAMEN DE QA: NO-GO (RECHAZADO PARA DESPLIEGUE A PRODUCCIÓN)
> 
> **Fundamentación de Negocio:**
> A pesar de que los módulos de autenticación, comentarios y etiquetas muestran estabilidad, el sistema presenta **fallas estructurales críticas de control de acceso en el módulo de Artículos (BUG-03 y BUG-04)**:
> - Cualquier usuario registrado puede **modificar** o **eliminar permanentemente** las publicaciones de otros autores sin validación de autoría (Vulnerabilidad OWASP API1:2023 - Broken Object Level Authorization).
> - Desplegar la API en su estado actual acarrearía la destrucción inmediata de la base de contenidos editoriales, violación de acuerdos de confidencialidad y pérdida irreversible de la reputación comercial de la plataforma.
> 
> **Condiciones Obligatorias para Reanudación y Re-testing:**
> 1. Aplicar los parches de seguridad en pp/api/routes/articles.py restituyendo la verificación de autoría (current_user.id == article.author_id).
> 2. Corregir la gestión de excepciones en el módulo de favoritos (pp/services/articles.py).
> 3. Ejecutar una **ronda de Pruebas de Regresión Completa** sobre la versión corregida para validar el cierre de los 9 tickets en MantisBT.
`

`
## **15. Términos y Acrónimos**
`
### **15.1 Términos**
`
| **Término** | **Definición** |
|---|---|
| **Caso de prueba** | Conjunto de condiciones, datos de entrada, pasos de ejecución y resultado esperado que valida una funcionalidad específica del sistema. |
| **Ciclo de pruebas** | Periodo de tiempo durante el cual se planifican, diseñan, ejecutan y evalúan las actividades de prueba para una entrega o versión del sistema. |
| **Criterio de aceptación** | Condiciones definidas que un sistema o funcionalidad debe cumplir para ser aceptado por el cliente o usuario final. |
| **Datos de prueba** | Conjunto de valores de entrada utilizados durante la ejecución de un caso de prueba para verificar el comportamiento del sistema. |
| **Defecto / Bug** | Discrepancia entre el comportamiento real del sistema y el comportamiento esperado según los requisitos o la especificación. |
| **Entorno de pruebas** | Conjunto de hardware, software, datos y configuraciones utilizados para ejecutar las pruebas. En este proyecto: Docker Compose + Python 3.14 + PostgreSQL local. |
| **Evidencia de prueba** | Artefactos generados durante la ejecución de pruebas que sirven como registro del resultado: screenshots de Swagger/Postman, output de pytest. |
`
| **Plan de pruebas** | Documento que describe el alcance, estrategia, recursos, cronograma y actividades del proceso de pruebas. |
| **Regresión** | Conjunto de pruebas ejecutadas para verificar que un cambio en el sistema no ha introducido nuevos defectos en funcionalidades ya validadas. |
| **Severidad** | Nivel de impacto técnico que un defecto tiene sobre el funcionamiento del sistema (Crítica / Alta / Media / Baja). |
| **Slug** | Cadena de texto derivada del título de un artículo, transformada en formato URL-friendly (sin espacios ni caracteres especiales). Ej: "Mi Artículo" → `mi-articulo`. Sirve como identificador único del artículo en los endpoints. |
| **Token JWT** | Credencial criptográfica de autenticación emitida por la API tras el login. Se incluye en el header `Authorization: Bearer {token}` de cada request a endpoints protegidos. |
`
### **15.2 Acrónimos**
`
| **Acrónimo** | **Significado** | **Descripción** |
|---|---|---|
| **API** | **Application Programming Interface** | Interfaz de programación de aplicaciones. Conjunto de reglas y endpoints que permiten la comunicación entre sistemas de software. |
| **BVA** | **Boundary Value Analysis** | Análisis de Valores Límite. Técnica de diseño de pruebas que evalúa los valores en los bordes de las particiones de equivalencia. |
| **CI/CD** | **Continuous Integration / Continuous Delivery** | Integración y entrega continua. Práctica de automatizar la integración, prueba y despliegue del software. |
| **EP** | **Equivalence Partitioning** | Partición de equivalencia. Técnica de diseño de casos de prueba que divide los datos de entrada en grupos equivalentes. |
| **HTTP** | **Hypertext Transfer Protocol** | Protocolo de transferencia de hipertexto. Protocolo de comunicación sobre el que opera la API REST del SUT. |
| **JSON** | **JavaScript Object Notation** | Formato ligero de intercambio de datos utilizado en el cuerpo de todas las peticiones y respuestas de la API. |
| **JWT** | **JSON Web Token** | Estándar de token de autenticación. La API emite un JWT tras el login; los clientes lo envían en cada request autenticado. |
| **KPI** | **Key Performance Indicator** | Indicador Clave de Rendimiento. Métrica utilizada para medir el éxito de una actividad o proceso. |
| **QA** | **Quality Assurance** | Aseguramiento de la calidad. Proceso sistemático para garantizar que el software cumple los requisitos de calidad. |
| **RACI** | **Responsible, Accountable, Consulted, Informed** | Matriz de asignación de responsabilidades en actividades de un proyecto. |
| **REST** | **Representational State Transfer** | Estilo arquitectónico para diseñar APIs web. El SUT es una API REST que usa los verbos HTTP (GET, POST, PUT, DELETE) para operar sobre recursos. |
| **SUT** | **System Under Test** | Sistema bajo prueba. En este proyecto: la API FastAPI RealWorld Example App (Conduit) ejecutándose en la rama `buggy-version`. |
| **UAT** | **User Acceptance Testing** | Pruebas de Aceptación de Usuario. Fase de pruebas en la que el cliente valida que el sistema cumple sus necesidades. No aplica en este proyecto académico. |
`