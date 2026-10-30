# Casos de Prueba — Conduit API QA

| **Proyecto** | FastAPI RealWorld Example App — Conduit (Backend API) |
|---|---|
| **Total de casos** | 41 (15 manuales + 26 automatizados) |
| **Plantilla** | §7.1 del Plan de Pruebas |
| **Responsable** | [Tu nombre] |

---

## ÍNDICE RÁPIDO

| ID | Nombre resumido | Modo | Prioridad |
|----|-----------------|------|-----------|
| CP-EXP-M-001 | Flujo completo happy path | Manual | Alta |
| CP-EXP-M-002 | Caracteres especiales en títulos | Manual | Media |
| CP-EXP-M-003 | Tokens JWT manipulados | Manual | Alta |
| CP-EXP-M-004 | BVA: limit=100 con 25+ artículos | Manual | Media |
| CP-EXP-M-005 | Colisión de slugs con títulos similares | Manual | Baja |
| CP-TOOL-M-001 | Swagger UI — verificar 19 endpoints documentados | Manual | Media |
| CP-TOOL-M-002 | Swagger UI — flujo autenticado con Bearer | Manual | Alta |
| CP-TOOL-M-003 | Postman — ejecutar colección postman.json | Manual | Alta |
| CP-QUAL-M-001 | Calidad de mensajes de error | Manual | Media |
| CP-QUAL-M-002 | Estructura JSON vs RealWorld Spec | Manual | Alta |
| CP-QUAL-M-003 | Editar artículo ajeno como no-autor (Swagger) | Manual | Alta |
| CP-QUAL-M-004 | Eliminar artículo ajeno como no-autor (Swagger) | Manual | Crítica |
| CP-EST-M-001 | Transición follow → unfollow | Manual | Media |
| CP-EST-M-002 | Transición marcar → desmarcar favorito | Manual | Media |
| CP-EST-M-003 | Eliminar artículo propio y verificar 404 | Manual | Media |
| CP-AUTH-A-001 | Registro retorna HTTP 201 | Automatizado | Alta |
| CP-AUTH-A-002 | Registro retorna token JWT en body | Automatizado | Alta |
| CP-AUTH-A-003 | Login retorna token JWT válido | Automatizado | Alta |
| CP-AUTH-A-004 | Login con email inexistente retorna 400 | Automatizado | Alta |
| CP-AUTH-A-005 | Registro con email duplicado retorna 400 | Automatizado | Alta |
| CP-ART-A-001 | Crear artículo válido retorna estructura correcta | Automatizado | Alta |
| CP-ART-A-002 | Crear artículo con título vacío retorna 422 | Automatizado | Alta |
| CP-ART-A-003 | Crear artículo sin autenticación retorna 401 | Automatizado | Alta |
| CP-ART-A-004 | Editar artículo como autor retorna artículo actualizado | Automatizado | Alta |
| CP-ART-A-005 | Editar artículo ajeno retorna 400 | Automatizado | Alta |
| CP-ART-A-006 | Eliminar artículo ajeno retorna 400 | Automatizado | Crítica |
| CP-ART-A-007 | GET /feed sin autenticación retorna 401 | Automatizado | Alta |
| CP-ART-A-008 | Filtrar artículos por tag retorna solo los correctos | Automatizado | Media |
| CP-ART-A-009 | limit=100 retorna máximo 20 artículos | Automatizado | Media |
| CP-COM-A-001 | Crear comentario en artículo existente | Automatizado | Media |
| CP-COM-A-002 | Crear comentario sin autenticación retorna 401 | Automatizado | Media |
| CP-COM-A-003 | Eliminar comentario propio | Automatizado | Media |
| CP-COM-A-004 | GET comentarios de artículo inexistente retorna 404 | Automatizado | Media |
| CP-PRF-A-001 | Seguir usuario cambia following a true | Automatizado | Media |
| CP-PRF-A-002 | Dejar de seguir cambia following a false | Automatizado | Media |
| CP-PRF-A-003 | GET perfil inexistente retorna 404 | Automatizado | Media |
| CP-PRF-A-004 | Seguir usuario sin autenticación retorna 401 | Automatizado | Media |
| CP-FAV-A-001 | Marcar favorito incrementa favoritesCount en 1 | Automatizado | Media |
| CP-FAV-A-002 | Desmarcar favorito decrementa favoritesCount en 1 | Automatizado | Media |
| CP-TAG-A-001 | GET /api/tags retorna lista ordenada | Automatizado | Baja |
| CP-TAG-A-002 | Tags de artículo creado aparecen en GET /api/tags | Automatizado | Baja |

---

## PRUEBAS MANUALES

---

### CP-EXP-M-001

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-EXP-M-001 |
| **Nombre** | Flujo completo de usuario: registro → login → artículo → seguir → feed → comentar → favoritar |
| **Funcionalidad / Endpoint cubierto** | Múltiples: `POST /api/users`, `POST /api/users/login`, `POST /api/articles`, `POST /api/profiles/{username}/follow`, `GET /api/articles/feed`, `POST /api/articles/{slug}/comments`, `POST /api/articles/{slug}/favorite` |
| **Precondiciones** | API corriendo en `http://localhost:8000`. Base de datos limpia (sin usuarios previos). Swagger UI accesible en `http://localhost:8000/docs`. |
| **Datos de entrada** | **Usuario A:** `{"user": {"username": "usuarioA", "email": "usuarioa@test.com", "password": "password123"}}`<br>**Usuario B:** `{"user": {"username": "usuarioB", "email": "usuariob@test.com", "password": "password123"}}`<br>**Artículo:** `{"article": {"title": "Artículo de Prueba", "description": "Descripción", "body": "Contenido del artículo", "tagList": ["test", "qa"]}}` |
| **Pasos de ejecución** | 1. Abrir `http://localhost:8000/docs`<br>2. Registrar Usuario A con `POST /api/users`<br>3. Registrar Usuario B con `POST /api/users`<br>4. Hacer login como Usuario B con `POST /api/users/login`, copiar el token<br>5. Clicar "Authorize" en Swagger, ingresar `Bearer {token de B}`, clicar Authorize<br>6. Crear un artículo como Usuario B con `POST /api/articles`<br>7. Hacer login como Usuario A, copiar token y re-autenticarse en Swagger<br>8. Seguir a Usuario B con `POST /api/profiles/usuarioB/follow`<br>9. Verificar feed con `GET /api/articles/feed` — el artículo de B debe aparecer<br>10. Comentar el artículo de B con `POST /api/articles/{slug}/comments`<br>11. Marcar el artículo de B como favorito con `POST /api/articles/{slug}/favorite`<br>12. Verificar el artículo con `GET /api/articles/{slug}` — observar `favorited` y `favoritesCount` |
| **Resultado esperado** | Cada endpoint retorna HTTP 200. El feed de A muestra el artículo de B. El comentario aparece en la respuesta. El campo `favorited` es `true` y `favoritesCount` es `1` en el artículo final. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [ ] Funcional  [ ] Regresión  [x] Integración  [ ] Seguridad  [x] Exploratoria |
| **Modo** | [x] Manual (Swagger UI)  [ ] Automatizado |
| **Técnica aplicada** | [x] Exploratoria |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Tomar screenshot de cada paso clave. Este caso valida el flujo narrativo completo de negocio; los casos individuales cubren los endpoints de forma aislada. |

