# **PLAN DE PRUEBAS**

_FastAPI RealWorld Example App — Conduit (Backend API)_

| **Proyecto:** | FastAPI RealWorld Example App — Conduit (Backend API) |
|---|---|
| **Versión:** | 1.0 |
| **Fecha:** | 26/10/2025 |
| **Elaborado por:** | [Tu nombre] / [Nombre compañera] |
| **Revisado por:** | [Nombre compañera] |
| **Aprobado por:** | [Nombre docente] |
| **Estado:** | [x] Borrador  [ ] En revisión  [ ] Aprobado |

---

## **1. Historial de Cambios**

| **Versión** | **Fecha** | **Descripción del Cambio** | **Autor** | **Aprobado por** |
|---|---|---|---|---|
| 1.0 | 26/10/2025 | Versión inicial del plan de pruebas | [Tu nombre] | [Por aprobar] |

---

## **2. Introducción**

### **2.1 Propósito**

Este documento describe la estrategia, alcance, recursos, técnicas y actividades de prueba para el sistema **FastAPI RealWorld Example App (Conduit)**, en el marco del taller universitario de la materia Pruebas de Software. El propósito es garantizar que la API cumpla con los contratos de comportamiento esperados, y validar que los mecanismos de prueba diseñados son efectivos para detectar defectos reales en el sistema.

El proceso de pruebas combina ejecución manual exploratoria (Swagger UI / Postman) con automatización a nivel de integración (pytest), buscando detectar defectos en los módulos de autenticación, gestión de artículos, comentarios, perfiles, favoritos y tags. Los hallazgos se documentan en MantisBT y se analizan mediante métricas cuantitativas al cierre del ciclo.

### **2.2 Alcance**

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

### **2.3 Referencias**

- RealWorld Spec (especificación funcional de la API Conduit): https://realworld-docs.netlify.app/docs/specs/backend-specs/endpoints
- Repositorio público del SUT: FastAPI RealWorld Example App (GitHub)
- `docs_qa/Plan_De_Accion.md` — Hoja de ruta interna del equipo QA
- `docs_qa/Contexto_Clase.md` — Compendio técnico ISTQB (apuntes de clase)
- Plantilla de Plan de Pruebas suministrada por la docente (este documento)

### **2.4 Contexto de Negocio**

El SUT es el motor backend de una **plataforma de blogs tipo Medium**: una red social de escritura donde los usuarios crean y comparten artículos, siguen a otros autores, comentan publicaciones y guardan favoritos. Comprender el negocio es fundamental para definir la naturaleza, prioridad y severidad de las pruebas:

- Los flujos de **autenticación** y **creación de artículos** son críticos: su falla inutiliza toda la plataforma.
- El **control de acceso** (solo el autor puede editar/eliminar su contenido) es un pilar de integridad y confianza.
- Los módulos de **comentarios y favoritos** tienen impacto medio: afectan el engagement pero no bloquean el negocio.
- Las **tags** tienen impacto bajo: son un auxiliar de clasificación.

Esta jerarquía de impacto define directamente la severidad y prioridad asignadas a cada defecto detectado.

---

## **3. Objetivos de Prueba**

| **#** | **Objetivo** | **Criterio de Éxito** |
|---|---|---|
| **1** | Verificar que los 19 endpoints de la API operan conforme al contrato de la especificación RealWorld. | ≥ 95% de los 41 casos de prueba ejecutados. |
| **2** | Identificar y documentar todos los defectos presentes en el sistema mediante la ejecución de la suite de pruebas. | Todos los defectos encontrados registrados y clasificados en MantisBT al cierre del ciclo. |
| **3** | Validar los mecanismos de autorización: solo los recursos propios pueden ser modificados o eliminados por su autor. | 0 defectos de seguridad/autorización abiertos al cierre del ciclo. |
| **4** | Verificar que las validaciones de entrada rechazan correctamente datos inválidos con el código HTTP apropiado. | Los casos de validación (EP/BVA) retornan el status code esperado en el 100% de los casos. |
| **5** | Generar métricas cuantitativas del proceso de pruebas para el análisis de calidad del software. | Dashboard de métricas generado con datos reales de pytest-cov y pytest-json-report. |

---

## **4. Roles y Responsabilidades del Equipo de Pruebas**

