# Análisis de Calidad del Software — Conduit API (FastAPI RealWorld)
## Informe Ejecutivo de QA y Evaluación de Madurez de Software
### Taller de Pruebas de Software — Universidad

---

## 1. Resumen Ejecutivo

El presente informe documenta los resultados del proceso formal de aseguramiento de calidad de software (QA) aplicado a la API REST **FastAPI RealWorld Example App (Conduit)**. Se ejecutó una estrategia mixta orientada por las directrices del **ISTQB (International Software Testing Qualifications Board)**, combinando **26 pruebas automatizadas de integración** con **pytest** y **15 pruebas manuales exploratorias y de caja negra** mediante **Swagger UI** y **Postman**, totalizando **41 casos de prueba**.

El ciclo de pruebas se ejecutó sobre la rama de evaluación uggy-version, la cual incorpora 9 defectos representativos de fallas reales de desarrollo (vulnerabilidades de control de acceso BOLA/IDOR, regresiones de integridad de datos, fallos de contrato HTTP y errores no controlados).

### Resultados Globales Clave:
- **Tasa de Ejecución:** **100%** (41 de 41 casos ejecutados).
- **Eficacia de Detección:** **100%** (9 de 9 defectos inyectados fueron cazados con éxito tanto por la suite automatizada como por las pruebas manuales).
- **Cobertura de Código en Backend:** **82.78%** de líneas ejecutadas (superando ampliamente la meta del 70%).
- **Cobertura Funcional de Endpoints:** **100%** (19 de 19 endpoints de la API evaluados).
- **Defectos Críticos:** 1 vulnerabilidad crítica de autorización (BUG-04: eliminación no autorizada de artículos ajenos).

---

## 2. Alineación con Principios y Metodología ISTQB

### 2.1 La Pirámide de Pruebas (Mike Cohn)
La estrategia implementada se fundamenta en la **Pirámide de Automatización de Pruebas de Mike Cohn**:
1. **Base sólida (Nivel de Integración / Componente - 63.4% del esfuerzo total):** 26 scripts automatizados con pytest que interactúan con una base de datos real PostgreSQL en Docker. Esto garantiza retroalimentación ultra-rápida (28.95 segundos para toda la suite), repetibilidad y bajo costo de mantenimiento.
2. **Capa Superior (Nivel Exploratorio / Manual de Sistema - 36.6% del esfuerzo total):** 15 pruebas manuales dirigidas a través de Swagger UI y Postman para evaluar flujos narrativos de usuario, límites de borde visuales, calidad heurística de mensajes de error, persistencia de autorización Bearer y casos de seguridad interactivos.

`
                  /                  /                   /     \       Manuales / Exploratorias (36.6% - 15 casos)
               /       \      Swagger UI, Postman, UX, Mensajes, Estados
              /---------             /                       /             \   Automatizadas de Integración (63.4% - 26 casos)
           /               \  pytest, Base de datos PostgreSQL en Docker,
          /                 \ pytest-cov (82.78% cobertura)
         /-------------------`

### 2.2 Técnicas de Diseño de Pruebas Aplicadas
Durante la concepción y ejecución de los casos se aplicaron las técnicas estándar de caja negra de ISTQB:
- **Partición de Equivalencia (EP):** Se aplicó en la verificación de tokens JWT (clases válidas vs. firmas manipuladas, tokens vacíos o strings arbitrarios en CP-EXP-M-003), y en formatos de email/contraseñas en CP-QUAL-M-001.
- **Análisis de Valores Límite (BVA):** Se aplicó en la paginación (limit=19, limit=20, limit=21, limit=100 en CP-EXP-M-004 y CP-ART-A-009), detectando la falla en el cap máximo de artículos.
- **Tablas de Decisión (Decision Tables):** Utilizadas para modelar las reglas de control de acceso por autoría (Usuario Autenticado × Es Autor del Recurso × Acción [GET, PUT, DELETE] en CP-QUAL-M-003, CP-QUAL-M-004, CP-ART-A-005 y CP-ART-A-006).
- **Transición de Estados (State Transition Testing):** Diseñada para validar el ciclo de vida de entidades:
  - Perfil: *No seguido* $
