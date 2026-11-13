# Métricas de Prueba de Software (Testing Metrics)
*Calidad de Software y Auditoría de Sistemas*

---

## 1. Fundamentos: ¿Qué es una métrica de prueba?

Una **métrica en pruebas de software** es una medida cuantitativa que describe el estado, la calidad o el avance del proceso de pruebas. Convierte la pregunta *“¿cómo vamos?”* en un número objetivo con el que se puede tomar decisiones.

### Conceptos y Vocabulario Clave

* **Medida:** El dato crudo capturado directamente.  
  * *Ejemplo:* Se ejecutaron $15$ casos de prueba.
* **Métrica:** Relación cuantitativa entre dos o más medidas.  
  * *Ejemplo:* $15$ de $20$ casos ejecutados = $75\%$ de avance.
* **Indicador / KPI:** Métrica que tiene asociada una meta u objetivo específico.  
  * *Ejemplo:* Cobertura $\ge 95\%$ antes de liberar el software a producción.

> **La Regla de Oro:**  
> *“Lo que no se mide, no se puede mejorar.”*  
> Sin embargo, medir sin una meta ni una decisión detrás solo genera ruido.

---

## 2. Motivación: ¿Por qué necesitamos métricas de prueba?

1. **Saber dónde estamos:** Aportan visibilidad objetiva sobre el avance real y permiten priorizar las tareas adecuadamente.
2. **Gestionar el riesgo:** Constituyen una herramienta clave para anticipar problemas antes de que escalen a etapas críticas.
3. **Decidir con evidencia:** Sustituyen opiniones subjetivas (*“yo creo que ya está listo”*) por datos verificables.
4. **Mejorar a futuro:** Los datos históricos registrados afinan las estimaciones y elevan la calidad en los siguientes ciclos de desarrollo.

> *Nota:* Nunca es tarde para empezar a registrar la información clave de tu proyecto.

### Beneficios de Medir

* **Dirección y alcance:** Permiten predecir el rumbo y el alcance a largo plazo.
* **Estimación y planeación:** Proporcionan una base empírica para estimar y facilitar la planificación.
* **Control y reporte:** Sirven de insumo principal para los reportes de estado y control gerencial.
* **Foco en el riesgo:** Identifican con precisión las áreas que requieren mayor esfuerzo de pruebas.
* **Decisiones más rápidas:** Señalan acciones correctivas y aceleran la toma de decisiones informadas.
* **Resolución temprana:** Detectan y ayudan a resolver problemas potenciales tempranamente.

---

## 3. Buenas Prácticas y Factores Clave

### Lo que SÍ se debe hacer
* Recolectar **únicamente** los datos que realmente se van a utilizar para decidir.
* Elegir las métricas por su importancia para los interesados (*stakeholders*), no por la facilidad de recolectarlas.
* Preferir un conjunto reducido de métricas accionables sobre muchas métricas que nadie revisa.
* Acompañar cada métrica de su **contexto** (meta, tendencia, *benchmark*).

### Lo que se debe EVITAR
* Tomar decisiones con base en datos variables o fáciles de manipular.
* Medir demasiado, demasiado pronto (o muy poco, demasiado tarde).
* Utilizar métricas que no aportan valor ni interesan a los interesados.
* Mostrar números sin explicar la decisión o acción que habilitan.

---

## 4. Ciclo de Vida de las Métricas

El establecimiento de un sistema de métricas de prueba sigue **seis pasos encadenados**:

1. **Identificar las métricas**
2. **Identificar los datos necesarios**
3. **Comunicar a los interesados**
4. **Capturar y verificar datos**
5. **Analizar y procesar**
6. **Reportar las métricas**

> **Principio de cadena:** Cada paso toma como entrada el producto del paso anterior. No se capturan datos sin saber qué métrica alimentan, ni se reporta nada que no haya sido verificado previamente.

---

### Paso 1: Identificar las métricas correctas
Las métricas correctas se definen **solo después** de determinar los objetivos que se quieren lograr. Antes de medir, se debe responder a cuatro preguntas fundamentales:

1. **¿Qué quieres medir y por qué?** El propósito define la métrica, no al revés.
2. **¿Cuál es el valor de cada métrica?** Analizar el beneficio obtenido frente al costo de su recolección.
3. **¿Quién es la audiencia?** Un gerente, un tester y un cliente requieren información y métricas distintas.
4. **¿Qué meta persigues?** Toda métrica útil se compara contra un objetivo o *target*.

---

### Paso 2: Identificar los datos (Métricas Base y Derivadas)