| **Rol** | **Nombre / Asignado a** | **Responsabilidades** | **Participación** |
|---|---|---|---|
| **QA Lead / Automatizador** | [Tu nombre] | Planificar y coordinar las actividades de prueba. Diseñar los casos de prueba en conjunto con la analista. Desarrollar y ejecutar los 26 scripts de prueba automatizados (pytest). Configurar el ambiente de pruebas. Ejecutar pruebas manuales técnicas (flujos de autorización, tokens JWT). Generar los archivos de datos para el dashboard (pytest-json-report, pytest-cov). | 100% |
| **QA Analyst / Bug Manager** | [Nombre compañera] | Revisar y validar los casos de prueba diseñados antes de la ejecución. Co-ejecutar pruebas manuales exploratorias (Swagger UI y colección Postman). Registrar y clasificar los defectos encontrados en MantisBT. Adjuntar evidencias y dar seguimiento al estado de cada ticket. Construir el dashboard de métricas a partir de los datos exportados. Co-redactar el análisis de calidad del software. | 100% |
| **Supervisora / Aprobadora** | [Nombre docente] | Revisar y aprobar el plan de pruebas. Validar que los entregables cumplen los criterios académicos. Aprobar el cierre del ciclo de pruebas. | Según cronograma académico |

### **4.1 Matriz RACI**

La siguiente matriz define quién es Responsable (R), Aprobador (A), Consultado (C) e Informado (I) en cada actividad clave del proceso de pruebas.

| **Actividad** | **QA Lead / Automatizador** | **QA Analyst / Bug Manager** | **Docente** |
|---|---|---|---|
| Planificación del plan de pruebas | **R/A** | **C** | **C** |
| Diseño de casos de prueba | **R** | **A** | **C** |
| Revisión y validación de casos de prueba | **C** | **R/A** | **I** |
| Preparación del ambiente (Docker, pytest) | **R/A** | **I** | **I** |
| Ejecución de pruebas manuales exploratorias | **C** | **R** | **I** |
| Ejecución de pruebas manuales técnicas | **R** | **C** | **I** |
| Ejecución de pruebas automatizadas | **R/A** | **I** | **I** |
| Registro de defectos en MantisBT | **C** | **R/A** | **I** |
| Generación de datos para dashboard | **R** | **C** | **I** |
| Construcción del dashboard de métricas | **I** | **R** | **I** |
| Análisis de calidad y cierre | **R** | **R** | **A** |

_Leyenda: R = Responsable de ejecutar  A = Aprobador  C = Consultado  I = Informado_

---

## **5. Estrategia de Pruebas**

### **5.1 Tipos de Prueba**

| **Tipo de Prueba** | **Descripción** | **Responsable** | **Incluida** |
|---|---|---|---|
| **Prueba funcional** | Verifica que cada endpoint opera conforme al contrato de la API (status codes, estructura JSON, lógica de negocio). | QA Lead | [x] Sí |
| **Prueba de regresión** | La suite de pytest actúa como suite de regresión: garantiza que las funcionalidades validadas se mantienen estables y que los defectos corregidos no reaparecen en ejecuciones futuras. | QA Lead | [x] Sí |
| **Prueba de integración** | Valida la interacción entre múltiples módulos de la API en un flujo completo (ej. autenticación → creación de artículo → comentario → favorito). | QA Lead | [x] Sí |
| **Prueba de rendimiento** | Evalúa el comportamiento bajo carga y estrés. | N/A | [ ] No — fuera del alcance del taller |
| **Prueba de seguridad** | Identifica vulnerabilidades de autorización: acceso no autorizado a recursos ajenos, endpoints que no requieren autenticación debiendo hacerlo. | QA Lead | [x] Sí (alcance parcial) |
| **Prueba de usabilidad** | Para una API REST, se evalúa la usabilidad del contrato: claridad de mensajes de error, documentación de Swagger UI, consistencia de la estructura JSON de respuesta. | QA Lead | [x] Sí (adaptada a API) |
| **Prueba de aceptación (UAT)** | Validación formal con el usuario o cliente final. | N/A | [ ] No — no hay cliente final en este proyecto académico |

### **5.2 Técnicas de Diseño de Casos de Prueba**

- **Partición de equivalencia (EP):** Se aplica en módulos de autenticación y validación de campos (ej. emails válidos vs. inválidos, contraseñas vacías vs. con valor).
- **Análisis de valores límite (BVA):** Se aplica en el parámetro `limit` de `GET /api/articles` (límite máximo = 20) y en longitudes de campos de texto.
- **Tabla de decisión:** Se aplica en pruebas de autorización (usuario autenticado/no autenticado × recurso propio/ajeno) y en combinaciones de filtros de artículos (`?tag`, `?author`, `?favorited`).
- **Prueba de transición de estados:** Se aplica en flujos de follow/unfollow (estado `following`: false → true → false) y favoritos (estado `favorited` + contador `favoritesCount`).
- **Prueba exploratoria:** Se aplica en casos manuales donde se buscan comportamientos no especificados (slugs con caracteres especiales, tokens JWT manipulados, mensajes de error bajo entradas inesperadas).