---

### CP-EXP-M-002

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-EXP-M-002 |
| **Nombre** | Crear artículos con caracteres especiales en el título y observar los slugs generados |
| **Funcionalidad / Endpoint cubierto** | `POST /api/articles` |
| **Precondiciones** | Usuario autenticado en Swagger UI. |
| **Datos de entrada** | Se prueban 4 variantes de título:<br>**Variante 1:** `"title": "Artículo con emoji 🚀"`<br>**Variante 2:** `"title": "<script>alert('xss')</script>"`<br>**Variante 3:** `"title": "مقالة عربية"` (árabe)<br>**Variante 4:** `"title": "日本語タイトル"` (japonés)<br>Todos con `"description": "Desc"`, `"body": "Body"` |
| **Pasos de ejecución** | 1. Autenticarse en Swagger UI con token válido<br>2. Para cada variante de título, ejecutar `POST /api/articles` con el body correspondiente<br>3. Anotar el `slug` retornado en cada respuesta<br>4. Intentar acceder al artículo con `GET /api/articles/{slug}` usando el slug obtenido<br>5. Registrar: ¿el slug es URL-safe? ¿el artículo es accesible? ¿hay errores inesperados? |
| **Resultado esperado** | La API acepta los títulos y retorna HTTP 200. El slug generado es URL-safe (sin emojis, sin HTML, sin caracteres no ASCII). El artículo es accesible por su slug. El contenido HTML no se ejecuta como código. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [ ] Integración  [ ] Seguridad  [x] Exploratoria |
| **Modo** | [x] Manual (Swagger UI)  [ ] Automatizado |
| **Técnica aplicada** | [x] Exploratoria |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Documentar el slug generado para cada variante. Si alguna variante genera un error 500 o un slug vacío, reportar como defecto. |

---

### CP-EXP-M-003

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-EXP-M-003 |
| **Nombre** | Acceder a endpoints protegidos con tokens JWT inválidos o manipulados |
| **Funcionalidad / Endpoint cubierto** | `GET /api/user` (endpoint protegido como representante de todos los endpoints con autenticación requerida) |
| **Precondiciones** | API corriendo. Postman abierto con request `GET http://localhost:8000/api/user`. |
| **Datos de entrada** | Se prueban 4 variantes de token en el header `Authorization`:<br>**Variante 1:** `Bearer not.a.jwt.at.all`<br>**Variante 2:** `Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.FIRMA_INVALIDA`<br>**Variante 3:** Sin header `Authorization` (omitirlo completamente)<br>**Variante 4:** `Bearer ` (Bearer con espacio y sin token) |
| **Pasos de ejecución** | 1. Abrir Postman, crear request `GET http://localhost:8000/api/user`<br>2. Enviar Variante 1 en Authorization → anotar código y mensaje<br>3. Enviar Variante 2 → anotar código y mensaje<br>4. Enviar Variante 3 (sin Authorization) → anotar código y mensaje<br>5. Enviar Variante 4 → anotar código y mensaje<br>6. Tomar screenshot de cada respuesta |
| **Resultado esperado** | HTTP 401 Unauthorized en las cuatro variantes. El cuerpo de respuesta no revela información sensible del sistema. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [ ] Integración  [x] Seguridad  [x] Exploratoria |
| **Modo** | [x] Manual (Postman)  [ ] Automatizado |
| **Técnica aplicada** | [x] EP (particiones inválidas del token) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Si alguna variante retorna 200 o 500 en lugar de 401, documentar como defecto de seguridad. |

---

### CP-EXP-M-004

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-EXP-M-004 |
| **Nombre** | BVA: solicitar `limit=100` con 25+ artículos y verificar que se retornan máximo 20 |
| **Funcionalidad / Endpoint cubierto** | `GET /api/articles?limit={n}` |
| **Precondiciones** | Al menos 25 artículos creados en la base de datos. Se pueden crear usando el script de seed del proyecto (`app/seed.py`) o manualmente via Swagger UI. |
| **Datos de entrada** | Se prueban 4 valores límite (BVA alrededor del máximo = 20):<br>**Valor 1:** `?limit=19` (justo por debajo del máximo)<br>**Valor 2:** `?limit=20` (exactamente en el límite)<br>**Valor 3:** `?limit=21` (un punto sobre el límite)<br>**Valor 4:** `?limit=100` (muy por encima del límite) |
| **Pasos de ejecución** | 1. Crear 25 artículos en la BD (manualmente o via seed)<br>2. En Swagger UI, ejecutar `GET /api/articles?limit=19` → contar artículos en `articles[]`<br>3. Ejecutar `GET /api/articles?limit=20` → contar artículos<br>4. Ejecutar `GET /api/articles?limit=21` → contar artículos<br>5. Ejecutar `GET /api/articles?limit=100` → contar artículos<br>6. Comparar `len(articles)` vs `articlesCount` en cada respuesta |
| **Resultado esperado** | `?limit=19` → 19 artículos. `?limit=20` → 20 artículos. `?limit=21` → máximo 20 artículos (el sistema debe capar). `?limit=100` → máximo 20 artículos. El campo `articlesCount` debe reflejar el total real (25+), no el número retornado. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [ ] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [x] Manual (Swagger UI)  [ ] Automatizado |
| **Técnica aplicada** | [x] BVA (límite máximo del parámetro `limit`) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Anotar la cantidad exacta retornada en cada variante. Si `limit=100` retorna más de 20 artículos, se confirma el defecto de validación de límite. |

---

### CP-EXP-M-005

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-EXP-M-005 |
| **Nombre** | Crear artículos con títulos similares y observar colisión de slugs |
| **Funcionalidad / Endpoint cubierto** | `POST /api/articles` — generación y unicidad de slug |
| **Precondiciones** | Usuario autenticado. Base de datos limpia (sin artículos previos). |
| **Datos de entrada** | **Artículo 1:** `"title": "Mi Blog"`<br>**Artículo 2:** `"title": "mi blog"` (mismas palabras en minúsculas)<br>**Artículo 3:** `"title": "Mi Blog!"` (con puntuación)<br>**Artículo 4:** `"title": "Mi  Blog"` (doble espacio)<br>Todos con `"description": "Desc"`, `"body": "Body"` |
| **Pasos de ejecución** | 1. Autenticarse en Swagger UI<br>2. Crear Artículo 1 (`"Mi Blog"`) → anotar el slug retornado<br>3. Intentar crear Artículo 2 (`"mi blog"`) → anotar código y respuesta (¿genera el mismo slug?)<br>4. Crear Artículo 3 (`"Mi Blog!"`) → anotar slug<br>5. Crear Artículo 4 (`"Mi  Blog"`) → anotar slug<br>6. Verificar si los slugs de los artículos 1, 3 y 4 son iguales o distintos |
| **Resultado esperado** | "Mi Blog" genera slug `mi-blog`. "mi blog" intenta generar `mi-blog` también → la API debe retornar HTTP 400 (slug duplicado). "Mi Blog!" y "Mi  Blog" pueden generar variantes como `mi-blog-1` o error, dependiendo de la implementación de slugify. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [ ] Media  [x] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [ ] Integración  [ ] Seguridad  [x] Exploratoria |
| **Modo** | [x] Manual (Swagger UI)  [ ] Automatizado |
| **Técnica aplicada** | [x] Exploratoria |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Documentar el slug generado para cada variante. El objetivo es explorar el comportamiento de la función `slugify` con entradas en el borde. |

