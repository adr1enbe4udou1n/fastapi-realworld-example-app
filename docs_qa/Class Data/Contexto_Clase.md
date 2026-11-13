### Compendio Técnico: Fundamentos y Marcos Teóricos de Pruebas de Software

#### 1\. Fundamentos de Quality Assurance y Testing

##### 1.1 Definición Sistémica de Pruebas de Software

El  *testing*  o pruebas de software se concibe como un conjunto riguroso de actividades metodológicas e interrelacionadas orientadas a la identificación sistemática de defectos o fallos en un artefacto, componente o sistema de software.  
Desde la arquitectura de información y la teoría normativa del aseguramiento de calidad, el proceso de pruebas no se constriñe a la mera ejecución operacional de casos de prueba. Por el contrario, constituye un marco analítico integral compuesto estructuralmente por dos grandes fases interdependientes:

1. **Ejecución de las Pruebas:**  Fase operacional orientada a la ejercitación del objeto de prueba bajo condiciones especificadas y al registro sintáctico de los comportamientos observados.  
2. **Análisis de las Pruebas:**  Fase evaluativa y analítica dedicada al examen sistemático de los resultados obtenidos, el contraste de desviaciones, el diagnóstico de anomalías y la determinación de la causa raíz.

##### 1.2 Marco Comparativo: Quality Assurance (QA) vs. Quality Control (QC)

Dentro de la ingeniería de software, Quality Assurance (QA) y Quality Control (QC) constituyen dos áreas disciplinares diferenciadas ontológicamente por sus objetivos, alcance y momento de aplicación dentro del ciclo de vida del proyecto:  
Quality Assurance (QA),Quality Control (QC)  
Enfoque y Orientación:  Orientado primordialmente al proceso de desarrollo y a la optimización del ciclo de vida.,Enfoque y Orientación:  Orientado exclusivamente al producto de software en sus diversas etapas de construcción.  
Naturaleza de la Estrategia:  Estrategia proactiva centrada en la prevención sistemática de defectos antes de su consolidación.,Naturaleza de la Estrategia:  Estrategia reactiva focalizada en la detección e identificación de defectos preexistentes.  
"Tipología de Herramienta:  Herramienta de gestión de calidad que establece normativas, estándares y marcos operacionales.",Tipología de Herramienta:  Herramienta correctiva y de evaluación técnica directa sobre los artefactos producidos.  
Alcance de la Responsabilidad:  Responsabilidad transversal compartida por la totalidad de los roles involucrados en el proyecto.,Alcance de la Responsabilidad:  Responsabilidad delimitada y encomendada de forma específica al equipo de pruebas.  
"Momento de Implementación:  Implementación continua e iterativa, ejecutada en paralelo con el desarrollo del proyecto.",Momento de Implementación:  Implementación ejecutada posterior a la finalización o disponibilidad funcional del producto.

##### 1.3 Verificación vs. Validación en el Proceso de Software

El testing se articula normativamente dentro del marco integral de Verificación y Validación (V\&V) del software. La distinción conceptual entre ambas actividades se establece con rigor metodológico de la siguiente manera:

* **Verificación:**  Proceso analítico y objetivo destinado a determinar si los productos de trabajo de una fase dada cumplen con las condiciones y especificaciones impuestas en las etapas precedentes. Responde rigurosamente a la premisa teórica de determinar si el producto se está construyendo correctamente conforme a los requisitos, arquitecturas y estándares estipulados.  
* **Validación:**  Proceso de evaluación analítica orientado a confirmar que el producto de software final satisface las necesidades operativas, requisitos funcionales y expectativas declaradas por el usuario y los  *stakeholders* . Responde ontológicamente a la premisa de determinar si se está construyendo el producto esperado para su contexto de uso previsto.

##### 1.4 Objetivos Estructurales del Testing

La ejecución metodológica de pruebas de software en un marco normativo persigue los siguientes objetivos teóricos fundamentales:

* **Prevención de defectos:**  Identificar ambigüedades, omisiones o inconsistencias en etapas tempranas para evitar la propagación de anomalías hacia fases subsiguientes.  
* **Detección de fallos y defectos:**  Revelar desviaciones y discrepancias situadas entre el comportamiento observado en el sistema y las especificaciones normativas.  
* **Verificación de completitud y validación funcional:**  Certificar cuantitativa y cualitativamente que el objeto de prueba cumple con la totalidad de los requisitos especificados y responde a las necesidades operativas de los  *stakeholders* .  
* **Cumplimiento normativo:**  Validar la estricta alineación del software con los estándares técnicos, marcos regulatorios y directrices legales aplicables.  
* **Reducción del riesgo operativo y tecnológico:**  Disminuir la probabilidad de falla operacional e impactar positivamente en la mitigación de riesgos críticos en entornos de producción.  
* **Verificación formal de requisitos:**  Proveer evidencia documental de que cada requisito de software ha sido ejercitado y certificado en términos de cobertura.  
* **Construcción de confianza:**  Proporcionar métricas e indicadores cualitativos sobre el nivel de madurez tecnológica y calidad estructural alcanzado por el sistema.

#### 2\. Taxonomía de Anomalías y Métricas de Clasificación

##### 2.1 Cadena Causal: Error, Defecto (Bug) y Fallo

La caracterización sintáctica de las anomalías en la ingeniería de software se rige por una secuencia causal estricta, la cual delimita el origen, la manifestación estática y el evento dinámico:  
**Error:**  Acción humana incorrecta realizada durante las actividades de concepción, especificación, arquitectura, diseño o codificación del software, que conduce a la introducción de una inconsistencia sintáctica o lógica en un producto de trabajo.  
**Defecto (Bug):**  Imperfección, desviación o resultado incorrecto presente en un artefacto o producto de trabajo de software (código fuente, documento de requisitos, diagrama de diseño), provocado directamente por un error humano subyacente.  
**Fallo:**  Evento o manifestación dinámica externa en la cual un componente o sistema deja de realizar la función requerida o la ejecuta fuera de los límites, tolerancias y especificaciones normativas estipuladas.

##### 2.2 Dimensiones de Evaluación: Severidad vs. Prioridad

La clasificación analítica de las anomalías reportadas en un ciclo de testing requiere la disociación conceptual de dos métricas multidimensionales independientes:

* **Severidad:**  Métrica objetiva de índole puramente técnica que evalúa el grado de impacto, gravedad o degradación estructural que la presencia de un defecto ejerce sobre la arquitectura, la estabilidad funcional o la integridad del sistema.  
* **Prioridad:**  Métrica de gestión y de negocio, fijada por los  *stakeholders*  o la dirección del proyecto, que determina la urgencia, presteza o prelación cronológica requerida para la resolución y corrección de un defecto dentro del plan de trabajo.

#### 3\. Principios Fundamentales del Testing (ISTQB)

##### 3.1 Exposición de los 7 Principios del Testing

El marco doctrinario propuesto por ISTQB consolida siete principios teóricos que orientan la estrategia y ejecución formal del testing de software:

1. **Las pruebas muestran la presencia de defectos:**  El testing riguroso permite evidenciar la presencia de anomalías dentro de un sistema, pero carece de la capacidad teórica para demostrar la ausencia absoluta de defectos. La no detección de fallos durante un ciclo de ejecución no constituye una prueba matemática de corrección del software.  
2. **Las pruebas exhaustivas no son posibles:**  Salvo en sistemas triviales de alcance finito, resulta inviable ejercitar la totalidad de las combinaciones de entradas, parámetros, precondiciones y rutas lógicas. La estrategia de pruebas debe fundamentarse en la evaluación de riesgos, la priorización funcional y el análisis contextual.  
3. **Pruebas tempranas:**  Las actividades de prueba deben iniciar en la fase más temprana posible del ciclo de vida del software (fases de requisitos y diseño). La detección precoz de anomalías reduce exponencialmente los costos de corrección y retrabajo.  
4. **Agrupamiento de defectos (**  ***Defect clustering***  **):**  La distribución de defectos en un sistema no es uniforme; empíricamente, la gran mayoría de los fallos operacionales y defectos detectados se concentran en un número reducido de módulos o componentes críticos.  
5. **La paradoja del pesticida:**  Si un conjunto idéntico de casos de prueba se repite de manera invariable a lo largo del tiempo, la suite perderá progresivamente su capacidad para descubrir nuevos defectos. Para mitigar este fenómeno, los casos de prueba deben ser revisados, actualizados y diversificados periódicamente.  
6. **Las pruebas dependen del contexto:**  La estrategia, técnicas, profundidad y tipos de prueba aplicados están supeditados de manera estricta al dominio del software, la criticidad operativa del negocio y el entorno tecnológico de despliegue.  
7. **La falacia de ausencia de errores:**  La identificación y rectificación de un volumen elevado de defectos no garantiza por sí sola el éxito o la usabilidad del sistema si la solución construida resulta inoperante, inviable o desacoplada de las necesidades y expectativas reales del usuario final.

#### 4\. Glosario Técnico Integrado de Artefactos y Conceptos

* **Plan de Pruebas (**  ***Test Plan***  **):**  Documentación formal que describe los objetivos de prueba a alcanzar, la delimitación del alcance, los recursos asignados, la gestión de riesgos, el cronograma de actividades y la organización directiva de las tareas involucradas.  
* **Alcance de las Pruebas (**  ***Scope***  **):**  Declaración normativa que delimita de manera precisa los componentes, áreas funcionales o atributos de calidad de un producto que serán sometidos a evaluación, especificando la tipología de defectos de interés y formalizando las exclusiones explícitas del proceso.  
* **Proceso:**  Conjunto de actividades interrelacionadas o interactivas que transforman elementos de entrada ( *inputs* ) en productos o resultados de salida ( *outputs* ), sujetas a mecanismos de control y puntos de seguimiento para evaluar su desempeño.  
* **Caso de Prueba (**  ***Test Case***  **):**  Conjunto estructurado de precondiciones, valores de entrada, acciones, resultados esperados y postcondiciones, desarrollado con el objetivo de ejercitar una condición específica, verificar un requisito funcional o validar una ruta lógica de ejecución.  
* **Suite de Pruebas (**  ***Test Suite***  **):**  Agrupación conceptual y estructurada de casos de prueba organizados sintácticamente para ser ejecutados de forma secuencial o paralela dentro de un ciclo o iteración de pruebas determinado.  
* **Datos de Prueba (**  ***Test Data***  **):**  Valores, estructuras de datos o conjuntos de información explícitamente creados o seleccionados para satisfacer las precondiciones e insumos necesarios en la ejecución de uno o más casos de prueba.  
* **Cronograma de Pruebas (**  ***Test Schedule***  **):**  Ordenación temporal estructurada que especifica la secuencia de actividades, tareas o eventos del proceso de pruebas, fijando sus fechas normativas de inicio, término e interdependencias operativas.  
* **Matriz de Riesgos:**  Instrumento analítico de evaluación y clasificación de problemas potenciales que asigna valores ponderados a la probabilidad de ocurrencia y a la severidad del impacto, facilitando la priorización del esfuerzo de prueba.  
* **Criterios de Salida (**  ***Exit Criteria***  **):**  Conjunto normativo de condiciones, métricas de cobertura y umbrales de calidad que deben cumplirse estrictamente para declarar formalmente completada una fase o tarea del ciclo de pruebas.  
* **Trazabilidad Bidireccional:**  Relación documentada y mantenible a lo largo del ciclo de vida que vincula en ambas direcciones los artefactos de desarrollo (requisitos, especificaciones) con los artefactos de pruebas (condiciones, casos de prueba, resultados y defectos), garantizando el análisis de cobertura e impacto.  
* **Métrica:**  Indicador cuantitativo formal utilizado para medir, evaluar y analizar el desempeño, la madurez del proceso, la cobertura de pruebas y la calidad del software, fundamentando la toma de decisiones informada.  
* **Smoke Test:**  Evaluación inicial, concisa y de nivel superficial orientada a verificar la estabilidad básica del entorno de pruebas y la build del sistema antes de proceder con la ejecución de suites de prueba de mayor profundidad.  
* **Testware:**  Conjunto especializado de artefactos, outcomes y productos de trabajo generados dentro del proceso de pruebas (con especial énfasis en contextos de pruebas automatizadas), que abarca desde la documentación técnica y los scripts de prueba hasta los registros de bugs y sus niveles de severidad asociados.  
* **Hito (**  ***Milestone***  **):**  Punto de control o evento formal de significancia estratégica dentro de la planificación del proyecto, utilizado para señalar la consecución de un objetivo normativo o la finalización de un entregable clave.