### **5.3 Niveles de Prueba**

- **Pruebas unitarias:** No aplica en este plan. El SUT no expone funciones puras aisladas; la lógica de negocio está integrada en los endpoints y repositorios.
- **Pruebas de integración:** [Tu nombre] — pytest 9.x + httpx (FastAPI TestClient). Validan la interacción entre endpoints, ORM (SQLAlchemy), base de datos y capa de seguridad (JWT).
- **Pruebas de sistema:** [Tu nombre] — Swagger UI / Postman. Validan el comportamiento del sistema completo desde la perspectiva de un cliente externo de la API.
- **Pruebas de aceptación:** No aplica en este proyecto académico.

### **5.4 Criterios de Suspensión y Requisitos de Reanudación**

Los criterios de suspensión definen las condiciones bajo las cuales se suspende la ejecución de pruebas; los criterios de reanudación determinan cuándo puede continuar.

| **Criterios de Suspensión** | **Requisitos de Reanudación** |
|---|---|
| La API no levanta correctamente en el entorno local (Docker Compose falla o la aplicación no responde en localhost:8000). | El entorno ha sido restaurado, la API responde con HTTP 200 en `GET /api/tags` (smoke test). |
| Defecto crítico no inyectado intencionalmente que impide la ejecución de casos de prueba. | El defecto ha sido identificado, documentado en MantisBT y aislado para continuar con los casos no bloqueados. |
| Ambiente de pruebas inestable (BD corrompida, fixtures de pytest fallando). | La BD de pruebas ha sido reinicializada y los fixtures validan correctamente. |
| Más del 30% de los casos automatizados fallan por causas no relacionadas con los bugs inyectados. | Se ha identificado la causa raíz (configuración, dependencias) y se ha corregido el entorno. |
| Cambio en la estrategia de bugs inyectados que invalida casos de prueba ya diseñados. | Los casos de prueba afectados han sido actualizados y revisados. |

### **5.5 Completitud de las Pruebas**

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

---

## **6. Criterios de Entrada y Salida**

| **Criterios de Entrada (para iniciar pruebas)** | **Criterios de Salida (para finalizar pruebas)** |
|---|---|
| La API responde correctamente en `http://localhost:8000` (Docker Compose activo). | ≥ 95% de los 41 casos de prueba ejecutados. |
| El sistema bajo prueba opera de forma estable y todas las funcionalidades principales responden ante las peticiones. | Todos los defectos encontrados registrados y clasificados en MantisBT. |
| Los 41 casos de prueba están documentados en `docs_qa/Casos_De_Prueba.md`. | 0 defectos de severidad Crítica sin documentar. |
| MantisBT está configurado y accesible para el equipo. | Archivos `pytest_results.json` y `coverage.json` generados. |
| Los fixtures de pytest (`tests/conftest.py`) están configurados y la BD de pruebas inicializa correctamente. | Informe de análisis de calidad redactado y entregado. |
| La colección `postman.json` está importada en Postman. | Aprobación del cierre por parte de la docente. |

---

## **7. Casos de Prueba**

### **7.1 Plantilla de Caso de Prueba**

| **Campo** | **Descripción** |
|---|---|
| **ID del caso** | `CP-[GRUPO]-[MODO]-[NUM]`  Ej: `CP-AUTH-A-001`, `CP-EXP-M-001` |
| **Nombre** | Descripción concisa: acción + objeto + condición + resultado esperado |
| **Funcionalidad / Endpoint cubierto** | Endpoint o área funcional que se prueba. Ej: `POST /api/users/login` |
| **Precondiciones** | Estado del sistema antes de ejecutar la prueba |
| **Datos de entrada** | Endpoint, método HTTP, headers y body JSON exactos |
| **Pasos de ejecución** | 1. [Paso 1]  2. [Paso 2]  3. [Paso 3] |
| **Resultado esperado** | Código HTTP + estructura del JSON de respuesta esperada |
| **Resultado obtenido** | [A completar durante la ejecución] |
| **Estado** | [ ] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [ ] Funcional  [ ] Regresión  [ ] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual (Swagger UI / Postman)  [ ] Automatizado (pytest) |
| **Técnica aplicada** | [ ] EP  [ ] BVA  [ ] Tabla de decisión  [ ] Transición de estados  [ ] Exploratoria |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | [DD/MM/AAAA] |
| **Defectos asociados** | [BUG-XX] / N/A |
| **Observaciones** | Evidencia: screenshot de Postman/Swagger o output de pytest |