---

### CP-TOOL-M-001

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-TOOL-M-001 |
| **Nombre** | Verificar que Swagger UI documenta correctamente los 19 endpoints de la API |
| **Funcionalidad / Endpoint cubierto** | `GET http://localhost:8000/docs` — documentación automática de FastAPI |
| **Precondiciones** | API corriendo en `http://localhost:8000`. Navegador web disponible. |
| **Datos de entrada** | Lista de los 19 endpoints esperados (ver §1.3 del Plan de Pruebas). |
| **Pasos de ejecución** | 1. Abrir `http://localhost:8000/docs` en el navegador<br>2. Verificar que las secciones aparecen (users, articles, profiles, comments, tags)<br>3. Contar los endpoints listados y comparar con los 19 esperados<br>4. Para cada endpoint, expandirlo y verificar: descripción en texto, parámetros documentados (query, path, body), schema del request body y schema de la respuesta<br>5. Registrar cualquier endpoint sin descripción, con schema faltante o con información incorrecta |
| **Resultado esperado** | Los 19 endpoints están presentes. Cada uno tiene: descripción legible, parámetros documentados y schema de request/response visible. No hay endpoints huérfanos ni secciones vacías. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [ ] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [x] Manual (Swagger UI)  [ ] Automatizado |
| **Técnica aplicada** | [x] Exploratoria (revisión de completitud) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Adjuntar screenshot de la vista general de Swagger UI con todos los endpoints visibles. |

---

### CP-TOOL-M-002

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-TOOL-M-002 |
| **Nombre** | Ejecutar flujo autenticado completo usando el botón Authorize de Swagger UI |
| **Funcionalidad / Endpoint cubierto** | Swagger UI — sistema de autenticación Bearer. Endpoints: `GET /api/user`, `POST /api/articles`, `DELETE /api/articles/{slug}` |
| **Precondiciones** | API corriendo. Usuario registrado previamente (o se registra en el paso 1). |
| **Datos de entrada** | **Login:** `{"user": {"email": "test@test.com", "password": "password123"}}`<br>**Artículo:** `{"article": {"title": "Artículo Swagger Test", "description": "Desc", "body": "Body"}}` |
| **Pasos de ejecución** | 1. Registrar un usuario con `POST /api/users` si no existe<br>2. Hacer login con `POST /api/users/login`, copiar el valor de `token` del response<br>3. Clicar el botón verde "Authorize" (esquina superior derecha de Swagger UI)<br>4. En el campo `Value`, ingresar `Bearer {el token copiado}` y clicar Authorize<br>5. Ejecutar `GET /api/user` → verificar que retorna los datos del usuario (HTTP 200)<br>6. Ejecutar `POST /api/articles` con el body indicado → anotar el slug del artículo creado<br>7. Ejecutar `DELETE /api/articles/{slug}` con el slug obtenido → verificar HTTP 200 |
| **Resultado esperado** | Los tres endpoints retornan HTTP 200 con datos válidos. La autenticación Bearer persiste entre los requests sin necesidad de volver a ingresarla. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [ ] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [x] Manual (Swagger UI)  [ ] Automatizado |
| **Técnica aplicada** | [x] EP (flujo con credenciales válidas) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Adjuntar screenshot del modal de Authorize y de cada respuesta exitosa. |

---

### CP-TOOL-M-003

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-TOOL-M-003 |
| **Nombre** | Importar y ejecutar la colección `postman.json` del repositorio en Postman |
| **Funcionalidad / Endpoint cubierto** | Colección Postman pre-existente en la raíz del repositorio (`postman.json`) |
| **Precondiciones** | Postman instalado. API corriendo en `http://localhost:8000`. Archivo `postman.json` disponible en la raíz del repositorio. |
| **Datos de entrada** | Archivo: `postman.json` (raíz del repositorio)<br>Variable de entorno: `base_url = http://localhost:8000` |
| **Pasos de ejecución** | 1. Abrir Postman → File → Import → seleccionar `postman.json` del repositorio<br>2. Configurar la variable de entorno `base_url` con valor `http://localhost:8000`<br>3. Ejecutar los requests de la colección en orden<br>4. Para cada request, anotar el código HTTP retornado<br>5. Identificar qué requests pasan (código esperado) y cuáles fallan<br>6. Documentar los resultados en una tabla |
| **Resultado esperado** | Los requests de flujos básicos (registro, login, listar artículos, listar tags) retornan los códigos esperados. La colección sirve como guía de uso funcional de la API. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [ ] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [x] Manual (Postman)  [ ] Automatizado |
| **Técnica aplicada** | [x] EP (flujos definidos en la colección) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Adjuntar screenshot del collection runner con el resumen de resultados. |

---

### CP-QUAL-M-001

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-QUAL-M-001 |
| **Nombre** | Evaluar la calidad y claridad de los mensajes de error ante datos inválidos |
| **Funcionalidad / Endpoint cubierto** | Múltiples endpoints: `POST /api/users/login`, `POST /api/articles`, `GET /api/articles/{slug}`, `POST /api/profiles/{username}/follow` |
| **Precondiciones** | API corriendo. Un usuario registrado disponible. |
| **Datos de entrada** | **Escenario 1:** `POST /api/users/login` con `{"user": {"email": "noexiste@test.com", "password": "pass"}}`<br>**Escenario 2:** `POST /api/articles` con `{"article": {"title": "", "description": "Desc", "body": "Body"}}` (autenticado)<br>**Escenario 3:** `GET /api/articles/slug-que-definitivamente-no-existe`<br>**Escenario 4:** `POST /api/profiles/usuario-que-no-existe/follow` (autenticado) |
| **Pasos de ejecución** | 1. Ejecutar cada escenario en Swagger UI o Postman<br>2. Para cada respuesta de error, anotar: código HTTP, campo `detail` del body<br>3. Evaluar cualitativamente: ¿El mensaje identifica qué falló? ¿Es útil para un desarrollador que consume la API? ¿Expone información sensible innecesaria? |
| **Resultado esperado** | Cada error retorna un código HTTP apropiado (400, 404, 422) con un mensaje `detail` descriptivo y útil. Ningún mensaje expone rutas internas, SQL ni información de infraestructura. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [ ] Integración  [ ] Seguridad  [x] Exploratoria |
| **Modo** | [x] Manual (Swagger UI / Postman)  [ ] Automatizado |
| **Técnica aplicada** | [x] EP (particiones inválidas) [x] Exploratoria |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Este caso requiere juicio humano para evaluar la calidad del mensaje, no solo el código HTTP. Documentar los mensajes exactos recibidos. |

---