ightarrow$ *Seguido* $
ightarrow$ *No seguido* (CP-EST-M-001).
  - Artículo: *No favorito* $
ightarrow$ *Favorito* $
ightarrow$ *No favorito* (CP-EST-M-002).
  - Recurso: *Creado* $
ightarrow$ *Consultable (200)* $
ightarrow$ *Eliminado* $
ightarrow$ *No Encontrado (404)* (CP-EST-M-003).

### 2.3 Severidad vs. Prioridad en la Gestión de Defectos
Para el reporte formal en MantisBT se distinguió rigurosamente entre:
- **Severidad (Impacto técnico en el sistema):** Grado en que el fallo interrumpe la operación o seguridad del software (Crítica, Alta, Media, Baja).
- **Prioridad (Urgencia de negocio para su corrección):** Importancia temporal y de negocio asignada para resolver el ticket (Alta, Media, Baja).

Ejemplo clave:
- **BUG-04 (Eliminación de artículo ajeno):** **Severidad Crítica** (vulnera la integridad de la base de datos permitiendo borrado masivo de información ajena sin autorización) y **Prioridad Alta** (bloqueante para pase a producción).
- **BUG-01 (Código 200 en vez de 201 en registro):** **Severidad Baja** (la funcionalidad de registro se ejecuta correctamente y el usuario es persistido) y **Prioridad Baja** (es una desviación de estándar REST sin impacto operativo inmediato).

---

## 3. Análisis de Calidad por Módulos del Sistema

`
+------------------+---------------+-------------+------------------------------------+
| Módulo           | Casos Totales | Bugs Id.    | Estado de Madurez                  |
+------------------+---------------+-------------+------------------------------------+
| Autenticación    | 7 casos       | BUG-01      | Alta madurez, JWT robusto          |
| Artículos        | 17 casos      | BUG-02,03,  | Crítico: Vulnerabilidades BOLA     |
|                  |               | 04,07,08,09 | y control de acceso pendientes     |
| Comentarios      | 4 casos       | Ninguno     | 100% Estable                       |
| Perfiles         | 6 casos       | BUG-06      | Medio: Desincronización de flag UI |
| Favoritos        | 4 casos       | BUG-05      | Deficiente: Falla no controlada 500|
| Tags             | 3 casos       | Ninguno     | 100% Estable                       |
+------------------+---------------+-------------+------------------------------------+
`

### 3.1 Módulo Articles (Gestión de Artículos) — Máximo Foco de Riesgo
Este módulo concentra **6 de los 9 defectos detectados (66.7%)**, incluyendo el único defecto de severidad crítica (BUG-04):
- **Vulnerabilidad BOLA / IDOR:** Falta de verificación de la identidad del usuario contra el autor del registro tanto en PUT /api/articles/{slug} como en DELETE /api/articles/{slug}. Esto permite a cualquier atacante autenticado alterar o destruir contenido de terceros.
- **Riesgo de Seguridad en Feed (BUG-07):** El endpoint /api/articles/feed omite la exigencia de token de autenticación en la versión con defectos, retornando respuestas inconsistentes.
- **Validación de Límite BVA (BUG-09):** El parámetro limit no aplica un tope duro (min(limit, 20)), lo que expone a la base de datos a ataques de denegación de servicio (DoS) por sobrecarga de memoria al solicitar volúmenes masivos (limit=10000).

### 3.2 Módulo Favorites (Favoritos) — Defecto de Robustez
El endpoint POST /api/articles/{slug}/favorite genera una excepción no controlada (HTTP 500 Internal Server Error). En Python/SQLAlchemy, el código intentó realizar operaciones de lista sobre una relación desvinculada o un índice inexistente, violando el principio de diseño defensivo.

### 3.3 Módulo Profiles (Perfiles) — Consistencia de Estados
El endpoint de seguimiento (ollow) persiste la relación en la base de datos pero la capa de serialización mapea erróneamente el atributo boolean ollowing como False de forma estática, provocando una desincronización funcional inmediata con el cliente frontend.

### 3.4 Módulos Comentarios y Tags — Alta Estabilidad
Tanto la creación/borrado de comentarios como la extracción y ordenamiento de tags mostraron una tasa de aprobación del **100%**, respetando las autorizaciones, respuestas 404 ante artículos inexistentes y orden alfabético estricto.