### **7.2 Registro de Casos de Prueba**

**Pruebas Manuales (15)**

| **ID** | **Nombre del Caso** | **Módulo** | **Prioridad** | **Estado** | **Defecto** |
|---|---|---|---|---|---|
| **CP-EXP-M-001** | Flujo completo happy path: registro → login → crear artículo → seguir usuario → ver feed → comentar → marcar favorito | Exploratorio | Alta | No ejecutado | N/A |
| **CP-EXP-M-002** | Enviar títulos con caracteres especiales (emojis, HTML, unicode) y observar slugs generados | Exploratorio | Media | No ejecutado | N/A |
| **CP-EXP-M-003** | Requests con tokens JWT manipulados: expirado, firma inválida, token de otro proyecto | Exploratorio | Alta | No ejecutado | N/A |
| **CP-EXP-M-004** | BVA: crear 25 artículos y solicitar `GET /api/articles?limit=100`; contar resultados manualmente | Exploratorio | Media | No ejecutado | — |
| **CP-EXP-M-005** | Crear artículos con títulos similares ("Mi Blog" y "mi blog") y observar colisión de slugs | Exploratorio | Baja | No ejecutado | N/A |
| **CP-TOOL-M-001** | Verificar en Swagger UI que los 19 endpoints están documentados correctamente | Herramientas | Media | No ejecutado | N/A |
| **CP-TOOL-M-002** | Usar botón Authorize de Swagger UI con token JWT y ejecutar 3 endpoints autenticados | Herramientas | Alta | No ejecutado | N/A |
| **CP-TOOL-M-003** | Importar `postman.json` en Postman y ejecutar la colección completa end-to-end | Herramientas | Alta | No ejecutado | N/A |
| **CP-QUAL-M-001** | Evaluar calidad y claridad de mensajes de error con datos inválidos en cada módulo | Calidad | Media | No ejecutado | N/A |
| **CP-QUAL-M-002** | Verificar estructura completa del JSON de respuesta de cada módulo vs. RealWorld Spec | Calidad | Alta | No ejecutado | N/A |
| **CP-QUAL-M-003** | Con dos usuarios: intentar editar artículo ajeno autenticado como no-autor (Swagger UI) | Calidad | Alta | No ejecutado | — |
| **CP-QUAL-M-004** | Con dos usuarios: intentar eliminar artículo ajeno autenticado como no-autor (Swagger UI) | Calidad | Crítica | No ejecutado | — |
| **CP-EST-M-001** | Flujo follow → unfollow verificando transición de `following`: false → true → false | Estados | Media | No ejecutado | — |
| **CP-EST-M-002** | Flujo marcar favorito → desmarcar; verificar `favorited` y `favoritesCount` en cada paso | Estados | Media | No ejecutado | — |
| **CP-EST-M-003** | Eliminar artículo propio y luego solicitar `GET /api/articles/{slug}`; verificar 404 | Estados | Media | No ejecutado | N/A |

**Pruebas Automatizadas (26)**

