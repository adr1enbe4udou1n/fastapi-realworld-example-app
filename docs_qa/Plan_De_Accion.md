# Plan de Acción — Taller de Pruebas de Software
## API: FastAPI RealWorld Example App (Conduit)

| **Campo**            | **Detalle**                                              |
|----------------------|----------------------------------------------------------|
| **Proyecto**         | FastAPI RealWorld Example App — Conduit Backend          |
| **Versión**          | 1.0                                                      |
| **Fecha**            | 26/10/2025                                               |
| **Elaborado por**    | [Tu nombre] (QA) + [Nombre compañera] (Gestión de bugs)  |
| **Rol QA**           | QA Lead / QA Analyst / QA Automatizador — [Tu nombre]    |
| **Rol Bug Tracking** | Bug Manager Mantis — [Nombre compañera]                  |
| **Estado**           | ✅ Aprobado — Listo para ejecución                       |

> **División del trabajo:** [Tu nombre] diseña y ejecuta la totalidad de los casos de prueba (manuales y automatizados), inyecta los bugs y genera los datos de métricas. Una vez detectados los defectos, [nombre compañera] los registra, clasifica y da seguimiento en **MantisBT** con la información que le entregues.

---

## Tabla de Contenido

1. [Descripción del Sistema](#1-descripción-del-sistema)
2. [Alcance de las Pruebas](#2-alcance-de-las-pruebas)
3. [Contexto de Negocio y su Influencia en las Pruebas](#3-contexto-de-negocio-y-su-influencia-en-las-pruebas)
4. [Estrategia de Inyección de Bugs](#4-estrategia-de-inyección-de-bugs)
5. [Distribución de los 40 Casos de Prueba](#5-distribución-de-los-40-casos-de-prueba)
6. [Matriz de Severidad y Prioridad](#6-matriz-de-severidad-y-prioridad)
7. [Estándar de Documentación de Casos](#7-estándar-de-documentación-de-casos)
8. [Stack de Herramientas](#8-stack-de-herramientas)
9. [Propuesta de Reporte de Bugs](#9-propuesta-de-reporte-de-bugs)
10. [Propuesta de Dashboard de Métricas](#10-propuesta-de-dashboard-de-métricas)
11. [Cronograma de Ejecución](#11-cronograma-de-ejecución)
12. [Riesgos del Plan](#12-riesgos-del-plan)
13. [Checklist de Entregables](#13-checklist-de-entregables)

---

## 1. Descripción del Sistema

### 1.1 ¿Qué es esta aplicación?

La aplicación bajo prueba es **Conduit**, una implementación de referencia (*RealWorld spec*) de una plataforma de blogs tipo Medium, construida íntegramente como **API REST** con **FastAPI** (Python). Esta API es el motor de backend de la plataforma: no posee interfaz gráfica (UI), ni frontend, ni páginas web. Toda interacción con el sistema se realiza a través de peticiones HTTP enviadas a sus endpoints.

El proyecto es de código abierto, disponible en GitHub, y fue escogido para este taller porque representa una aplicación real con complejidad suficiente para practicar pruebas automatizadas a nivel de integración y unitario.

### 1.2 Arquitectura Técnica

```
fastapi-realworld-example-app/
├── app/
│   ├── api/
│   │   ├── deps.py          # Dependencias de autenticación (JWT)
│   │   └── routes/          # Controladores por módulo
│   │       ├── auth.py      # Registro y login
│   │       ├── user.py      # Perfil del usuario autenticado
│   │       ├── profiles.py  # Perfiles públicos + follow/unfollow
│   │       ├── articles.py  # CRUD de artículos + feed
│   │       ├── comments.py  # CRUD de comentarios
│   │       ├── favorites.py # Marcar/desmarcar favoritos
│   │       └── tags.py      # Listado de tags
│   ├── crud/                # Lógica de acceso a datos (repositorios)
│   ├── models/              # Modelos SQLAlchemy (ORM)
│   ├── schemas/             # Schemas Pydantic (validación E/S)
│   ├── core/                # Configuración y seguridad (JWT)
│   ├── db/                  # Configuración de base de datos
│   └── main.py              # Punto de entrada FastAPI
├── tests/                   # Suite de pruebas con pytest
├── docs_qa/                 # Artefactos de QA (este documento)
├── postman.json             # Colección Postman lista para importar
├── compose.yaml             # Docker Compose (PostgreSQL + App)
└── pyproject.toml           # Gestión de dependencias (uv)
```

**Stack tecnológico:**

| Capa | Tecnología |
|------|-----------|
| Framework API | FastAPI 0.115+ |
| Lenguaje | Python 3.15 |
| ORM | SQLAlchemy 2.x (async) |
| Base de Datos | PostgreSQL (psycopg3) |
| Autenticación | JWT (python-jose) |
| Contraseñas | bcrypt |
| Validación | Pydantic v2 |
| Despliegue | Docker + Docker Compose |

### 1.3 Módulos del Sistema y Endpoints

| Módulo | Método | Endpoint | Autenticación |
|--------|--------|----------|---------------|
| **Auth** | POST | `/api/users` | No requerida |
| **Auth** | POST | `/api/users/login` | No requerida |
| **User** | GET | `/api/user` | Requerida |
| **User** | PUT | `/api/user` | Requerida |
| **Profiles** | GET | `/api/profiles/{username}` | Opcional |
| **Profiles** | POST | `/api/profiles/{username}/follow` | Requerida |
| **Profiles** | DELETE | `/api/profiles/{username}/follow` | Requerida |
| **Articles** | GET | `/api/articles` | Opcional |
| **Articles** | POST | `/api/articles` | Requerida |
| **Articles** | GET | `/api/articles/feed` | Requerida |
| **Articles** | GET | `/api/articles/{slug}` | Opcional |
| **Articles** | PUT | `/api/articles/{slug}` | Requerida |
| **Articles** | DELETE | `/api/articles/{slug}` | Requerida |
| **Comments** | GET | `/api/articles/{slug}/comments` | Opcional |
| **Comments** | POST | `/api/articles/{slug}/comments` | Requerida |
| **Comments** | DELETE | `/api/articles/{slug}/comments/{id}` | Requerida |
| **Favorites** | POST | `/api/articles/{slug}/favorite` | Requerida |
| **Favorites** | DELETE | `/api/articles/{slug}/favorite` | Requerida |
| **Tags** | GET | `/api/tags` | No requerida |

**Total de endpoints: 19**

### 1.4 Modelo de Datos Resumido

```
User           Article         Comment         Tag
─────────      ───────────     ───────────     ───────
id             id              id              id
name           author_id ─┐   article_id ─┐   name
email          title      │   author_id ──┤
password       slug       │   body        │
bio            description│   created_at  │
image          body       │   updated_at  │
created_at     created_at │               │
updated_at     updated_at │               │
               ──────────────────────────────────────
               Relaciones N:M: article_tag, article_favorite, follower_user
```

---

## 2. Alcance de las Pruebas

### 2.1 En alcance ✅

| Área | Descripción |
|------|-------------|
| **Autenticación y autorización** | Registro, login, tokens JWT, acceso a rutas protegidas |
| **Gestión de usuarios** | Obtener y actualizar el perfil del usuario autenticado |
| **Gestión de perfiles** | Ver perfil público, seguir y dejar de seguir usuarios |
| **CRUD de artículos** | Crear, leer, actualizar y eliminar artículos |
| **Feed de artículos** | Listar artículos de usuarios seguidos |
| **Filtros de artículos** | Filtrar por autor, tag y favoritos |
| **Gestión de comentarios** | Crear, leer y eliminar comentarios en artículos |
| **Favoritos** | Marcar/desmarcar artículos como favorito y verificar contador |
| **Tags** | Listar tags disponibles |
| **Control de acceso** | Verificar que solo los autores pueden editar/eliminar sus recursos |
| **Validación de entradas** | Campos requeridos, formatos inválidos, valores fuera de rango |
| **Códigos de estado HTTP** | Verificar respuestas 200, 201, 400, 401, 404, 422 |
| **Estructura de respuesta** | Verificar que el JSON de respuesta cumple el contrato de la API |

### 2.2 Fuera de alcance ❌

| Área | Justificación |
|------|---------------|
| Interfaz gráfica (UI/Frontend) | La aplicación es backend-only |
| Pruebas de rendimiento / carga | Fuera del alcance del taller actual |
| Pruebas de infraestructura (Docker, DB) | No son funcionalidades de negocio |
| Migraciones de Alembic | Son tareas de DBA, no QA funcional |
| Pipeline CI/CD | No existe en este proyecto aún |
| Módulo de pagos o notificaciones | No existen en la aplicación |

---

## 3. Contexto de Negocio y su Influencia en las Pruebas

> **Principio ISTQB aplicado:** *"Las pruebas dependen del contexto"* — la estrategia, profundidad y priorización deben definirse a partir del dominio del negocio.

Esta API simula el motor de una **plataforma de blogs tipo Medium**. Su negocio core gira en torno a:

1. **Crear y compartir contenido** (artículos)
2. **Construir comunidad** (follows, feeds personalizados)
3. **Interactuar con el contenido** (comentarios, favoritos)

### 3.1 Flujos Críticos de Negocio

Los flujos que, si fallan, destruyen completamente la propuesta de valor del negocio:

| Flujo Crítico | Razón |
|---------------|-------|
| Registro y login de usuarios | Sin autenticación, ninguna funcionalidad autenticada funciona |
| Creación de artículos | Es la funcionalidad central del negocio |
| Control de acceso (solo el autor edita/borra) | Integridad del contenido de los usuarios |
| Listado y filtrado de artículos | Descubrimiento de contenido = experiencia del lector |

### 3.2 Influencia del Negocio en Severidad y Prioridad

| Módulo | Impacto en el Negocio | → Severidad esperada |
|--------|-----------------------|----------------------|
| Auth (login/registro) | Crítico — bloquea todo lo demás | Crítica / Alta |
| Artículos (CRUD) | Muy alto — es el contenido principal | Alta |
| Control de acceso (autoría) | Muy alto — afecta integridad y confianza | Alta / Crítica |
| Comentarios | Medio — interacción social | Media |
| Favoritos | Medio — engagement del usuario | Media |
| Perfiles / Follow | Medio — construcción de comunidad | Media |
| Tags | Bajo — clasificación auxiliar | Baja |

---

## 4. Estrategia de Inyección de Bugs

> **¿Por qué inyectar bugs?**  
> Para validar que nuestra suite de pruebas es efectiva. Un conjunto de tests que no detecta los bugs que intencionalmente introducimos no tiene valor real. Esta técnica se llama *Mutation Testing* en su forma formal.

### 4.1 Criterios de Selección de Bugs

- Deben cubrir los tres tipos: **HTTP, Lógica y Validación**
- Deben estar distribuidos en diferentes módulos
- Deben tener severidades variadas (para poblar la matriz)
- Cada bug debe ser detectable por **al menos un caso de prueba** del plan
- No deben romper la aplicación completamente (para que las pruebas puedan ejecutarse)

### 4.2 Catálogo de Bugs a Inyectar (9 bugs)

| Bug ID | Tipo | Severidad | Módulo | Archivo a Modificar | Descripción del Bug |
|--------|------|-----------|--------|---------------------|---------------------|
| **BUG-01** | HTTP | Baja | Auth | `app/api/routes/auth.py` | `POST /api/users` retorna **HTTP 200** en lugar de **201 Created** al registrar un usuario exitosamente |
| **BUG-02** | Validación | Alta | Articles | `app/schemas/articles.py` | Se elimina la restricción `min_length=1` del campo `title`, permitiendo crear artículos con título vacío `""` |
| **BUG-03** | Lógica | Alta | Articles | `app/api/routes/articles.py` | Se elimina la verificación de autoría en `PUT /{slug}`, permitiendo que **cualquier usuario autenticado** edite un artículo ajeno |
| **BUG-04** | Seguridad | Crítica | Articles | `app/api/routes/articles.py` | Se elimina la verificación de autoría en `DELETE /{slug}`, permitiendo que **cualquier usuario autenticado** elimine un artículo ajeno |
| **BUG-05** | Lógica | Alta | Favorites | `app/api/routes/favorites.py` | El endpoint `POST /favorite` invierte la lógica: llama a `favorite=False` internamente, por lo que marcar como favorito en realidad lo desmarca (y viceversa) |
| **BUG-06** | Lógica | Media | Profiles | `app/models/user.py` | El método `profile()` siempre retorna `following=False` independientemente del estado real de la relación |
| **BUG-07** | HTTP | Alta | Articles | `app/api/routes/articles.py` | `GET /api/articles/feed` cambia `CurrentUser` por `OptionalCurrentUser`, por lo que no retorna **401** cuando se accede sin token; retorna 200 con lista vacía |
| **BUG-08** | Lógica | Media | Articles | `app/crud/crud_article.py` | El filtro `?tag=` en `GET /api/articles` se ignora internamente, retornando **todos los artículos** en lugar de los filtrados por tag |
| **BUG-09** | Validación | Media | Articles | `app/api/routes/articles.py` | El parámetro `limit` en `GET /api/articles` no está siendo capado al máximo de 20: si el cliente envía `?limit=100`, el sistema retorna hasta 100 artículos, ignorando el límite máximo definido |

### 4.3 Instrucciones de Inyección (cómo realizar cada bug)

> ⚠️ **IMPORTANTE:** Estos cambios se realizan en una **rama separada** de Git llamada `buggy-version`. Las pruebas se corren contra esa rama. La rama `main` conserva el código correcto.

**BUG-01** — `app/api/routes/auth.py`:
```python
# ANTES (correcto)
@router.post("", ..., status_code=201)

# DESPUÉS (con bug — cambiar a 200 o simplemente omitir status_code, FastAPI usa 200 por defecto)
@router.post("", ...)  # Sin status_code explícito → retorna 200
```

**BUG-02** — `app/schemas/articles.py`:
```python
# ANTES (correcto)
title: str = Field(..., min_length=1)

# DESPUÉS (con bug — remover la restricción)
title: str
```

**BUG-03 y BUG-04** — `app/api/routes/articles.py`:
```python
# ANTES (correcto) — dentro de update() y delete()
if article.author != current_user:
    raise HTTPException(status_code=400, detail="You are not the author of this article")

# DESPUÉS (con bug — comentar o eliminar el bloque de verificación)
# if article.author != current_user:  ← COMENTADO = BUG
#     raise HTTPException(...)
```

**BUG-05** — `app/api/routes/favorites.py`:
```python
# ANTES (correcto) — en el endpoint favorite()
await articles.favorite(db_obj=article, user=current_user)

# DESPUÉS (con bug — invertir el parámetro)
await articles.favorite(db_obj=article, user=current_user, favorite=False)
```

**BUG-06** — `app/models/user.py`:
```python
# ANTES (correcto) — método profile()
following=user is not None and self.followers.__contains__(user),

# DESPUÉS (con bug — siempre False)
following=False,
```

**BUG-07** — `app/api/routes/articles.py`:
```python
# ANTES (correcto) — firma del endpoint get_feed()
async def get_feed(current_user: CurrentUser, ...)

# DESPUÉS (con bug — autenticación opcional)
async def get_feed(current_user: OptionalCurrentUser, ...)
```

**BUG-08** — `app/crud/crud_article.py` (en el método `get_list`):
```python
# ANTES (correcto) — aplica el filtro por tag
if tag:
    query = query.join(Article.tags).filter(Tag.name == tag)

# DESPUÉS (con bug — comentar el filtro)
# if tag:
#     query = query.join(Article.tags).filter(Tag.name == tag)
```

**BUG-09** — `app/api/routes/articles.py` (en la función `get_list`):
```python
# ANTES (correcto) — usa min() para capar al máximo de 20
result, count = await articles.get_list(
    min(limit, max_limit),  ← ESTA LÍNEA PROTEGE EL LÍMITE
    offset, ...
)

# DESPUÉS (con bug — pasar limit directamente sin capar)
result, count = await articles.get_list(
    limit,  ← sin min(), acepta cualquier valor del cliente
    offset, ...
)
```

### 4.4 Flujo de Trabajo de Inyección

```
main (código limpio)
    └── git checkout -b buggy-version
            └── Aplicar los 9 bugs (uno por uno, probando que no rompen la app)
            └── git commit -m "chore: inject intentional bugs for QA testing"
            └── Ejecutar suite de pruebas
            └── Generar reporte de bugs
```

---

## 5. Distribución de los 40 Casos de Prueba

### 5.1 Resumen de Distribución

| Modo | Cantidad | Herramienta | Enfoque |
|------|----------|-------------|---------|
| **Manuales** | 15 | Swagger UI / Postman | Exploración, flujos de negocio, UX de la API |
| **Automatizados** | 25 | pytest + httpx | Integración, regresión, validación de contrato |
| **TOTAL** | **40** | | |

### 5.2 Convención de IDs

```
CP-[GRUPO]-[MODO]-[NÚMERO]
│    │       │      └── Número secuencial (001, 002...)
│    │       └── M = Manual / A = Automatizado
│    └── Para MANUALES: EXP (exploratorio) / TOOL (herramientas) / QUAL (calidad) / EST (estados)
│       Para AUTOMATIZADOS: AUTH / ART / COM / PRF / FAV / TAG
└── CP = Caso de Prueba
```

**Ejemplos:**
- `CP-EXP-M-001` → Caso Manual 001 de Exploración
- `CP-AUTH-A-001` → Caso Automatizado 001 del módulo Auth

### 5.3 Índice Maestro de los 40 Casos

#### PRUEBAS MANUALES (15) — Swagger UI o Postman

> **Por qué estas pruebas son genuinamente manuales:**  
> Para una API REST sin UI, lo que justifica la prueba manual NO es la comodidad, sino la naturaleza de lo que se evalúa. Aquí hay tres categorías que resisten la automatización: (1) **pruebas exploratorias** — por definición no se pueden scriptear porque se busca lo inesperado; (2) **pruebas de herramientas** — se evalúa Swagger UI y la colección Postman como artefactos, no el código; (3) **juicio cualitativo** — determinar si un mensaje de error es útil o si la estructura del JSON es legible requiere criterio humano, no un `assert`.

| ID | Nombre del Caso | Categoría | Prioridad | Por qué es manual | Bug detecta |
|----|-----------------|-----------|-----------|-------------------|------------|
| CP-EXP-M-001 | Flujo completo happy path: registro → login → crear artículo con tags → seguir usuario → ver feed → comentar → marcar favorito | Exploratorio | Alta | Valida el flujo de negocio completo de forma narrativa; un test automatizado sólo verifica pasos aislados, el humano detecta inconsistencias entre pasos | — |
| CP-EXP-M-002 | Enviar títulos con caracteres especiales: emojis (🚀), HTML (`<script>`), unicode árabe/chino, y observar los slugs generados | Exploratorio | Media | Comportamiento no especificado en el contrato; se explora para descubrir — no se puede scriptear lo que no se conoce de antemano | — |
| CP-EXP-M-003 | Enviar requests con tokens JWT manipulados: expirado, firma inválida, token de otro proyecto | Exploratorio | Alta | Prueba de seguridad exploratoria; se observa cómo responde el sistema ante variaciones no documentadas del token | — |
| CP-EXP-M-004 | Crear 25 artículos y solicitar `GET /api/articles?limit=100`; contar manualmente los resultados (BVA: límite máximo = 20) | Exploratorio | Media | Requiere construir estado real en la BD y observar el resultado cuantitativamente; complementa el test automatizado con evidencia visual | BUG-09 |
| CP-EXP-M-005 | Crear dos artículos con títulos muy similares (ej. "Mi Blog" y "mi blog") y observar si se genera el mismo slug o uno diferente | Exploratorio | Baja | Explora el comportamiento de la función `slugify` con entradas límite; detecta posibles colisiones de slug no cubiertas en spec | — |
| CP-TOOL-M-001 | Verificar en Swagger UI que los 19 endpoints están documentados correctamente: schemas de request/response, descripciones y parámetros | Herramientas | Media | Se evalúa Swagger UI como artefacto de documentación, no el código. Requiere lectura y juicio humano sobre claridad y completitud | — |
| CP-TOOL-M-002 | Usar el botón "Authorize" de Swagger UI con un token JWT y ejecutar 3 endpoints autenticados (GET /user, POST /articles, DELETE /articles/{slug}) | Herramientas | Alta | Prueba la experiencia de uso de Swagger UI como cliente de la API; valida que la autenticación interactiva funciona correctamente | — |
| CP-TOOL-M-003 | Importar `postman.json` en Postman y ejecutar la colección completa; documentar qué requests pasan y cuáles fallan | Herramientas | Alta | El archivo `postman.json` es un artefacto del repo. Se testea la colección misma como entregable, no solo el API | — |
| CP-QUAL-M-001 | Enviar datos inválidos en cada módulo (email sin @, contraseña vacía, slug inexistente) y evaluar si los mensajes de error son claros y útiles para un desarrollador | Calidad | Media | La claridad de un mensaje de error es un juicio subjetivo. Un `assert` verifica el status code, pero solo un humano evalúa si el mensaje tiene valor | — |
| CP-QUAL-M-002 | Revisar la estructura completa del JSON de respuesta de cada módulo y comparar campo a campo con la especificación RealWorld | Calidad | Alta | Validación del contrato de la API que requiere lectura comprensiva del spec y comparación visual estructurada | — |
| CP-QUAL-M-003 | Con dos usuarios: intentar editar el artículo del usuario A estando autenticado como usuario B; documentar la respuesta | Calidad | Alta | Verificación manual de BUG-03. Aunque el test automatizado lo detecta, la prueba manual produce la evidencia (screenshot) para el reporte de Mantis | BUG-03 |
| CP-QUAL-M-004 | Con dos usuarios: intentar eliminar el artículo del usuario A estando autenticado como usuario B; documentar la respuesta | Calidad | Crítica | Verificación manual de BUG-04. Caso de seguridad crítico que exige evidencia visual documentada para el reporte | BUG-04 |
| CP-EST-M-001 | Flujo de transición de estado de follow: seguir usuario A → verificar `following: true` → dejar de seguir → verificar `following: false` | Estados | Media | Observación del ciclo completo de un estado de negocio; permite detectar BUG-06 visualmente y obtener evidencia para Mantis | BUG-06 |
| CP-EST-M-002 | Flujo de transición de favoritos: marcar favorito → verificar `favorited: true` y `favoritesCount +1` → desmarcar → verificar `favorited: false` y `favoritesCount -1` | Estados | Media | Validación end-to-end del sistema de favoritos observando el contador en cada paso; produce evidencia visual de BUG-05 | BUG-05 |
| CP-EST-M-003 | Eliminar artículo propio y luego hacer `GET /api/articles/{slug}` del mismo; verificar que retorna 404 | Estados | Media | Valida la transición de estado: recurso existente → eliminado → no encontrado. Simple pero importante para confirmar integridad referencial | — |

#### PRUEBAS AUTOMATIZADAS (25) — pytest

| ID | Nombre del Caso | Módulo | Prioridad | Bug que detecta |
|----|-----------------|--------|-----------|-----------------|
| CP-AUTH-A-001 | Registro retorna HTTP 201 (no 200) | Auth | Alta | BUG-01 |
| CP-AUTH-A-002 | Token JWT es retornado en registro exitoso | Auth | Alta | — |
| CP-AUTH-A-003 | Login retorna token JWT válido | Auth | Alta | — |
| CP-AUTH-A-004 | Login con email inexistente retorna 400 | Auth | Alta | — |
| CP-AUTH-A-005 | Registro con email duplicado retorna 400 | Auth | Alta | — |
| CP-ART-A-001 | Crear artículo con datos válidos retorna 200 y estructura correcta | Articles | Alta | — |
| CP-ART-A-002 | Crear artículo con título vacío retorna 422 | Articles | Alta | BUG-02 |
| CP-ART-A-003 | Crear artículo sin autenticación retorna 401 | Articles | Alta | — |
| CP-ART-A-004 | Editar artículo como autor retorna artículo actualizado | Articles | Alta | — |
| CP-ART-A-005 | Editar artículo como no-autor retorna 400 | Articles | Alta | BUG-03 |
| CP-ART-A-006 | Eliminar artículo como no-autor retorna 400 | Articles | Crítica | BUG-04 |
| CP-ART-A-007 | Feed sin autenticación retorna 401 | Articles | Alta | BUG-07 |
| CP-ART-A-008 | Filtrar artículos por tag devuelve solo artículos con ese tag | Articles | Media | BUG-08 |
| CP-ART-A-009 | Solicitar `?limit=100` con más de 20 artículos en BD retorna máximo 20 (BVA) | Articles | Media | BUG-09 |
| CP-COM-A-001 | Crear comentario en artículo existente retorna comentario | Comments | Media | — |
| CP-COM-A-002 | Crear comentario sin autenticación retorna 401 | Comments | Media | — |
| CP-COM-A-003 | Eliminar comentario como autor del comentario | Comments | Media | — |
| CP-COM-A-004 | Obtener comentarios de artículo inexistente retorna 404 | Comments | Media | — |
| CP-PRF-A-001 | Seguir usuario cambia `following` a `true` | Profiles | Media | BUG-06 |
| CP-PRF-A-002 | Dejar de seguir cambia `following` a `false` | Profiles | Media | BUG-06 |
| CP-PRF-A-003 | Obtener perfil de usuario inexistente retorna 404 | Profiles | Media | — |
| CP-PRF-A-004 | Seguir sin autenticación retorna 401 | Profiles | Media | — |
| CP-FAV-A-001 | Marcar favorito incrementa `favoritesCount` en 1 | Favorites | Media | BUG-05 |
| CP-FAV-A-002 | Desmarcar favorito decrementa `favoritesCount` en 1 | Favorites | Media | BUG-05 |
| CP-TAG-A-001 | `GET /api/tags` retorna lista de tags existentes | Tags | Baja | — |
| CP-TAG-A-002 | Tags de artículo creado aparecen en `/api/tags` | Tags | Baja | — |

### 5.4 Cobertura de Módulos

```
Grupo/Módulo     Manual  Auto  Total  Bugs cubiertos
─────────────────────────────────────────────────────
Exploratorio      5      0      5    BUG-09
Herramientas      3      0      3    —
Calidad           4      0      4    BUG-03, BUG-04
Estados           3      0      3    BUG-05, BUG-06
─────────────────────────────────────────────────────
Auth              0      5      5    BUG-01
Articles          0      9     9    BUG-02,03,04,07,08,09
Comments          0      4      4    —
Profiles          0      4      4    BUG-06
Favorites         0      2      2    BUG-05
Tags              0      2      2    —
─────────────────────────────────────────────────────
TOTAL            15     26     41    9/9 bugs cubiertos ✅

Nota: 41 > 40 mínimo exigido por la docente. El caso extra (CP-ART-A-009) cubre BUG-09.
```

---

## 6. Matriz de Severidad y Prioridad

> **Recordatorio de clase:**  
> - **Severidad** = impacto técnico en el sistema (dimensión objetiva)  
> - **Prioridad** = urgencia de resolución según el negocio (dimensión de gestión)  
> Son métricas **independientes**. Un bug puede ser severidad alta y prioridad baja (o viceversa).

### 6.1 Definición de Niveles para este Proyecto

#### Severidad

| Nivel | Criterio aplicado a esta API | Ejemplo |
|-------|------------------------------|---------|
| **Crítica** | El sistema expone una vulnerabilidad de seguridad que compromete datos de usuarios, O un flujo de negocio principal queda completamente inutilizable | Un usuario puede borrar artículos ajenos |
| **Alta** | Una funcionalidad de negocio importante no funciona correctamente pero el sistema sigue activo | Artículos se pueden crear sin título; el feed no requiere auth |
| **Media** | Una funcionalidad secundaria falla, o el contrato de la API (estructura del JSON / status codes) no es el esperado | `following` siempre retorna `false`; filtro por tag ignorado |
| **Baja** | Inconsistencia menor que no afecta funcionalidad pero viola el contrato HTTP | `POST /users` retorna 200 en vez de 201 |

#### Prioridad

| Nivel | Criterio de negocio |
|-------|---------------------|
| **Alta** | Debe corregirse antes de cualquier despliegue. Afecta la confianza o seguridad de los usuarios |
| **Media** | Debe corregirse en el próximo ciclo de desarrollo. Afecta la experiencia pero tiene workaround |
| **Baja** | Puede diferirse a la siguiente versión. No afecta funcionalidad core |

### 6.2 Matriz de Bugs Inyectados

| Bug ID | Severidad | Prioridad | Justificación |
|--------|-----------|-----------|---------------|
| BUG-04 | **Crítica** | **Alta** | Eliminar artículos de otros usuarios es una brecha de seguridad inaceptable en cualquier plataforma de contenido |
| BUG-03 | **Alta** | **Alta** | Editar artículos ajenos viola la integridad del contenido y la confianza del autor |
| BUG-07 | **Alta** | **Alta** | El feed es una funcionalidad premium autenticada; que funcione sin auth es un bug de autorización |
| BUG-02 | **Alta** | **Alta** | Artículos sin título no tienen sentido en una plataforma de blogs; indica validación rota |
| BUG-05 | **Alta** | **Media** | El sistema de favoritos no funciona correctamente; afecta el engagement pero no la seguridad |
| BUG-06 | **Media** | **Media** | El estado de seguimiento siempre falso degrada la experiencia del feed y la comunidad |
| BUG-08 | **Media** | **Media** | El filtro por tag es una función de descubrimiento de contenido; su falla afecta la UX |
| BUG-09 | **Media** | **Media** | El límite de páginación es una protección de rendimiento; ignorarlo podría saturar la DB con peticiones grandes |
| BUG-01 | **Baja** | **Baja** | El status code 200 vs 201 es una violación del contrato REST, pero no afecta funcionalidad |

---

## 7. Estándar de Documentación de Casos

### 7.1 Plantilla Adaptada para API REST

Todos los casos de prueba se documentarán usando esta plantilla. Los casos manuales se completarán en un documento Markdown o tabla Excel. Los casos automatizados tendrán su código en `tests/`.

```
┌─────────────────────────────────────────────────────────────────────┐
│ ID del Caso     │ CP-[MOD]-[MODO]-[NUM]                             │
│ Nombre          │ [Acción + objeto + condición]                     │
│ Módulo          │ [Auth / Articles / Comments / Profiles / ...]     │
│ Tipo de Prueba  │ [ ] Funcional  [X] Integración  [ ] Seguridad    │
│ Modo            │ [ ] Manual  [ ] Automatizado                      │
│ Técnica BVA/EP  │ [EP / BVA / Error Guessing / Tabla de Decisión]  │
│ Prioridad       │ [ ] Alta  [ ] Media  [ ] Baja                    │
├─────────────────────────────────────────────────────────────────────┤
│ PRECONDICIONES  │                                                   │
│                 │ 1. La API está corriendo en localhost:8000        │
│                 │ 2. [Datos de usuario/artículo necesarios]        │
│                 │ 3. [Token JWT activo si aplica]                  │
├─────────────────────────────────────────────────────────────────────┤
│ DATOS DE ENTRADA │                                                  │
│ Endpoint        │ POST /api/articles                               │
│ Headers         │ Authorization: Bearer {token}                    │
│                 │ Content-Type: application/json                   │
│ Body (JSON)     │ { "article": { "title": "Mi Artículo",          │
│                 │               "description": "Desc",            │
│                 │               "body": "Cuerpo" } }              │
├─────────────────────────────────────────────────────────────────────┤
│ PASOS           │                                                   │
│                 │ 1. Abrir Swagger UI en /docs (o Postman)         │
│                 │ 2. Autenticarse con el token del usuario         │
│                 │ 3. Enviar la petición con los datos indicados    │
│                 │ 4. Observar el código de estado y el body        │
├─────────────────────────────────────────────────────────────────────┤
│ RESULTADO       │ HTTP 200 OK                                       │
│ ESPERADO        │ Body contiene: { "article": { "title": ...,      │
│                 │   "slug": "mi-articulo", "author": {...} } }     │
├─────────────────────────────────────────────────────────────────────┤
│ RESULTADO       │ [Completar durante la ejecución]                 │
│ OBTENIDO        │                                                   │
├─────────────────────────────────────────────────────────────────────┤
│ ESTADO          │ [ ] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloq │
│ DEFECTO ASOC.   │ [DEF-XXX] / N/A                                  │
│ FECHA EJECUCIÓN │ [DD/MM/AAAA]                                     │
│ OBSERVACIONES   │ [Notas relevantes sobre la ejecución]            │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 Reglas de Nomenclatura y Documentación

1. **El nombre del caso debe ser descriptivo:** No usar "Prueba 1" sino "Crear artículo con título vacío retorna 422 Unprocessable Entity"
2. **El resultado esperado debe ser específico:** Incluir siempre el código HTTP y la estructura del JSON relevante
3. **Una técnica por caso:** Aplicar EP, BVA, Error Guessing o Tabla de Decisión conscientemente
4. **Trazabilidad:** Cada caso que detecta un bug debe referenciar el Bug ID
5. **Evidencia:** Los casos manuales deben adjuntar screenshot de Swagger/Postman. Los automatizados generan log de pytest

### 7.3 Técnicas Aplicadas por Módulo

| Módulo | Técnica principal | Aplicación concreta |
|--------|-------------------|---------------------|
| Auth | **EP** + **BVA** | Emails válidos/inválidos, contraseñas vacías vs. válidas |
| Articles (crear) | **EP** + **BVA** | Título vacío ("") vs. normal, límite de caracteres |
| Articles (filtros) | **Tabla de Decisión** | Combinaciones de filtros: ?tag, ?author, ?favorited |
| Autorización | **Tabla de Decisión** | Usuario autenticado/no autenticado × recurso propio/ajeno |
| Profiles/Follow | **Transición de Estados** | Estado `following`: false → true (follow) → false (unfollow) |
| Favoritos | **Transición de Estados** | Estado `favorited`: false → true → false, y contador |

---

## 8. Stack de Herramientas

### 8.1 Herramientas de Ejecución

| Categoría | Herramienta | Propósito | Modo |
|-----------|-------------|-----------|------|
| **Documentación interactiva** | Swagger UI (`/docs`) | Ejecutar pruebas manuales visualmente, explorar contratos | Manual |
| **Cliente HTTP** | Postman (postman.json incluido) | Ejecutar y documentar pruebas manuales; organizar colecciones | Manual |
| **Framework de pruebas** | pytest 9.x | Correr la suite automatizada | Automatizado |
| **Cliente HTTP (tests)** | httpx + TestClient (FastAPI) | Hacer peticiones HTTP dentro de pytest | Automatizado |
| **Soporte async** | pytest-asyncio | Habilitar pruebas con funciones `async def` | Automatizado |
| **Cobertura de código** | pytest-cov | Medir qué % del código fuente ejecutan los tests | Automatizado |
| **Control de versiones** | Git (rama `buggy-version`) | Aislar los bugs inyectados del código limpio | Ambos |

### 8.2 Herramientas de Entorno

| Categoría | Herramienta | Propósito |
|-----------|-------------|-----------|
| **Levantamiento del entorno** | Docker + Docker Compose | Levantar PostgreSQL y la API con un comando |
| **Gestor de dependencias** | uv (pyproject.toml) | Instalar dependencias de Python reproduciblemente |
| **Base de datos de pruebas** | SQLite o PostgreSQL (test) | BD aislada para que los tests no afecten producción |

### 8.3 Herramientas de Reportes

| Categoría | Herramienta | Propósito |
|-----------|-------------|-----------|
| **Reporte HTML de tests** | pytest-html | Generar reporte visual de la ejecución automatizada |
| **Reporte JSON** | pytest --json-report | Exportar resultados en JSON para el dashboard |
| **Dashboard de métricas** | AI + datos exportados de pytest | [Tu compañera] genera visualizaciones a partir de los datos (ver sección 10) |
| **Gestión de bugs** | **MantisBT** | [Tu compañera] registra y da seguimiento a los defectos detectados |

### 8.4 Comandos Clave

```bash
# Levantar la API con Docker
docker compose up -d

# Instalar dependencias (con uv)
uv sync

# Correr TODOS los tests
uv run pytest tests/ -v

# Correr tests de un módulo específico
uv run pytest tests/api/articles/ -v

# Correr tests con reporte de cobertura
uv run pytest tests/ --cov=app --cov-report=html

# Correr tests con reporte HTML (requiere pytest-html)
uv run pytest tests/ --html=docs_qa/reports/test_report.html

# Correr tests con reporte JSON (requiere pytest-json-report)
uv run pytest tests/ --json-report --json-report-file=docs_qa/reports/results.json

# Ver la API en Swagger UI (una vez levantada)
# http://localhost:8000/docs
```

---

## 9. Reporte de Bugs — Flujo hacia MantisBT

> El registro y seguimiento de bugs se hace en **MantisBT**. Tu compañera es la responsable de operar la plataforma. Tu trabajo es detectar el bug y entregarle la información estructurada para que ella lo cargue.

### 9.1 Flujo de Trabajo

```
[Tú detectas el bug]                    [Tu compañera carga en Mantis]
      │                                           │
      ├── Test automatizado falla (pytest)          ├── Crea el ticket
      ├── Prueba manual evidencia el bug            ├── Asigna severidad y prioridad
      └── Le pasas la ficha de bug (ver 9.2)        ├── Adjunta evidencia (screenshot/log)
                                                  └── Hace seguimiento del estado
```

### 9.2 Ficha de Bug (lo que debes entregarle a tu compañera por cada defecto)

Esta ficha es el insumo que ella necesita para cargar el ticket en Mantis. Prepárala en texto plano o Markdown.

```
TÍTULO:        [Descripción corta del bug, max 80 caracteres]
CP ASOCIADO:   [ID del caso de prueba que lo detectó]
MÓDULO:       [Auth / Articles / Comments / Profiles / Favorites / Tags]
SEVERIDAD:     [Crítica / Alta / Media / Baja]
PRIORIDAD:     [Alta / Media / Baja]
ENTORNO:       localhost:8000, rama buggy-version, Python 3.15

DESCRIPCIÓN:
[Qué comportamiento incorrecto se observa y por qué es un bug.]

PASOS PARA REPRODUCIR:
1. [Paso concreto, incluir endpoint, método y body exacto si aplica]
2. ...

RESULTADO ESPERADO: [Código HTTP + descripción del comportamiento correcto]
RESULTADO OBTENIDO: [Código HTTP + descripción de lo que realmente pasa]

EVIDENCIA: [Screenshot de Postman/Swagger / output del terminal de pytest]
```

### 9.3 Campos de MantisBT que tu compañera debe mapear

| Ficha (tu insumo) | Campo en MantisBT |
|-------------------|-----------------|
| Título | Summary |
| Módulo | Category |
| Severidad | Severity |
| Prioridad | Priority |
| Descripción | Description |
| Pasos para reproducir | Steps to Reproduce |
| Resultado esperado / obtenido | Additional Information |
| Evidencia | Attachments |

### 9.4 Estados en Mantis para este proyecto

```
New → Confirmed → Assigned → Resolved → Closed
                                   ↑__________↓  (si se reabre: Feedback)
```

Para el taller: **New** al detectar, **Resolved** al documentar que fue un bug inyectado, **Closed** al verificar.

---

## 10. Propuesta de Dashboard de Métricas

### 10.1 Métricas a Medir (alineadas con el plan de la docente)

| # | Métrica | Fórmula | Meta del proyecto |
|---|---------|---------|-------------------|
| 1 | **Tasa de ejecución de casos** | (Casos ejecutados / Total casos) × 100 | ≥ 95% |
| 2 | **Tasa de casos aprobados** | (Casos Pasaron / Casos ejecutados) × 100 | ≥ 80% (buscamos fallos) |
| 3 | **Densidad de defectos** | Defectos encontrados / Casos ejecutados | Esperamos ~0.2 (8 bugs / 40 casos) |
| 4 | **Defectos por severidad** | Conteo agrupado por nivel | Ver distribución BUG-01 a BUG-08 |
| 5 | **Cobertura de código** | pytest-cov (líneas ejecutadas / total) | ≥ 70% |
| 6 | **Tasa de detección de bugs inyectados** | (Bugs detectados / Bugs inyectados) × 100 | 100% (los 8 bugs) |
| 7 | **Defectos críticos abiertos** | Conteo directo | 0 al cierre |
| 8 | **Tasa de reapertura** | (Bugs reabiertos / Bugs resueltos) × 100 | < 5% |

### 10.2 Estrategia: generar los datos, la IA hace el resto

No necesitas escribir scripts de visualización. Tu único trabajo es **generar los archivos de datos** con los resultados reales; la IA que elijas se encargará de convertirlos en gráficas y el dashboard.

**Paso 1 — Generar los datos al final de la ejecución:**

```bash
# Reporte JSON de pytest (resultados de todos los tests)
uv run pytest tests/ -v \
  --json-report \
  --json-report-file=docs_qa/data/pytest_results.json

# Reporte de cobertura en JSON
uv run pytest tests/ \
  --cov=app \
  --cov-report=json:docs_qa/data/coverage.json
```

**Paso 2 — Tabla resumen manual (completar al terminar la ejecución):**

Guardar esto en `docs_qa/data/resumen_metricas.md` con los valores reales:

```markdown
| Métrica                         | Valor real  | Meta    |
|---------------------------------|-------------|----------
| Total casos diseñados           | 41          | —       |
| Casos manuales ejecutados       | XX / 15     | 15/15   |
| Casos automatizados ejecutados  | XX / 26     | 26/26   |
| Casos que pasaron                | XX          | ≥ 80%  |
| Casos que fallaron               | XX          | —       |
| Bugs inyectados detectados      | XX / 9      | 9/9     |
| Bugs por severidad (Crítica)    | XX          | 1       |
| Bugs por severidad (Alta)       | XX          | 4       |
| Bugs por severidad (Media)      | XX          | 3       |
| Bugs por severidad (Baja)       | XX          | 1       |
| Cobertura de código (pytest-cov) | XX%        | ≥ 70%  |
| Defectos críticos abiertos      | XX          | 0       |
```

**Paso 3 — Pasar los archivos a la IA:**  
Entregarle a la IA los archivos `pytest_results.json`, `coverage.json` y `resumen_metricas.md` con el prompt:  
*"Genera un dashboard visual en HTML con gráficas de pie y barras con estos datos de resultados de pruebas de software."*

---

## 11. Cronograma de Ejecución

> Las fechas son referenciales. Ajustarlas según las fechas reales de entrega del taller.

| Fase | Actividad | Duración estimada | Entregable |
|------|-----------|-------------------|------------|
| **Fase 1 — Setup** | Leer plan, clonar repo, levantar entorno con Docker, explorar Swagger UI | 2 horas | Entorno funcionando |
| **Fase 2 — Diseño** | Documentar los 40 casos de prueba en detalle | 4 horas | `docs_qa/Casos_De_Prueba.md` |
| **Fase 3 — Inyección** | Crear rama `buggy-version` e inyectar los 9 bugs | 1.5 horas | Rama con bugs en Git |
| **Fase 4 — Pruebas manuales** | Ejecutar los 15 casos manuales en Swagger/Postman | 3 horas | Evidencias (screenshots) |
| **Fase 5 — Pruebas automáticas** | Escribir y ejecutar los 25 casos automatizados en pytest | 6 horas | Archivos en `tests/` |
| **Fase 6 — Reporte de bugs** | Preparar las 9 fichas de bug y parsárselas a tu compañera para cargar en Mantis | 2 horas | Tickets en MantisBT + `docs_qa/data/resumen_metricas.md` |
| **Fase 7 — Dashboard** | Generar archivos `pytest_results.json` y `coverage.json`; pasarlos a la IA para generar visualizaciones | 1 hora | `docs_qa/data/` + dashboard generado |
| **Fase 8 — Análisis** | Escribir el análisis de calidad final | 2 horas | `docs_qa/Analisis_Calidad.md` |
| **TOTAL** | | **~22 horas** | |

---

## 12. Riesgos del Plan

| # | Riesgo | Probabilidad | Impacto | Plan de Mitigación |
|---|--------|-------------|---------|-------------------|
| R1 | La API no levanta en el entorno local (problemas con Docker o DB) | Media | Alto | Usar SQLite como BD alternativa para pruebas; documentar la configuración paso a paso |
| R2 | Los bugs inyectados no son detectados por los tests (tests mal diseñados) | Baja | Alto | Verificar que cada bug tiene al menos un caso de prueba que lo referencia; hacer smoke test manual primero |
| R3 | Falta de tiempo para los 25 casos automatizados | Media | Medio | Priorizar módulos Auth y Articles; los módulos Tags y menor prioridad pueden reducirse |
| R4 | Bug inyectado rompe completamente la aplicación | Baja | Alto | Probar cada bug en aislamiento antes de commitear todos juntos |
| R5 | Dificultad con pytest-asyncio (tests async) | Media | Medio | Revisar la configuración existente en `conftest.py` y `pyproject.toml`; la base ya está lista |

---

## 13. Checklist de Entregables

> Para usar al final del taller. Marcar cada ítem como completado antes de entregar.

| # | Entregable | Archivo/Ubicación | Estado |
|---|-----------|-------------------|--------|
| 1 | **Descripción del sistema** | Este documento (§1) | ✅ Incluido |
| 2 | **Plan de pruebas** (plantilla docente) | `docs_qa/plan_pruebas (1).md` rellenado | ⬜ Pendiente |
| 3 | **Plan de acción / Estrategia** | `docs_qa/Plan_De_Accion.md` (este archivo) | ✅ Completo |
| 4 | **40 Casos de prueba documentados** | `docs_qa/Casos_De_Prueba.md` | ⬜ Pendiente |
| 5 | **Scripts de prueba automatizados** | `tests/api/` | ⬜ Pendiente |
| 6 | **Reporte de bugs (9 defectos en MantisBT)** | Tickets en MantisBT + fichas en `docs_qa/data/` | ⬜ Pendiente |
| 7 | **Dashboard de métricas** | `docs_qa/data/pytest_results.json` + `coverage.json` + HTML generado | ⬜ Pendiente |
| 8 | **Análisis de calidad** | `docs_qa/Analisis_Calidad.md` | ⬜ Pendiente |
| 9 | **Evidencias manuales** (screenshots) | `docs_qa/evidencias/` | ⬜ Pendiente |
| 10 | **Rama con bugs** en Git | Rama `buggy-version` (9 bugs) | ⬜ Pendiente |

---

*Documento elaborado como hoja de ruta del taller universitario de Pruebas de Software.*  
*Basado en la plantilla de la docente, los apuntes de clase (Compendio Técnico ISTQB) y el análisis del repositorio FastAPI RealWorld Example App.*