#### 5\. Ciclo de Vida: SDLC vs. STLC

##### 5.1 Marco Comparativo entre SDLC y STLC

* **SDLC (Software Development Life Cycle):**  Marco de referencia formal definido por el estándar ISO/IEC 12207 que establece el enfoque general para el desarrollo de software sobre el proceso y las actividades que se llevarán a cabo desde la definición del producto de software hasta su uso final, así como los entregables que se crearán y entregarán al cliente. Sus fases generales comprenden: Planeación, Análisis, Diseño, Implementación/Pruebas y Mantenimiento.  
* **STLC (Software Testing Life Cycle):**  Subconjunto específico y disciplinado de actividades metodológicas orientadas a la concepción, análisis, diseño, preparación, ejecución y cierre de las pruebas de software, estructurado explícitamente para certificar la calidad de un producto en alineación con el SDLC.

##### 5.2 Fases del STLC (Software Testing Life Cycle)

###### *1\. Test Analysis (Análisis de Pruebas)*

* **Premisa:**  Definición rigurosa del objeto de evaluación en respuesta a la interrogante teórica:  *"¿Qué probar?"*  ( *What to test* ).  
* **Actividades clave:**  
* Análisis detallado de las bases de prueba ( *test basis* ) asociadas al nivel de pruebas bajo evaluación.  
* Evaluación crítica de las bases de prueba y los ítems de prueba para identificar ambigüedades, inconsistencias o defectos en la especificación.  
* Identificación formal de las  *features*  y conjuntos de funcionalidades sujetas a evaluación.  
* Definición y priorización metodológica de las condiciones de prueba.  
* **Entregables / Salidas:**  Especificación formal de condiciones de prueba analizadas y priorizadas.

###### *2\. Test Design (Diseño de Pruebas)*

* **Premisa:**  Formalización de la estrategia operacional en respuesta a la interrogante teórica:  *"¿Cómo probar?"*  ( *How to test* ).  
* **Actividades clave:**  
* Diseño, formalización y priorización de casos de prueba abstractos y concretos.  
* Identificación y especificación de los datos de prueba requeridos.  
* Diseño del entorno de pruebas e identificación de requisitos de infraestructura y herramientas.  
* Selección y asignación de las técnicas de diseño de prueba dinámicas a implementar.  
* Establecimiento y captura de la trazabilidad bidireccional entre requisitos y casos de prueba.  
* **Entregables / Salidas:**  Condiciones de prueba refinadas, conjuntos de casos de prueba especificados, datos de prueba identificados, arquitectura del ambiente de pruebas e infraestructura requerida.

###### *3\. Test Implementation (Implementación de Pruebas)*

* **Premisa:**  Evaluación de la preparación operativa y disponibilidad de artefactos previa a la ejecución ( *"Do we have everything in place?"* ).  
* **Actividades clave:**  
* Elaboración, estructuración y priorización de los procedimientos de prueba o scripts.  
* Integración y secuenciación de  *test suites*  a partir de los procedimientos desarrollados.  
* Construcción, verificación y despliegue del ambiente de pruebas.  
* Creación, carga y preparación efectiva de los datos de prueba en el entorno.  
* Verificación y actualización sistemática de la matriz de trazabilidad bidireccional.  
* **Entregables / Salidas:**  Procedimientos de prueba, secuencia de ejecución de procedimientos,  *test suites*  consolidadas, cronograma de ejecución de pruebas y datos de prueba creados.