| **ID** | **Nombre del Caso** | **Módulo** | **Prioridad** | **Estado** | **Defecto** |
|---|---|---|---|---|---|
| **CP-AUTH-A-001** | Registro exitoso retorna HTTP 201 Created (no 200) | Auth | Alta | No ejecutado | — |
| **CP-AUTH-A-002** | Registro exitoso retorna token JWT en el body de respuesta | Auth | Alta | No ejecutado | N/A |
| **CP-AUTH-A-003** | Login con credenciales válidas retorna token JWT | Auth | Alta | No ejecutado | N/A |
| **CP-AUTH-A-004** | Login con email inexistente retorna HTTP 400 | Auth | Alta | No ejecutado | N/A |
| **CP-AUTH-A-005** | Registro con email duplicado retorna HTTP 400 | Auth | Alta | No ejecutado | N/A |
| **CP-ART-A-001** | Crear artículo con datos válidos retorna 200 con estructura correcta (slug, author, tagList) | Articles | Alta | No ejecutado | N/A |
| **CP-ART-A-002** | Crear artículo con título vacío (`""`) retorna HTTP 422 Unprocessable Entity | Articles | Alta | No ejecutado | — |
| **CP-ART-A-003** | Crear artículo sin token de autenticación retorna HTTP 401 | Articles | Alta | No ejecutado | N/A |
| **CP-ART-A-004** | Editar artículo como autor legítimo retorna artículo actualizado | Articles | Alta | No ejecutado | N/A |
| **CP-ART-A-005** | Editar artículo de otro usuario retorna HTTP 400 | Articles | Alta | No ejecutado | — |
| **CP-ART-A-006** | Eliminar artículo de otro usuario retorna HTTP 400 | Articles | Crítica | No ejecutado | — |
| **CP-ART-A-007** | Acceder a `GET /api/articles/feed` sin token retorna HTTP 401 | Articles | Alta | No ejecutado | — |
| **CP-ART-A-008** | `GET /api/articles?tag=X` retorna solo artículos etiquetados con el tag X | Articles | Media | No ejecutado | — |
| **CP-ART-A-009** | `GET /api/articles?limit=100` con 25+ artículos en BD retorna máximo 20 | Articles | Media | No ejecutado | — |
| **CP-COM-A-001** | Crear comentario en artículo existente retorna el comentario con autor y body | Comments | Media | No ejecutado | N/A |
| **CP-COM-A-002** | Crear comentario sin autenticación retorna HTTP 401 | Comments | Media | No ejecutado | N/A |
| **CP-COM-A-003** | Eliminar comentario propio retorna HTTP 200 sin errores | Comments | Media | No ejecutado | N/A |
| **CP-COM-A-004** | Obtener comentarios de artículo inexistente retorna HTTP 404 | Comments | Media | No ejecutado | N/A |
| **CP-PRF-A-001** | Seguir a un usuario cambia el campo `following` a `true` en la respuesta | Profiles | Media | No ejecutado | — |
| **CP-PRF-A-002** | Dejar de seguir a un usuario cambia el campo `following` a `false` | Profiles | Media | No ejecutado | — |
| **CP-PRF-A-003** | Obtener perfil de usuario inexistente retorna HTTP 404 | Profiles | Media | No ejecutado | N/A |
| **CP-PRF-A-004** | Seguir usuario sin autenticación retorna HTTP 401 | Profiles | Media | No ejecutado | N/A |
| **CP-FAV-A-001** | Marcar artículo como favorito incrementa `favoritesCount` en 1 y `favorited` = true | Favorites | Media | No ejecutado | — |
| **CP-FAV-A-002** | Desmarcar artículo favorito decrementa `favoritesCount` en 1 y `favorited` = false | Favorites | Media | No ejecutado | — |
| **CP-TAG-A-001** | `GET /api/tags` retorna una lista de tags existentes en la BD | Tags | Baja | No ejecutado | N/A |
| **CP-TAG-A-002** | Tags asignados al crear un artículo aparecen en `GET /api/tags` | Tags | Baja | No ejecutado | N/A |

**Total: 41 casos de prueba (15 manuales + 26 automatizados)**

---

## **8. Gestión de Defectos**

### **8.1 Clasificación de Defectos**

La clasificación se define en función del impacto en el negocio de la plataforma (blogs tipo Medium):

| **Severidad** | **Descripción aplicada al SUT** | **Tiempo de Resolución** |
|---|---|---|
| **Crítica** | El sistema expone una brecha de seguridad (cualquier usuario puede eliminar contenido ajeno), o un flujo de negocio principal es completamente inutilizable. | Inmediata — mismo día |
| **Alta** | Una funcionalidad importante de negocio no opera correctamente (artículos sin validación de título, feed sin autenticación, autoría ignorada en edición). | 24–48 horas |
| **Media** | Una funcionalidad secundaria falla o el contrato de la API no es el esperado (estado `following` incorrecto, filtro de tags ignorado, límite de paginación ignorado). | 3–5 días hábiles |
| **Baja** | Inconsistencia menor que no afecta funcionalidad: violación del estándar REST en status codes (200 vs 201). | Próxima versión |

### **8.2 Plantilla de Reporte de Defecto**

Los defectos detectados se registran en **MantisBT** por [Nombre compañera] a partir de las fichas preparadas por [Tu nombre]. La siguiente plantilla define los campos mínimos por defecto.