### CP-QUAL-M-002

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-QUAL-M-002 |
| **Nombre** | Verificar la estructura completa del JSON de respuesta contra la especificación RealWorld |
| **Funcionalidad / Endpoint cubierto** | `GET /api/user`, `GET /api/articles/{slug}`, `GET /api/articles/{slug}/comments`, `GET /api/profiles/{username}` |
| **Precondiciones** | Usuario autenticado, artículo con comentario creados. Spec de RealWorld disponible en: `https://realworld-docs.netlify.app/docs/specs/backend-specs/api-response-format` |
| **Datos de entrada** | Spec RealWorld para cada respuesta. Endpoints a verificar: los cuatro indicados. |
| **Pasos de ejecución** | 1. Ejecutar `GET /api/user` → comparar campo a campo con spec: `{user: {email, token, username, bio, image}}`<br>2. Ejecutar `GET /api/articles/{slug}` → comparar con spec: `{article: {slug, title, description, body, tagList, createdAt, updatedAt, favorited, favoritesCount, author: {username, bio, image, following}}}`<br>3. Ejecutar `GET /api/articles/{slug}/comments` → comparar con spec: `{comments: [{id, createdAt, updatedAt, body, author}]}`<br>4. Ejecutar `GET /api/profiles/{username}` → comparar con spec: `{profile: {username, bio, image, following}}`<br>5. Registrar cualquier campo faltante, extra, con nombre incorrecto o tipo de dato diferente |
| **Resultado esperado** | Todos los campos definidos en la especificación RealWorld están presentes en las respuestas, con los nombres exactos y tipos de dato correctos (string, boolean, number, array). |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [ ] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [x] Manual (Swagger UI / Postman)  [ ] Automatizado |
| **Técnica aplicada** | [x] EP (verificación de partición válida completa) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Adjuntar screenshot de cada respuesta comparada contra la spec. Documentar cualquier discrepancia encontrada. |

---

### CP-QUAL-M-003

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-QUAL-M-003 |
| **Nombre** | Editar artículo ajeno autenticado como no-autor y verificar que el sistema lo rechaza |
| **Funcionalidad / Endpoint cubierto** | `PUT /api/articles/{slug}` — control de acceso por autoría |
| **Precondiciones** | Usuario A registrado y con un artículo publicado (slug conocido). Usuario B registrado y autenticado en Swagger UI. |
| **Datos de entrada** | **Endpoint:** `PUT /api/articles/{slug del artículo de A}`<br>**Auth:** Token JWT de usuario B<br>**Body:** `{"article": {"title": "Modificado por intruso", "body": "Contenido alterado"}}` |
| **Pasos de ejecución** | 1. Registrar Usuario A, crear artículo, anotar el slug<br>2. Registrar Usuario B, hacer login, copiar token<br>3. En Swagger UI, autenticarse como Usuario B<br>4. Ejecutar `PUT /api/articles/{slug de A}` con el body indicado<br>5. Tomar screenshot de la respuesta completa<br>6. Verificar con `GET /api/articles/{slug}` que el título no fue modificado |
| **Resultado esperado** | HTTP 400 Bad Request con `detail: "You are not the author of this article"`. El GET posterior confirma que el artículo no fue modificado. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [ ] Integración  [x] Seguridad  [ ] Exploratoria |
| **Modo** | [x] Manual (Swagger UI)  [ ] Automatizado |
| **Técnica aplicada** | [x] Tabla de decisión (autenticado × no-autor) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Screenshot obligatorio: evidencia para el reporte de MantisBT si el sistema permite la edición indebida. |

---

### CP-QUAL-M-004

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-QUAL-M-004 |
| **Nombre** | Eliminar artículo ajeno autenticado como no-autor y verificar que el sistema lo rechaza |
| **Funcionalidad / Endpoint cubierto** | `DELETE /api/articles/{slug}` — seguridad y control de acceso |
| **Precondiciones** | Usuario A con artículo publicado (slug conocido). Usuario B autenticado en Swagger UI. |
| **Datos de entrada** | **Endpoint:** `DELETE /api/articles/{slug del artículo de A}`<br>**Auth:** Token JWT de usuario B |
| **Pasos de ejecución** | 1. Registrar Usuario A, crear artículo, anotar el slug<br>2. Registrar Usuario B, autenticarse en Swagger como B<br>3. Ejecutar `DELETE /api/articles/{slug de A}`<br>4. Tomar screenshot de la respuesta<br>5. Ejecutar `GET /api/articles/{slug}` para confirmar que el artículo sigue existiendo |
| **Resultado esperado** | HTTP 400 Bad Request con `detail: "You are not the author of this article"`. El GET posterior retorna HTTP 200 (artículo intacto, no fue eliminado). |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [ ] Integración  [x] Seguridad  [ ] Exploratoria |
| **Modo** | [x] Manual (Swagger UI)  [ ] Automatizado |
| **Técnica aplicada** | [x] Tabla de decisión (autenticado × no-autor) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Este es el caso de mayor severidad del plan. Screenshot obligatorio del intento fallido Y del GET que confirma integridad del artículo. |

---

### CP-EST-M-001

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-EST-M-001 |
| **Nombre** | Flujo follow → unfollow: verificar transición del campo `following` false → true → false |
| **Funcionalidad / Endpoint cubierto** | `POST /api/profiles/{username}/follow`, `DELETE /api/profiles/{username}/follow`, `GET /api/profiles/{username}` |
| **Precondiciones** | Usuario A y Usuario B registrados. Autenticado como Usuario A. Usuario A no sigue a Usuario B (estado inicial). |
| **Datos de entrada** | **Username objetivo:** nombre de Usuario B |
| **Pasos de ejecución** | 1. `GET /api/profiles/{username de B}` → verificar `following: false` (estado inicial)<br>2. `POST /api/profiles/{username de B}/follow` → verificar `following: true` en la respuesta<br>3. `GET /api/profiles/{username de B}` → confirmar que `following: true` persiste en un GET posterior<br>4. `DELETE /api/profiles/{username de B}/follow` → verificar `following: false` en la respuesta<br>5. `GET /api/profiles/{username de B}` → confirmar que `following: false` persiste |
| **Resultado esperado** | El campo `following` cambia correctamente en cada transición y el estado persiste entre requests. Pasos 1→2: false→true. Pasos 4→5: true→false. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [x] Manual (Swagger UI)  [ ] Automatizado |
| **Técnica aplicada** | [x] Transición de estados (following: false → true → false) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Tomar screenshot en cada paso. El valor de `following` debe ser `true` en el paso 2 y 3, y `false` en el paso 1, 4 y 5. |

---

### CP-EST-M-002

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-EST-M-002 |
| **Nombre** | Flujo favoritos: marcar → verificar contador → desmarcar → verificar contador |
| **Funcionalidad / Endpoint cubierto** | `POST /api/articles/{slug}/favorite`, `DELETE /api/articles/{slug}/favorite`, `GET /api/articles/{slug}` |
| **Precondiciones** | Artículo existente (puede ser de cualquier usuario). Usuario A autenticado. El artículo tiene `favoritesCount: 0` y `favorited: false` para Usuario A. |
| **Datos de entrada** | **Slug:** slug del artículo de prueba |
| **Pasos de ejecución** | 1. `GET /api/articles/{slug}` → verificar `favorited: false`, `favoritesCount: 0`<br>2. `POST /api/articles/{slug}/favorite` → verificar `favorited: true`, `favoritesCount: 1`<br>3. `GET /api/articles/{slug}` → confirmar `favorited: true`, `favoritesCount: 1` persiste<br>4. `DELETE /api/articles/{slug}/favorite` → verificar `favorited: false`, `favoritesCount: 0`<br>5. `GET /api/articles/{slug}` → confirmar `favorited: false`, `favoritesCount: 0` persiste |
| **Resultado esperado** | `favorited` y `favoritesCount` cambian correctamente en cada transición. Los valores persisten entre requests independientes. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [x] Manual (Swagger UI)  [ ] Automatizado |
| **Técnica aplicada** | [x] Transición de estados (favorited: false → true → false) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Anotar los valores exactos de `favorited` y `favoritesCount` en cada paso. Si el contador no cambia o `favorited` no cambia, reportar defecto. |