###### *4\. Test Execution (Ejecución de Pruebas)*

* **Premisa:**  Evaluación comparativa entre el comportamiento real desplegado por el software y el comportamiento esperado normativo ( *Actual Results vs Expected Results* ).  
* **Actividades clave:**  
* Registro riguroso de las identificaciones (IDs) y versiones de los elementos e ítems de prueba evaluados.  
* Ejecución de pruebas conforme a los procedimientos e instrumentación de comparación de resultados.  
* Análisis de anomalías e inconsistencias detectadas para la emisión y reporte formal de defectos.  
* Repetición de actividades de prueba ( *re-testing* ) para confirmar correcciones y ejecución de pruebas de regresión.  
* Mantenimiento y actualización continua de la trazabilidad bidireccional.  
* **Entregables / Salidas:**  Documentación del estado de los casos de prueba (pasado/fallado/bloqueado), reportes de defectos formalizados y documentación analítica sobre el  *testware*  involucrado.

###### *5\. Test Completion (Completitud de Pruebas)*

* **Premisa:**  Evaluación del cumplimiento de hitos estratégicos y criterios de cierre del proyecto ( *Project Milestones* ).  
* **Actividades clave:**  
* Revisión formal de los reportes de defectos registrados y gestión del cierre de sus estados operacionales.  
* Consolidation y redacción del reporte de resumen de pruebas ( *Test Summary Report* ).  
* Finalización, empaquetado, preservación y archivado del  *testware*  generado.  
* Examen y análisis sistemático de lecciones aprendidas.  
* Identificación de ítems de acción para la mejora continua del nivel de madurez del proceso de pruebas.  
* **Entregables / Salidas:**  Reporte de resumen de pruebas ( *Test Summary Report* ), matriz de ítems de acción para iteraciones futuras,  *backlog*  actualizado de producto y  *testware*  finalizado y archivado.

##### 5.3 Fases Transversales del STLC

El ciclo de vida de pruebas integra dos etapas transversales de acompañamiento continuo que operan en paralelo durante la totalidad del proceso:

1. **Test Planning (Planeación de Pruebas):**  Disciplina transversal orientada a definir los objetivos generales del testing y el enfoque metodológico para alcanzarlos dentro de las restricciones impuestas por el contexto del proyecto. Su resultado formal se plasma en los  *Test Plans* .  
2. **Test Monitoring & Control (Monitoreo y Control de Pruebas):**  
3. **Monitoreo:**  Actividad de supervisión continua encargada de comparar el progreso real de las actividades frente a las estimaciones del  *Test Plan*  mediante métricas e indicadores de seguimiento formalizados en la teoría. Dicha supervisión evalúa estrictamente:  
4. *Task Completion*  (Completitud de tareas).  
5. *Resource Allocation and Usage*  (Asignación y uso de recursos).  
6. *Effort*  (Esfuerzo).  
7. *Test Progress Reports*  (Reportes de progreso de pruebas).  
8. *Test Summary Reports*  (Reportes de resumen de pruebas).  
9. **Control:**  Ejecución de acciones correctivas, directivas y reajustes necesarios para reconducir el proceso y garantizar el cumplimiento de los objetivos definidos en el plan.  
10. Ambas actividades se soportan de manera continua en la evaluación sistemática de los  **criterios de salida**  ( *exit criteria* ) preestablecidos.

#### 6\. Marcos Teóricos de Técnicas de Diseño de Casos de Prueba

##### 6.1 Taxonomía General de Técnicas de Prueba Dinámicas

Las técnicas de diseño de casos de prueba aplicadas en el testing dinámico se estructuran formalmente en tres categorías teóricas principales:

* **Técnicas Basadas en la Especificación (Caja Negra / Black-Box):**  Enfocadas en derivar casos de prueba directamente a partir de la documentación funcional o especificaciones de requisitos, sin considerar la estructura lógica interna del código fuente. Comprende:  
* Partición de Equivalencia ( *Equivalence Partitioning* )  
* Análisis de Valores Límite ( *Boundary Value Analysis* )  
* Tablas de Decisión ( *Decision Table Testing* )  
* Transición de Estados ( *State Transition Testing* )  
* Pruebas de Casos de Uso ( *Use Case Testing* )  
* **Técnicas Basadas en la Estructura (Caja Blanca / White-Box):**  Enfocadas en medir y garantizar la Cobertura ( *Coverage* ) de la arquitectura interna, el flujo de control y las sentencias del código fuente. Comprende:  
* Cobertura de Sentencias ( *Statement Testing and Coverage* )  
* Cobertura de Decisiones ( *Decision Testing and Coverage* )  
* Cobertura de Condiciones ( *Condition Coverage* )  
* Cobertura de Múltiples Condiciones ( *Multiple Condition Coverage* )  
* **Técnicas Basadas en la Experiencia:**  Métodos fundamentados en el conocimiento analítico, la intuición técnica y el sesgo histórico del profesional de pruebas. Comprende:  
* Predicción de Errores ( *Error Guessing* )  
* Pruebas Exploratorias ( *Exploratory Testing* )  
* Pruebas Basadas en Listas de Chequeo ( *Checklist-Based Testing* )

##### 6.2 Enfoque Teórico: Partición de Equivalencia ( *Equivalence Partitioning* )

1. **Concepto:**  Técnica de caja negra mediante la cual el dominio de datos de entrada o salida de un sistema se divide en particiones discretas, asumiendo teóricamente que el módulo de software procesará de forma idéntica a todos los elementos pertenecientes a una misma partición.  
2. **Principio Fundamental:**  Si un caso de prueba diseñado con un valor representativo dentro de una partición específica descubre un defecto, todos los demás valores pertenecientes a esa misma partición poseen una elevada probabilidad estadística de detectar la misma anomalía.  
3. **Regla Metodológica:**  El diseño de pruebas debe garantizar la cobertura de cada partición identificada al menos una vez, considerando obligatoriamente tanto las particiones válidas (datos aceptados por el sistema) como las particiones inválidas (datos rechazados que deben desencadenar manejo de excepciones).  
4. **Pasos Teóricos de la Técnica:**  
5. Identificar e independizar las particiones de equivalencia válidas e inválidas del dominio.  
6. Crear un caso de prueba por cada partición para ejercitar un elemento representativo de la misma.

##### 6.3 Enfoque Teórico: Análisis de Valores Límite ( *Boundary Value Analysis* )

* **Concepto:**  Técnica de caja negra complementaria a la partición de equivalencia, cuyo objetivo es el diseño de casos de prueba enfocados específicamente en los bordes, fronteras o extremos del dominio de una partición de equivalencia.  
* **Fundamento de Riesgo:**  La justificación teórica de esta técnica radica en que la densidad de defectos en el software tiende a concentrarse en las fronteras de las particiones. Esto es consecuencia del patrón de error humano al implementar operadores condicionales y relacionales en las estructuras de decisión del código (tales como la confusión sintáctica entre operadores estrictos o no estrictos), o bien por errores en la delimitación de rangos e índices de arreglos.  
* **Pasos Teóricos de la Técnica:**  
* Identificar las particiones de equivalencia asociadas a la especificación.  
* Determinar los valores límite exactos que delimitan las fronteras de cada partición.  
* Crear casos de prueba para cada punto frontera evaluando:  
* El valor situado exactamente sobre el límite ( *on the boundary* ).  
* Un valor situado inmediatamente por debajo del límite ( *below the boundary* ).  
* Un valor situado inmediatamente por encima del límite ( *above the boundary* ).