* **Métricas Base:** Se capturan directamente durante el proceso de pruebas. Representan el dato crudo.  
  * *Ejemplos:* Número de casos ejecutados, aprobados, fallidos, bloqueados.
* **Métricas Derivadas:** Se calculan a partir de las métricas base mediante una fórmula matemática.  
  * *Ejemplos:* $\%$ de avance, $\%$ de cobertura, densidad de defectos.

#### Fórmula Base de Ejecución
$$\text{Total de casos} = \text{Aprobados} + \text{Fallidos} + \text{Bloqueados}$$

*Ejemplo:*  
$$20 = 10 + 6 + 4$$

#### Ejemplo de Cálculo de Métrica Derivada: Cobertura de Pruebas
La **cobertura de pruebas** mide qué porción del alcance planeado ya ha sido probada:

$$\% \text{ Cobertura} = \left( \frac{\text{Casos Ejecutados}}{\text{Casos Planeados}} \right) \times 100$$

**Datos del Ejemplo:**
* Casos planeados: $20$
* Casos ejecutados: $15$
* $\%$ Cobertura: $\left(\frac{15}{20}\right) \times 100 = 75\%$
* $\%$ Pendiente: $25\%$ ($5$ casos restantes por ejecutar)

*Interpretación / Lectura:* El $75\%$ del alcance planeado ya fue probado; aún resta ejecutar $5$ casos para cerrar el ciclo de pruebas.

---

### Paso 3: Comunicar a los interesados
Para asegurar compromiso y resultados, la planeación de métricas debe involucrar a los interesados desde el inicio y no cuando los reportes ya están hechos.

* Comunicar la necesidad de las métricas a todos los equipos involucrados.
* Obtener retroalimentación activa de los interesados.
* Establecer expectativas claras: frecuencia de recolección de datos y periodicidad de generación de reportes.

**Participantes requeridos:**
* Equipo de Pruebas (QA)
* Equipo de Desarrollo
* Gerencia / Project Manager (PM)
* Product Owner (PO)
* Cliente / Pruebas de Aceptación de Usuario (UAT)

---

### Paso 4: Capturar y verificar los datos
* Asegurar que todo el mecanismo e infraestructura de captura esté disponible antes de iniciar la medición.
* Comunicar lineamientos claros al equipo sobre qué datos se recogen y por qué.
* Identificar las fuentes de datos inexactos en cada métrica base y aplicar acciones correctivas.
* Definir una plantilla común y estandarizada para capturar las métricas base de forma uniforme.

> **Regla fundamental:** *"Dato basura entra, dato basura sale"* (Garbage in, garbage out).  
> La calidad de cualquier métrica depende directamente de la calidad del dato capturado. Es imprescindible evitar ambigüedades y validar las fuentes.

---

### Paso 5: Analizar y procesar los datos
* Verificar que los datos registrados sean exactos, consistentes y actualizados.
* Definir la plantilla formal en la que se registran y procesan las métricas derivadas.
* Calcular las métricas derivadas utilizando las fórmulas correspondientes.
* Validar que las métricas transmitan la información y realidad correctas.

> *Nota:* Analizar es más que simplemente calcular números; una métrica que conduce a conclusiones equivocadas es peor que no tener ninguna métrica.

---

### Paso 6: Reportar las métricas
* El reporte debe incluir siempre un **resumen ejecutivo**.
* Presentar la información en un formato claro, visual y entendible, preferiblemente apoyado en gráficos e instrucciones para su interpretación.
* Señalar con claridad todos los problemas, desviaciones o puntos destacados.
* Comparar los resultados contra *benchmarks* preestablecidos y mostrar las tendencias en el tiempo.

> **Regla de presentación:** Un número aislado sin contexto no comunica. Un gráfico con tendencia y metas definidas sí transmite el estado real del proyecto (si el proceso va bien, mal o estancado).

---

## 5. Advertencia: Errores Comunes a Evitar

1. Falta de compromiso de la gerencia.
2. Medir demasiado, demasiado pronto.
3. Medir muy poco, demasiado tarde.
4. Seleccionar métricas equivocadas.
5. Definición vaga o inexacta de las métricas.
6. Recolectar datos que posteriormente no se utilizan.
7. Falta de comunicación entre equipos e interesados.
8. No compartir ni visibilizar los resultados obtenidos.

---

## 6. Métricas Usadas en Proyectos

Las métricas en proyectos se dividen en **cuatro familias principales** que acompañan al equipo durante todo el ciclo de desarrollo:

### 1. Fase de Diseño de Casos de Prueba
* Número de requisitos de prueba vs. áreas funcionales / requisitos del sistema.
* Número de casos planeados vs. casos listos para ejecución.
* Tiempo total de definición vs. tiempo estimado.
* Productividad del diseño (casos diseñados por hora de esfuerzo).