---

### CP-EST-M-003

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-EST-M-003 |
| **Nombre** | Eliminar artículo propio y verificar que un GET posterior retorna 404 |
| **Funcionalidad / Endpoint cubierto** | `DELETE /api/articles/{slug}` → `GET /api/articles/{slug}` |
| **Precondiciones** | Usuario autenticado con artículo propio creado. Slug del artículo conocido. |
| **Datos de entrada** | **Slug:** slug del artículo propio |
| **Pasos de ejecución** | 1. `GET /api/articles/{slug}` → verificar HTTP 200 (artículo existe)<br>2. `DELETE /api/articles/{slug}` → verificar HTTP 200<br>3. `GET /api/articles/{slug}` → verificar HTTP 404 |
| **Resultado esperado** | Paso 1: HTTP 200. Paso 2: HTTP 200 (eliminación exitosa). Paso 3: HTTP 404 Not Found con `detail: "No article found"`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Regresión  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [x] Manual (Swagger UI)  [ ] Automatizado |
| **Técnica aplicada** | [x] Transición de estados (recurso: existe → eliminado → no encontrado) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Tomar screenshot del paso 3 mostrando el 404. |

---

## PRUEBAS AUTOMATIZADAS

---

### CP-AUTH-A-001

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-AUTH-A-001 |
| **Nombre** | Registro exitoso de nuevo usuario retorna HTTP 201 Created |
| **Funcionalidad / Endpoint cubierto** | `POST /api/users` |
| **Precondiciones** | Base de datos de pruebas limpia. Sin usuarios previos con el email de prueba. |
| **Datos de entrada** | **Método:** POST<br>**Endpoint:** `/api/users`<br>**Headers:** `Content-Type: application/json`<br>**Body:** `{"user": {"username": "John Doe", "email": "john.doe@example.com", "password": "password"}}` |
| **Pasos de ejecución** | 1. Limpiar la BD de pruebas (fixture de pytest)<br>2. Enviar POST /api/users con el body indicado<br>3. Verificar el código de estado HTTP de la respuesta |
| **Resultado esperado** | HTTP **201** Created. Body: `{"user": {"username": "John Doe", "email": "john.doe@example.com", "token": "<jwt>", "bio": null, "image": null}}` |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] EP (partición válida: datos de registro correctos) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Si retorna 200 en lugar de 201, se confirma el defecto de status code. El assert debe ser `assert response.status_code == 201`. |

---

### CP-AUTH-A-002

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-AUTH-A-002 |
| **Nombre** | Registro exitoso retorna token JWT no vacío en el body de respuesta |
| **Funcionalidad / Endpoint cubierto** | `POST /api/users` |
| **Precondiciones** | BD de pruebas limpia. |
| **Datos de entrada** | **Método:** POST<br>**Endpoint:** `/api/users`<br>**Body:** `{"user": {"username": "John Doe", "email": "john.doe@example.com", "password": "password"}}` |
| **Pasos de ejecución** | 1. Enviar POST /api/users con datos válidos<br>2. Verificar que `response.json()["user"]["token"]` existe y no es vacío<br>3. Verificar que el token tiene formato JWT: 3 partes separadas por `.` |
| **Resultado esperado** | HTTP 200/201. `body.user.token` es un string no vacío con formato `xxxxx.yyyyy.zzzzz`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] EP (partición válida) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | `assert len(token.split(".")) == 3` valida el formato JWT básico. |

---

### CP-AUTH-A-003

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-AUTH-A-003 |
| **Nombre** | Login con credenciales válidas retorna HTTP 200 y token JWT |
| **Funcionalidad / Endpoint cubierto** | `POST /api/users/login` |
| **Precondiciones** | Usuario existente con email `john.doe@example.com` y password hasheada en BD. |
| **Datos de entrada** | **Método:** POST<br>**Endpoint:** `/api/users/login`<br>**Body:** `{"user": {"email": "john.doe@example.com", "password": "password"}}` |
| **Pasos de ejecución** | 1. Crear usuario con password hasheada en la BD de pruebas<br>2. Enviar POST /api/users/login<br>3. Verificar status 200<br>4. Verificar que `body.user.token` es un JWT válido y el `sub` del payload corresponde al ID del usuario |
| **Resultado esperado** | HTTP 200. `body.user.email` = `john.doe@example.com`. `body.user.token` es JWT válido cuyo payload contiene el ID del usuario. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] EP (partición válida) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Usar `decode_access_token` del módulo `app.core.security` para verificar el payload del JWT. |

---

### CP-AUTH-A-004

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-AUTH-A-004 |
| **Nombre** | Login con email no registrado retorna HTTP 400 Bad Request |
| **Funcionalidad / Endpoint cubierto** | `POST /api/users/login` |
| **Precondiciones** | Usuario John existe en BD. Se intenta login con email de un usuario inexistente. |
| **Datos de entrada** | **Método:** POST<br>**Endpoint:** `/api/users/login`<br>**Body:** `{"user": {"email": "noexiste@example.com", "password": "password"}}` |
| **Pasos de ejecución** | 1. Crear usuario John en BD<br>2. Enviar POST /api/users/login con email inexistente<br>3. Verificar status 400 |
| **Resultado esperado** | HTTP 400 Bad Request. `body.detail` = `"Bad credentials"`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] EP (partición inválida: email no registrado) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | — |

---

### CP-AUTH-A-005

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-AUTH-A-005 |
| **Nombre** | Registro con email ya existente retorna HTTP 400 Bad Request |
| **Funcionalidad / Endpoint cubierto** | `POST /api/users` |
| **Precondiciones** | Usuario con `email: john.doe@example.com` ya existe en BD. |
| **Datos de entrada** | **Método:** POST<br>**Endpoint:** `/api/users`<br>**Body:** `{"user": {"username": "Otro Nombre", "email": "john.doe@example.com", "password": "password"}}` |
| **Pasos de ejecución** | 1. Crear usuario John en BD<br>2. Intentar registrar otro usuario con el mismo email<br>3. Verificar status 400 |
| **Resultado esperado** | HTTP 400 Bad Request. `body.detail` = `"Email already registered"`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] EP (partición inválida: email duplicado) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | — |

---

### CP-ART-A-001

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-ART-A-001 |
| **Nombre** | Crear artículo con datos válidos retorna HTTP 200 con estructura de respuesta correcta |
| **Funcionalidad / Endpoint cubierto** | `POST /api/articles` |
| **Precondiciones** | Usuario John autenticado. Tag "existing-tag" pre-existente en BD. |
| **Datos de entrada** | **Método:** POST<br>**Endpoint:** `/api/articles`<br>**Headers:** `Authorization: Bearer {token de John}`<br>**Body:** `{"article": {"title": "Test Title", "description": "Test Description", "body": "Test Body", "tagList": ["tag1", "tag2"]}}` |
| **Pasos de ejecución** | 1. Autenticar como John<br>2. Enviar POST /api/articles con el body indicado<br>3. Verificar status 200<br>4. Verificar que `body.article` contiene: `slug = "test-title"`, `title = "Test Title"`, `tagList` incluye "tag1" y "tag2" ordenados, `favorited = false`, `favoritesCount = 0`, `author.username = "John Doe"` |
| **Resultado esperado** | HTTP 200. `body.article.slug` = `"test-title"`. `body.article.tagList` = `["tag1", "tag2"]`. `body.article.favorited` = `false`. `body.article.author.username` = `"John Doe"`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] EP (partición válida: todos los campos correctos) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Verificar que los tags se retornan ordenados alfabéticamente. |