| **Campo** | **Detalle** |
|---|---|
| **ID del defecto** | Asignado automáticamente por MantisBT. Ej: `#0000001` |
| **Título** | Descripción corta y específica del defecto (máx. 80 caracteres) |
| **Caso de prueba relacionado** | ID del caso que detectó el defecto. Ej: `CP-ART-A-006` |
| **Módulo afectado** | Auth / Articles / Comments / Profiles / Favorites / Tags |
| **Severidad** | [ ] Crítica  [ ] Alta  [ ] Media  [ ] Baja |
| **Prioridad** | [ ] Alta  [ ] Media  [ ] Baja |
| **Estado** | [ ] Nuevo  [ ] Confirmado  [ ] Asignado  [ ] Resuelto  [ ] Cerrado |
| **Descripción** | Descripción técnica del comportamiento incorrecto observado |
| **Pasos para reproducir** | 1. Endpoint y método HTTP  2. Headers y body  3. Resultado observado |
| **Resultado esperado** | Código HTTP + descripción del comportamiento correcto según la especificación |
| **Resultado obtenido** | Código HTTP + descripción del comportamiento incorrecto observado |
| **Evidencia** | Screenshot de Swagger UI / Postman, o output del terminal de pytest |
| **Entorno** | `localhost:8000`, Python 3.15, Docker Compose |
| **Reportado por** | [Tu nombre] |
| **Fecha de reporte** | [DD/MM/AAAA] |
| **Cargado en Mantis por** | [Nombre compañera] |
| **Fecha de resolución** | [DD/MM/AAAA] |

---

## **9. Entregables de Prueba**

| **Entregable** | **Descripción** | **Fase** | **Responsable** | **Fecha estimada** |
|---|---|---|---|---|
| **Plan de Pruebas** | Este documento: alcance, estrategia, recursos, cronograma y criterios del proceso de pruebas. | Planificación | [Tu nombre] | 26/10/2025 |
| **Plan de Acción** | Hoja de ruta interna con estrategia de bugs, distribución de casos y convenciones. Ubicación: `docs_qa/Plan_De_Accion.md` | Planificación | [Tu nombre] | 26/10/2025 |
| **Casos de Prueba** | 41 casos documentados con plantilla completa (precondiciones, pasos, resultado esperado). Ubicación: `docs_qa/Casos_De_Prueba.md` | Diseño | [Tu nombre] | [Por definir] |
| **Scripts de Prueba Automatizados** | 26 scripts pytest en `tests/api/` organizados por módulo. | Implementación | [Tu nombre] | [Por definir] |

| **Registro de Defectos (MantisBT)** | 9 tickets cargados en MantisBT con toda la información de cada defecto detectado. | Ejecución | [Nombre compañera] | Continuo durante ejecución |
| **Evidencias de Pruebas Manuales** | Screenshots de Swagger UI y Postman para los 15 casos manuales. Ubicación: `docs_qa/evidencias/` | Ejecución | [Tu nombre] | [Por definir] |
| **Datos de Métricas** | Archivos `pytest_results.json` y `coverage.json` generados al finalizar la ejecución automatizada. Ubicación: `docs_qa/data/` | Cierre | [Tu nombre] | [Por definir] |
| **Dashboard de Métricas** | Visualización de los indicadores clave del proceso (generado con IA a partir de los datos de métricas). | Cierre | [Tu nombre] / [Nombre compañera] | [Por definir] |
| **Análisis de Calidad** | Informe con conclusiones sobre la calidad del software probado con base en las métricas. Ubicación: `docs_qa/Analisis_Calidad.md` | Cierre | [Tu nombre] | [Por definir] |

---

## **10. Recursos y Ambiente de Prueba**

### **10.1 Equipo de Pruebas**

| **Nombre** | **Rol** | **Responsabilidades** | **Dedicación** |
|---|---|---|---|
| [Tu nombre] | QA Lead / QA Analyst / QA Automatizador | Diseño, ejecución manual, automatización, inyección de bugs, generación de métricas | 100% |
| [Nombre compañera] | Bug Manager (MantisBT) | Carga, clasificación y seguimiento de tickets en MantisBT | 100% |

### **10.2 Herramientas**

| **Categoría** | **Herramienta** | **Propósito** |
|---|---|---|
| **Pruebas manuales — Documentación interactiva** | Swagger UI (`http://localhost:8000/docs`) | Explorar y ejecutar endpoints manualmente; verificar documentación de la API |
| **Pruebas manuales — Cliente HTTP** | Postman + colección `postman.json` | Ejecutar y documentar casos manuales; colección pre-existente en el repositorio |
| **Pruebas automatizadas — Framework** | pytest 9.x + pytest-asyncio | Ejecutar la suite de 26 tests automatizados con soporte async |
| **Pruebas automatizadas — Cliente HTTP** | httpx + FastAPI TestClient | Realizar peticiones HTTP dentro de los tests de pytest |
| **Cobertura de código** | pytest-cov | Medir el porcentaje de código fuente ejercitado por los tests |
| **Reporte de resultados** | pytest-json-report | Exportar resultados de ejecución en JSON para el dashboard |
| **Gestión de defectos** | MantisBT | Registro, clasificación y seguimiento de los 9 defectos detectados |
| **Control de versiones** | Git (ramas `main` y `buggy-version`) | Aislar el código con bugs del código limpio |
| **Gestor de dependencias** | uv (pyproject.toml) | Instalar y gestionar dependencias Python de forma reproducible |
| **Entorno de ejecución** | Docker + Docker Compose | Levantar la API y PostgreSQL con un solo comando |