---

## 4. Eficacia del Proceso de QA y Conclusiones

1. **Capacidad Detectora Comprobada:** La suite de pruebas demostró una sensibilidad del **100%**, identificando cada uno de los 9 defectos sin generar falsos positivos ni falsos negativos.
2. **Validación Cruzada (Test Automation + Exploratory Testing):** Los defectos más complejos de seguridad y paginación (BUG-03, BUG-04, BUG-09) fueron confirmados en dos dimensiones independientes: mediante aserciones programáticas de pytest y mediante interacción humana en Swagger UI con evidencias visuales fotográficas.
3. **Recomendación para Pase a Producción (Go / No-Go):**
   - **DICTAMEN: NO-GO (Rechazado para Producción en versión actual).**
   - **Justificación:** La presencia de BUG-04 (Borrado no autorizado de artículos) y BUG-03 (Modificación de contenido ajeno) representan una violación directa al principio de Confidencialidad e Integridad de la información (OWASP API Security Top 10 - API1:2023 Broken Object Level Authorization).
   - **Plan de Remediación Requerido:** Se deben corregir las dependencias de verificación de autoría en pp/api/routes/articles.py, corregir el gestor de favoritos en pp/services/articles.py, y re-ejecutar la suite completa de 41 pruebas para verificar la no-regresión (Regression Testing).

## 5. Evaluación del Riesgo de Negocio en la Plataforma Conduit

Desde la perspectiva estratégica de negocio, Conduit opera como una plataforma de publicación editorial donde el activo más valioso es el **contenido generado por los usuarios (UGC - User Generated Content)** y la **confianza de los autores**. Los defectos identificados impactan directamente en las tres dimensiones fundamentales del negocio digital:

`
+--------------------------------------------------------------------------------------------------+
|                            MATRIZ DE RIESGO E IMPACTO EN EL NEGOCIO                              |
+--------------------------+-----------------------+---------------------+-------------------------+
| Dimensión de Negocio     | Defecto Asociado      | Nivel de Riesgo     | Impacto Operativo/Legal |
+--------------------------+-----------------------+---------------------+-------------------------+
| Confidencialidad e       | BUG-03 (Edición ajena)| **CRÍTICO / ALTO**  | - Corrupción de autoría |
| Integridad Editorial     | BUG-04 (Borrado ajeno)|                     | - Riesgo de demandas por|
|                          |                       |                     |   pérdida de datos.     |
|                          |                       |                     | - Fuga masiva de autores|
+--------------------------+-----------------------+---------------------+-------------------------+
| Disponibilidad y         | BUG-09 (BVA limit=100)| **MEDIO / ALTO**    | - Sobrecarga de memoria |
| Resiliencia de Servidor  | BUG-07 (Feed sin auth)|                     |   y ataques DoS.        |
|                          |                       |                     | - Exposición de datos.  |
+--------------------------+-----------------------+---------------------+-------------------------+
| Engagement y Retención   | BUG-05 (Crash favor.) | **MEDIO**           | - Frustración de usuario|
| de Audiencia             | BUG-06 (Follow false) |                     | - Pérdida de tracción   |
|                          |                       |                     |   algorítmica social.   |
+--------------------------+-----------------------+---------------------+-------------------------+
| Estandarización y API    | BUG-01 (HTTP 200/201) | **BAJO**            | - Inconsistencia menor  |
| Contract                 |                       |                     |   en clientes frontend. |
+--------------------------+-----------------------+---------------------+-------------------------+
`

### 5.1 Caso de Negocio: Impacto Catastrófico de BUG-04
El defecto **BUG-04** permite que cualquier usuario registrado ejecute una petición DELETE /api/articles/{slug} y elimine permanentemente artículos pertenecientes a otros creadores de contenido. En un entorno productivo real:
1. Un atacante malintencionado podría crear una cuenta gratuita y ejecutar un script automatizado para barrer todos los slugs públicos de la plataforma, borrando el 100% de los artículos de la base de datos en cuestión de minutos.
2. Esto representaría una pérdida irrecuperable de propiedad intelectual para los autores, acarreando la destrucción del valor de mercado de la plataforma y contingencias legales graves bajo normativas de protección de datos.