---

### CP-ART-A-002

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-ART-A-002 |
| **Nombre** | Crear artículo con título vacío retorna HTTP 422 Unprocessable Entity |
| **Funcionalidad / Endpoint cubierto** | `POST /api/articles` — validación del campo `title` |
| **Precondiciones** | Usuario autenticado. |
| **Datos de entrada** | **Método:** POST<br>**Endpoint:** `/api/articles`<br>**Headers:** `Authorization: Bearer {token}`<br>**Body:** `{"article": {"title": "", "description": "Test Description", "body": "Test Body"}}` |
| **Pasos de ejecución** | 1. Autenticar como John<br>2. Enviar POST /api/articles con `title: ""`<br>3. Verificar status 422 |
| **Resultado esperado** | HTTP 422 Unprocessable Entity. El body indica que el campo `title` no cumple la validación mínima. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] BVA (valor en el límite inferior: string vacío = longitud 0, por debajo del mínimo de 1) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Si retorna 200 y crea el artículo, se confirma el defecto de validación de campo `title`. |

---

### CP-ART-A-003

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-ART-A-003 |
| **Nombre** | Crear artículo sin token de autenticación retorna HTTP 401 Unauthorized |
| **Funcionalidad / Endpoint cubierto** | `POST /api/articles` — autenticación requerida |
| **Precondiciones** | Sin token en los headers. |
| **Datos de entrada** | **Método:** POST<br>**Endpoint:** `/api/articles`<br>**Headers:** _(sin Authorization)_<br>**Body:** `{"article": {"title": "Test", "description": "Test", "body": "Test"}}` |
| **Pasos de ejecución** | 1. Enviar POST /api/articles sin header Authorization<br>2. Verificar status 401 |
| **Resultado esperado** | HTTP 401 Unauthorized. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Integración  [x] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] Tabla de decisión (no autenticado × endpoint protegido) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | — |

---

### CP-ART-A-004

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-ART-A-004 |
| **Nombre** | Editar artículo como autor legítimo retorna HTTP 200 con artículo actualizado |
| **Funcionalidad / Endpoint cubierto** | `PUT /api/articles/{slug}` |
| **Precondiciones** | John autenticado. Artículo de John con slug `test-title` en BD. |
| **Datos de entrada** | **Método:** PUT<br>**Endpoint:** `/api/articles/test-title`<br>**Headers:** `Authorization: Bearer {token de John}`<br>**Body:** `{"article": {"title": "New Title"}}` |
| **Pasos de ejecución** | 1. Crear artículo de John en BD<br>2. Autenticar como John<br>3. Enviar PUT /api/articles/test-title con nuevo título<br>4. Verificar status 200<br>5. Verificar que `body.article.title` = `"New Title"` |
| **Resultado esperado** | HTTP 200. `body.article.title` = `"New Title"`. El artículo fue actualizado correctamente. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] Tabla de decisión (autenticado × autor) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | — |

---

### CP-ART-A-005

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-ART-A-005 |
| **Nombre** | Editar artículo de otro usuario retorna HTTP 400 Bad Request |
| **Funcionalidad / Endpoint cubierto** | `PUT /api/articles/{slug}` — control de acceso por autoría |
| **Precondiciones** | Artículo de Jane (`slug = "test-title"`) en BD. John autenticado. |
| **Datos de entrada** | **Método:** PUT<br>**Endpoint:** `/api/articles/test-title`<br>**Headers:** `Authorization: Bearer {token de John}`<br>**Body:** `{"article": {"title": "Modificado"}}` |
| **Pasos de ejecución** | 1. Crear usuario Jane y artículo de Jane en BD<br>2. Autenticar como John<br>3. Enviar PUT /api/articles/test-title (artículo de Jane) con token de John<br>4. Verificar status 400 |
| **Resultado esperado** | HTTP 400 Bad Request. `body.detail` = `"You are not the author of this article"`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [x] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] Tabla de decisión (autenticado × no-autor) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Si retorna 200, se confirma el defecto de autorización en edición. |

---

### CP-ART-A-006

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-ART-A-006 |
| **Nombre** | Eliminar artículo de otro usuario retorna HTTP 400 Bad Request |
| **Funcionalidad / Endpoint cubierto** | `DELETE /api/articles/{slug}` — seguridad crítica |
| **Precondiciones** | Artículo de Jane (`slug = "test-title"`) en BD. John autenticado. |
| **Datos de entrada** | **Método:** DELETE<br>**Endpoint:** `/api/articles/test-title`<br>**Headers:** `Authorization: Bearer {token de John}` |
| **Pasos de ejecución** | 1. Crear usuario Jane y su artículo en BD<br>2. Autenticar como John<br>3. Enviar DELETE /api/articles/test-title con token de John<br>4. Verificar status 400 |
| **Resultado esperado** | HTTP 400 Bad Request. `body.detail` = `"You are not the author of this article"`. El artículo de Jane permanece intacto en BD. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [x] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] Tabla de decisión (autenticado × no-autor) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | El caso de mayor severidad del plan. Si retorna 200, se confirma una brecha de seguridad crítica. Verificar adicionalmente que el artículo sigue en BD con un GET posterior. |

---

### CP-ART-A-007

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-ART-A-007 |
| **Nombre** | Acceder a `GET /api/articles/feed` sin autenticación retorna HTTP 401 |
| **Funcionalidad / Endpoint cubierto** | `GET /api/articles/feed` — endpoint que requiere autenticación obligatoria |
| **Precondiciones** | Sin token en headers. |
| **Datos de entrada** | **Método:** GET<br>**Endpoint:** `/api/articles/feed`<br>**Headers:** _(sin Authorization)_ |
| **Pasos de ejecución** | 1. Enviar GET /api/articles/feed sin header Authorization<br>2. Verificar status 401 |
| **Resultado esperado** | HTTP 401 Unauthorized. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [x] Alta  [ ] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Integración  [x] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] Tabla de decisión (no autenticado × endpoint protegido) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Si retorna 200 con lista vacía en lugar de 401, se confirma el defecto de autenticación del feed. |

---

### CP-ART-A-008

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-ART-A-008 |
| **Nombre** | Filtrar artículos por tag retorna únicamente artículos etiquetados con ese tag |
| **Funcionalidad / Endpoint cubierto** | `GET /api/articles?tag={tag}` |
| **Precondiciones** | BD con: 2 artículos con tag `"python"` y 1 artículo con tag `"java"` (sin tag python). |
| **Datos de entrada** | **Método:** GET<br>**Endpoint:** `/api/articles?tag=python`<br>**Headers:** _(sin auth — es opcional)_ |
| **Pasos de ejecución** | 1. Crear en BD: artículo A con tag "python", artículo B con tag "python", artículo C con tag "java"<br>2. Enviar GET /api/articles?tag=python<br>3. Verificar status 200<br>4. Verificar que `body.articlesCount` = 2<br>5. Verificar que todos los artículos en `body.articles` tienen "python" en su `tagList`<br>6. Verificar que el artículo C (tag "java") NO aparece en la respuesta |
| **Resultado esperado** | HTTP 200. `articlesCount` = 2. Todos los artículos retornados tienen `"python"` en `tagList`. El artículo con solo tag `"java"` no aparece. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] EP (partición: con filtro activo vs. sin filtro) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Si `articlesCount` = 3 (todos), el filtro de tag está siendo ignorado — se confirma defecto de lógica. |