$$\% \text{ Avance de Diseño} = \left( \frac{\text{Casos Listos}}{\text{Casos Planeados}} \right) \times 100$$

*Seguimiento habitual:* Casos planeados vs. casos listos desglosados por responsable.

---

### 2. Ejecución y Progreso de las Pruebas
* Casos ejecutados vs. casos planeados.
* Tiempo real de ejecución vs. tiempo planeado.
* Conteo de casos aprobados, fallidos y bloqueados.
* Casos aprobados por área funcional.

$$\% \text{ Aprobados} = \left( \frac{\text{Casos Aprobados}}{\text{Casos Ejecutados}} \right) \times 100$$

*Ejemplo:* De $15$ casos ejecutados, $10$ aprobados $\rightarrow 67\%$ de aprobación; $6$ fallidos y $4$ bloqueados indican las áreas donde se debe intervenir.

---

### 3. Métricas de Producto (Defectos)
* Bugs creados vs. bugs cerrados por ciclo/sprint.
* Bugs cerrados vs. bugs reabiertos.
* Distribución de bugs por nivel de severidad (ej. Blocker, Critical, Major, Minor).
* Densidad de defectos por área funcional o módulo.
* Bugs detectados por caso de prueba ejecutado.

$$\text{Densidad de Defectos} = \frac{\text{Número de Defectos}}{\text{Tamaño del Módulo o Software (ej. por KLOC o por Módulo)}}$$

---

### 4. Métricas de Calidad y Efectividad de las Pruebas
La métrica clave en esta categoría es la **Eficiencia de Detección de Defectos** (DRE - *Defect Removal Efficiency*), la cual mide la capacidad del equipo para identificar defectos antes de que el software llegue al cliente final en producción.

$$DRE = \left( \frac{\text{Defectos Detectados por QA}}{\text{Defectos Detectados por QA} + \text{Defectos Escapados a Producción}} \right) \times 100$$

#### Ejemplo Práctico de DRE:
* Defectos detectados por QA: $90$
* Defectos escapados a producción: $10$

$$DRE = \left( \frac{90}{90 + 10} \right) \times 100 = 90\%$$

* **Tasa de Fuga (*Defect Leakage*):** $10\%$ (Objetivo: mantener esta tasa lo más baja posible).
* *Lectura:* Un $DRE$ del $90\%$ refleja una buena efectividad en pruebas; el $10\%$ restante corresponde a defectos detectados por el cliente que el proceso debe enfocarse en reducir.

#### Otras Métricas de Efectividad
* Bugs detectados en pruebas UAT que no fueron identificados previamente por el equipo de QA.
* Comparativa de bugs reportados: $\text{QA} / \text{UAT} / \text{Usuario Final en Producción}$.
* Tasa de captura de defectos.

---

## 7. Síntesis: Fórmulas Clave

| Métrica | Fórmula LaTeX |
| :--- | :--- |
| **$\%$ Cobertura** | $\% \text{ Cobertura} = \left( \frac{\text{Casos Ejecutados}}{\text{Casos Planeados}} \right) \times 100$ |
| **$\%$ Aprobación** | $\% \text{ Aprobación} = \left( \frac{\text{Casos Aprobados}}{\text{Casos Ejecutados}} \right) \times 100$ |
| **$\%$ Fallidos** | $\% \text{ Fallidos} = \left( \frac{\text{Casos Fallidos}}{\text{Casos Ejecutados}} \right) \times 100$ |
| **Densidad de Defectos** | $\text{Densidad} = \frac{\text{Defectos Totales}}{\text{Tamaño (KLOC o Módulo)}}$ |
| **Efectividad DRE** | $DRE = \left( \frac{\text{Defectos QA}}{\text{Defectos QA} + \text{Defectos Producción}} \right) \times 100$ |
| **Tasa de Reapertura** | $\% \text{ Reapertura} = \left( \frac{\text{Bugs Reabiertos}}{\text{Bugs Corregidos}} \right) \times 100$ |

---

## 8. Referencias Bibliográficas

1. **ISTQB** (2011). *Certified Tester Foundation Level Syllabus*.
2. **Globant** (2022). *Test Design Techniques*.
3. **GeeksforGeeks** (2025). *Software Testing Metrics: its Types and Example*.  
   Disponible en: [GeeksforGeeks - Software Testing Metrics](https://www.geeksforgeeks.org/software-testing/software-testing-metrics-its-types-and-example/)
4. **Guru99** (2025). *Test Metrics in Software Testing*.