### **10.3 Ambiente de Prueba**

| **Ambiente** | **URL / Servidor** | **Versión** | **Responsable** |
|---|---|---|---|
| **Local — Desarrollo / QA** | `http://localhost:8000` | Python 3.15, FastAPI 0.115+, PostgreSQL (psycopg3), Docker Compose | [Tu nombre] |

_Nota: Este proyecto opera en un entorno local único. No hay ambientes de Staging ni Producción._
| **Documentación interactiva** | `http://localhost:8000/docs` (Swagger UI) | Generada automáticamente por FastAPI | [Tu nombre] |



---

## **11. Cronograma de Pruebas**

| **Actividad** | **Fecha Inicio** | **Fecha Fin** | **Responsable** | **Estado** |
|---|---|---|---|---|
| Planificación: Plan de Acción + Plan de Pruebas | 26/10/2025 | [Por definir] | [Tu nombre] | ✅ En progreso |
| Diseño y documentación de los 41 casos de prueba | [Por definir] | [Por definir] | [Tu nombre] | [ ] Pendiente |
| Preparación del ambiente (Docker, pytest, MantisBT) | [Por definir] | [Por definir] | [Tu nombre] / [Compañera] | [ ] Pendiente |

| Ejecución de 15 pruebas manuales (Swagger / Postman) | [Por definir] | [Por definir] | [Tu nombre] | [ ] Pendiente |
| Desarrollo y ejecución de 26 pruebas automatizadas (pytest) | [Por definir] | [Por definir] | [Tu nombre] | [ ] Pendiente |
| Carga de defectos en MantisBT | [Por definir] | [Por definir] | [Nombre compañera] | [ ] Pendiente |
| Generación de datos de métricas (JSON exports) | [Por definir] | [Por definir] | [Tu nombre] | [ ] Pendiente |
| Generación del dashboard de métricas | [Por definir] | [Por definir] | [Tu nombre] / [Compañera] | [ ] Pendiente |
| Redacción del análisis de calidad y cierre | [Por definir] | [Por definir] | [Tu nombre] | [ ] Pendiente |

---

## **12. Riesgos y Mitigación**

| **#** | **Riesgo** | **Probabilidad** | **Impacto** | **Plan de Mitigación** |
|---|---|---|---|---|
| **1** | La API no levanta en el entorno local (Docker o PostgreSQL fallan). | Media | Alto | Usar SQLite como BD alternativa para la suite de pytest; documentar la configuración paso a paso en el README de pruebas. |
| **2** | Los bugs inyectados no son detectados por los tests (diseño de casos insuficiente). | Baja | Alto | Verificar antes de ejecutar que cada bug tiene al menos un caso asociado en la columna "Defecto" del §7.2. Ejecutar un smoke test manual de cada bug primero. |
| **3** | Un bug inyectado rompe la aplicación completamente (impide ejecutar el resto de tests). | Baja | Alto | Inyectar y probar los bugs uno por uno antes de hacer el commit conjunto. Mantener la rama `main` intacta como punto de rollback. |
| **4** | Falta de tiempo para completar los 26 scripts automatizados. | Media | Medio | Priorizar módulos Auth y Articles (mayor severidad). Los módulos Tags (2 casos) y Favorites (2 casos) pueden reducirse si hay restricción de tiempo. |
| **5** | Dificultad con la configuración de pytest-asyncio para tests async. | Media | Medio | Revisar la configuración existente en `tests/conftest.py` y `pyproject.toml`; la base de fixtures ya está implementada en el repositorio. |

---

## **13. Métricas de Calidad**