---

### CP-ART-A-009

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-ART-A-009 |
| **Nombre** | Solicitar `?limit=100` retorna máximo 20 artículos (límite máximo del sistema) |
| **Funcionalidad / Endpoint cubierto** | `GET /api/articles?limit={n}` — validación del parámetro `limit` |
| **Precondiciones** | BD con al menos 25 artículos creados. |
| **Datos de entrada** | **Método:** GET<br>**Endpoint:** `/api/articles?limit=100` |
| **Pasos de ejecución** | 1. Crear 25 artículos en BD de pruebas<br>2. Enviar GET /api/articles?limit=100<br>3. Verificar status 200<br>4. Verificar que `len(body.articles)` <= 20<br>5. Verificar que `body.articlesCount` refleja el total real (25), no los retornados |
| **Resultado esperado** | HTTP 200. `len(articles)` = 20 (no 100). `articlesCount` = 25. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] BVA (valor muy por encima del límite: 100 >> 20) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Si `len(articles)` > 20, se confirma que el `min(limit, max_limit)` fue removido y el defecto de validación de límite está activo. |

---

### CP-COM-A-001

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-COM-A-001 |
| **Nombre** | Crear comentario en artículo existente retorna HTTP 200 con el comentario creado |
| **Funcionalidad / Endpoint cubierto** | `POST /api/articles/{slug}/comments` |
| **Precondiciones** | Artículo de John con slug `test-title` en BD. John autenticado. |
| **Datos de entrada** | **Método:** POST<br>**Endpoint:** `/api/articles/test-title/comments`<br>**Headers:** `Authorization: Bearer {token de John}`<br>**Body:** `{"comment": {"body": "Este es un comentario de prueba"}}` |
| **Pasos de ejecución** | 1. Crear artículo de John en BD<br>2. Autenticar como John<br>3. Enviar POST /api/articles/test-title/comments<br>4. Verificar status 200<br>5. Verificar que `body.comment.body` = `"Este es un comentario de prueba"` y `body.comment.author.username` = `"John Doe"` |
| **Resultado esperado** | HTTP 200. `body.comment.body` = el texto enviado. `body.comment.author.username` = nombre de John. El campo `id` existe y es un entero. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] EP (partición válida) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | — |

---

### CP-COM-A-002

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-COM-A-002 |
| **Nombre** | Crear comentario sin autenticación retorna HTTP 401 Unauthorized |
| **Funcionalidad / Endpoint cubierto** | `POST /api/articles/{slug}/comments` |
| **Precondiciones** | Artículo existente. Sin token. |
| **Datos de entrada** | **Método:** POST<br>**Endpoint:** `/api/articles/test-title/comments`<br>**Headers:** _(sin Authorization)_<br>**Body:** `{"comment": {"body": "Comentario"}}` |
| **Pasos de ejecución** | 1. Crear artículo en BD<br>2. Enviar POST sin Authorization<br>3. Verificar status 401 |
| **Resultado esperado** | HTTP 401 Unauthorized. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Integración  [x] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] Tabla de decisión (no autenticado × endpoint protegido) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | — |

---

### CP-COM-A-003

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-COM-A-003 |
| **Nombre** | Eliminar comentario propio retorna HTTP 200 y el comentario deja de existir |
| **Funcionalidad / Endpoint cubierto** | `DELETE /api/articles/{slug}/comments/{id}` |
| **Precondiciones** | John autenticado. Artículo de John con un comentario de John en BD. ID del comentario conocido. |
| **Datos de entrada** | **Método:** DELETE<br>**Endpoint:** `/api/articles/test-title/comments/{id del comentario}`<br>**Headers:** `Authorization: Bearer {token de John}` |
| **Pasos de ejecución** | 1. Crear artículo y comentario de John en BD<br>2. Autenticar como John<br>3. Enviar DELETE /api/articles/test-title/comments/{id}<br>4. Verificar status 200<br>5. Verificar con GET /api/articles/test-title/comments que el comentario ya no aparece |
| **Resultado esperado** | HTTP 200. El comentario eliminado ya no aparece en el listado de comentarios del artículo. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] Tabla de decisión (autenticado × autor del comentario) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | — |

---

### CP-COM-A-004

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-COM-A-004 |
| **Nombre** | Obtener comentarios de un artículo inexistente retorna HTTP 404 Not Found |
| **Funcionalidad / Endpoint cubierto** | `GET /api/articles/{slug}/comments` |
| **Precondiciones** | BD sin artículo con slug `slug-que-no-existe`. |
| **Datos de entrada** | **Método:** GET<br>**Endpoint:** `/api/articles/slug-que-no-existe/comments` |
| **Pasos de ejecución** | 1. Enviar GET /api/articles/slug-que-no-existe/comments con BD sin ese artículo<br>2. Verificar status 404 |
| **Resultado esperado** | HTTP 404 Not Found. `body.detail` = `"No article found"`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] EP (partición inválida: recurso inexistente) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | — |

---

### CP-PRF-A-001

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-PRF-A-001 |
| **Nombre** | Seguir a un usuario cambia el campo `following` a `true` en la respuesta |
| **Funcionalidad / Endpoint cubierto** | `POST /api/profiles/{username}/follow` |
| **Precondiciones** | John y Jane en BD. Jane autenticada. John no sigue a Jane (estado inicial: `following: false`). |
| **Datos de entrada** | **Método:** POST<br>**Endpoint:** `/api/profiles/John Doe/follow`<br>**Headers:** `Authorization: Bearer {token de Jane}` |
| **Pasos de ejecución** | 1. Crear usuarios John y Jane en BD<br>2. Autenticar como Jane<br>3. Enviar POST /api/profiles/John Doe/follow<br>4. Verificar status 200<br>5. Verificar que `body.profile.following` = `true` y `body.profile.username` = `"John Doe"` |
| **Resultado esperado** | HTTP 200. `body.profile` = `{"username": "John Doe", "bio": "John Bio", "image": "...", "following": true}`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] Transición de estados (following: false → true) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Si `following` retorna `false` después de hacer follow, se confirma el defecto de lógica en perfiles. |

---

### CP-PRF-A-002

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-PRF-A-002 |
| **Nombre** | Dejar de seguir a un usuario cambia `following` a `false` |
| **Funcionalidad / Endpoint cubierto** | `DELETE /api/profiles/{username}/follow` |
| **Precondiciones** | Jane sigue a John (relación en BD). Jane autenticada. |
| **Datos de entrada** | **Método:** DELETE<br>**Endpoint:** `/api/profiles/John Doe/follow`<br>**Headers:** `Authorization: Bearer {token de Jane}` |
| **Pasos de ejecución** | 1. Crear John y Jane en BD con Jane ya siguiendo a John<br>2. Autenticar como Jane<br>3. Enviar DELETE /api/profiles/John Doe/follow<br>4. Verificar status 200<br>5. Verificar que `body.profile.following` = `false` |
| **Resultado esperado** | HTTP 200. `body.profile.following` = `false`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] Transición de estados (following: true → false) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | — |

---

### CP-PRF-A-003

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-PRF-A-003 |
| **Nombre** | Obtener perfil de usuario inexistente retorna HTTP 404 Not Found |
| **Funcionalidad / Endpoint cubierto** | `GET /api/profiles/{username}` |
| **Precondiciones** | BD sin usuario con el nombre indicado. |
| **Datos de entrada** | **Método:** GET<br>**Endpoint:** `/api/profiles/UsuarioQueNoExiste` |
| **Pasos de ejecución** | 1. Enviar GET /api/profiles/UsuarioQueNoExiste con BD vacía<br>2. Verificar status 404 |
| **Resultado esperado** | HTTP 404 Not Found. `body.detail` = `"No user found"`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] EP (partición inválida: recurso inexistente) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | — |

---

### CP-PRF-A-004

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-PRF-A-004 |
| **Nombre** | Intentar seguir usuario sin autenticación retorna HTTP 401 Unauthorized |
| **Funcionalidad / Endpoint cubierto** | `POST /api/profiles/{username}/follow` |
| **Precondiciones** | Usuario John en BD. Sin token. |
| **Datos de entrada** | **Método:** POST<br>**Endpoint:** `/api/profiles/John Doe/follow`<br>**Headers:** _(sin Authorization)_ |
| **Pasos de ejecución** | 1. Crear usuario John en BD<br>2. Enviar POST /api/profiles/John Doe/follow sin Authorization<br>3. Verificar status 401 |
| **Resultado esperado** | HTTP 401 Unauthorized. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [ ] Integración  [x] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] Tabla de decisión (no autenticado × endpoint protegido) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | — |

---

### CP-FAV-A-001

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-FAV-A-001 |
| **Nombre** | Marcar artículo como favorito incrementa `favoritesCount` en 1 y `favorited` cambia a `true` |
| **Funcionalidad / Endpoint cubierto** | `POST /api/articles/{slug}/favorite` |
| **Precondiciones** | Artículo de Jane con `favoritesCount: 0`. John autenticado. |
| **Datos de entrada** | **Método:** POST<br>**Endpoint:** `/api/articles/test-title/favorite`<br>**Headers:** `Authorization: Bearer {token de John}` |
| **Pasos de ejecución** | 1. Crear artículo de Jane en BD<br>2. Autenticar como John<br>3. Enviar POST /api/articles/test-title/favorite<br>4. Verificar status 200<br>5. Verificar `body.article.favorited` = `true`<br>6. Verificar `body.article.favoritesCount` = `1` |
| **Resultado esperado** | HTTP 200. `favorited` = `true`. `favoritesCount` = `1`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] Transición de estados (favorited: false → true) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Si `favorited` = `false` o `favoritesCount` = `0` después del POST, se confirma el defecto de lógica invertida en favoritos. |

---

### CP-FAV-A-002

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-FAV-A-002 |
| **Nombre** | Desmarcar artículo favorito decrementa `favoritesCount` en 1 y `favorited` cambia a `false` |
| **Funcionalidad / Endpoint cubierto** | `DELETE /api/articles/{slug}/favorite` |
| **Precondiciones** | Artículo de Jane ya marcado como favorito por John (`favoritesCount: 1`, `favorited: true` para John). John autenticado. |
| **Datos de entrada** | **Método:** DELETE<br>**Endpoint:** `/api/articles/test-title/favorite`<br>**Headers:** `Authorization: Bearer {token de John}` |
| **Pasos de ejecución** | 1. Crear artículo de Jane con John en `favorited_by` (BD)<br>2. Autenticar como John<br>3. Enviar DELETE /api/articles/test-title/favorite<br>4. Verificar status 200<br>5. Verificar `body.article.favorited` = `false`<br>6. Verificar `body.article.favoritesCount` = `0` |
| **Resultado esperado** | HTTP 200. `favorited` = `false`. `favoritesCount` = `0`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [x] Media  [ ] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] Transición de estados (favorited: true → false) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | — |

---

### CP-TAG-A-001

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-TAG-A-001 |
| **Nombre** | `GET /api/tags` retorna HTTP 200 con lista de tags existentes ordenada alfabéticamente |
| **Funcionalidad / Endpoint cubierto** | `GET /api/tags` |
| **Precondiciones** | Tags "Tag 3", "Tag 2", "Tag 1" creados en BD (en ese orden). Sin autenticación requerida. |
| **Datos de entrada** | **Método:** GET<br>**Endpoint:** `/api/tags`<br>**Headers:** _(ninguno requerido)_ |
| **Pasos de ejecución** | 1. Insertar en BD: Tag "Tag 3", Tag "Tag 2", Tag "Tag 1"<br>2. Enviar GET /api/tags sin autenticación<br>3. Verificar status 200<br>4. Verificar que `body.tags` = `["Tag 1", "Tag 2", "Tag 3"]` (ordenado alfabéticamente) |
| **Resultado esperado** | HTTP 200. `body.tags` es un array con los 3 tags en orden alfabético ascendente: `["Tag 1", "Tag 2", "Tag 3"]`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [ ] Media  [x] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] EP (partición válida: tags existentes) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Verificar también que el endpoint no requiere autenticación (no retorna 401 sin token). |

---

### CP-TAG-A-002

| **Campo** | **Detalle** |
|---|---|
| **ID del caso** | CP-TAG-A-002 |
| **Nombre** | Tags asignados al crear un artículo aparecen en `GET /api/tags` |
| **Funcionalidad / Endpoint cubierto** | `POST /api/articles` → `GET /api/tags` (integración entre módulos) |
| **Precondiciones** | Usuario autenticado. BD sin tags previos. |
| **Datos de entrada** | **POST body:** `{"article": {"title": "Tagged Article", "description": "Desc", "body": "Body", "tagList": ["nuevo-tag", "otro-tag"]}}` |
| **Pasos de ejecución** | 1. Autenticar como John<br>2. Enviar POST /api/articles con `tagList: ["nuevo-tag", "otro-tag"]`<br>3. Verificar status 200 del POST<br>4. Enviar GET /api/tags sin autenticación<br>5. Verificar que `body.tags` incluye `"nuevo-tag"` y `"otro-tag"` |
| **Resultado esperado** | POST: HTTP 200 con artículo creado. GET: HTTP 200 con `body.tags` que contiene `"nuevo-tag"` y `"otro-tag"`. |
| **Resultado obtenido** | — |
| **Estado** | [x] No ejecutado  [ ] Pasó  [ ] Falló  [ ] Bloqueado |
| **Prioridad** | [ ] Alta  [ ] Media  [x] Baja |
| **Tipo de prueba** | [x] Funcional  [x] Integración  [ ] Seguridad  [ ] Exploratoria |
| **Modo** | [ ] Manual  [x] Automatizado (pytest) |
| **Técnica aplicada** | [x] EP (integración entre módulo de artículos y módulo de tags) |
| **Responsable** | [Tu nombre] |
| **Fecha de ejecución** | — |
| **Defectos asociados** | — |
| **Observaciones** | Este caso valida la integración entre dos módulos: que crear un artículo con tags actualiza correctamente el catálogo de tags. |

---

_Documento generado como parte del taller universitario de Pruebas de Software._
_41 casos de prueba: 15 manuales + 26 automatizados._