| **Métrica** | **Fórmula / Medición** | **Meta** | **Valor Actual** |
|---|---|---|---|
| **Tasa de ejecución de casos** | (Casos ejecutados / 41 casos totales) × 100 | **≥ 95%** | — |
| **Tasa de casos aprobados** | (Casos que pasan / Casos ejecutados) × 100 | **≥ 80%** _(ajustado: buscamos detectar bugs, no aprobarlos todos)_ | — |
| **Tasa de detección de defectos** | (Defectos encontrados documentados / Total defectos reportados) × 100 | **100%** | — |
| **Densidad de defectos** | Defectos encontrados / Casos ejecutados | **< 0.3** | — |
| **Defectos críticos documentados en Mantis** | Conteo de tickets de severidad Crítica | **≥ 0** | — |
| **Defectos críticos abiertos al cierre** | Conteo de tickets Críticos sin estado Closed | **= 0** | — |
| **Tasa de reapertura de defectos** | (Defectos reabiertos / Defectos resueltos) × 100 | **< 5%** | — |
| **Cobertura de código (pytest-cov)** | Líneas de código ejercitadas por los tests / Total líneas | **≥ 70%** | — |
| **Cobertura de requisitos (endpoints)** | (Endpoints cubiertos por ≥ 1 caso / 19 endpoints totales) × 100 | **100%** | — |

---

## **13. Criterios de Cierre y Entregables**

### **13.1 Entregables del Plan de Pruebas**

- Plan de Pruebas (este documento) — `docs_qa/plan_pruebas (1).md`
- Plan de Acción / Estrategia — `docs_qa/Plan_De_Accion.md`
- 41 Casos de prueba documentados — `docs_qa/Casos_De_Prueba.md`
- Scripts de prueba automatizados — `tests/api/`
- Rama Git con bugs inyectados — `buggy-version`
- Registro de 9 defectos en MantisBT
- Evidencias de pruebas manuales — `docs_qa/evidencias/`
- Datos de métricas — `docs_qa/data/pytest_results.json`, `docs_qa/data/coverage.json`
- Dashboard de métricas visual
- Análisis de calidad del software — `docs_qa/Analisis_Calidad.md`

### **13.2 Aprobaciones**

| **Nombre** | **Rol** | **Firma** | **Fecha** |
|---|---|---|---|
| [Tu nombre] | QA Lead / QA Analyst / Automatizador | ___________________ | [DD/MM/AAAA] |
| [Nombre compañera] | Bug Manager (MantisBT) | ___________________ | [DD/MM/AAAA] |
| [Nombre docente] | Supervisora / Aprobadora académica | ___________________ | [DD/MM/AAAA] |

---

## **14. Términos y Acrónimos**

### **14.1 Términos**

| **Término** | **Definición** |
|---|---|
| **Caso de prueba** | Conjunto de condiciones, datos de entrada, pasos de ejecución y resultado esperado que valida una funcionalidad específica del sistema. |
| **Ciclo de pruebas** | Periodo de tiempo durante el cual se planifican, diseñan, ejecutan y evalúan las actividades de prueba para una entrega o versión del sistema. |
| **Criterio de aceptación** | Condiciones definidas que un sistema o funcionalidad debe cumplir para ser aceptado por el cliente o usuario final. |
| **Datos de prueba** | Conjunto de valores de entrada utilizados durante la ejecución de un caso de prueba para verificar el comportamiento del sistema. |
| **Defecto / Bug** | Discrepancia entre el comportamiento real del sistema y el comportamiento esperado según los requisitos o la especificación. |
| **Entorno de pruebas** | Conjunto de hardware, software, datos y configuraciones utilizados para ejecutar las pruebas. En este proyecto: Docker Compose + Python 3.15 + PostgreSQL local. |
| **Evidencia de prueba** | Artefactos generados durante la ejecución de pruebas que sirven como registro del resultado: screenshots de Swagger/Postman, output de pytest. |

| **Plan de pruebas** | Documento que describe el alcance, estrategia, recursos, cronograma y actividades del proceso de pruebas. |
| **Regresión** | Conjunto de pruebas ejecutadas para verificar que un cambio en el sistema no ha introducido nuevos defectos en funcionalidades ya validadas. |
| **Severidad** | Nivel de impacto técnico que un defecto tiene sobre el funcionamiento del sistema (Crítica / Alta / Media / Baja). |
| **Slug** | Cadena de texto derivada del título de un artículo, transformada en formato URL-friendly (sin espacios ni caracteres especiales). Ej: "Mi Artículo" → `mi-articulo`. Sirve como identificador único del artículo en los endpoints. |
| **Token JWT** | Credencial criptográfica de autenticación emitida por la API tras el login. Se incluye en el header `Authorization: Bearer {token}` de cada request a endpoints protegidos. |

### **14.2 Acrónimos**

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
