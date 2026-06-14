# Evaluación experta de calidad de clasificación ML vs IAG

## Descripción

Este directorio contiene los resultados de la validación cualitativa del proceso de clasificación, realizada mediante evaluación experta independiente sobre una muestra de 200 casos donde Machine Learning (ML) e Inteligencia Artificial Generativa (IAG) asignaron categorías distintas.

---

## Archivo incluido

| Archivo | Descripción |
|---------|-------------|
| `encuesta_evaluacion.xlsx` | Planilla con las evaluaciones de los 3 expertos, incluyendo notas y comentarios por caso |

---

## Perfil de los evaluadores

La evaluación fue aplicada a tres especialistas con perfiles disciplinares complementarios:

- Un sociólogo con experiencia directa en el proceso de clasificación manual realizado en 2020
- Un abogado constitucionalista
- Una abogada experta en Derecho Internacional

Cada evaluador trabajó de manera independiente, sin consultar con los otros.

---

## Instrumento de evaluación

El siguiente instrumento fue enviado a cada evaluador:

### Contexto

Durante el Proceso Constituyente 2016, ciudadanos aportaron conceptos constitucionales en texto libre (categoría "otros"). Estos fueron clasificados usando dos metodologías:

- **ML:** Machine Learning clásico (2020)
- **IAG:** Inteligencia Artificial Generativa — GPT-4.1-mini (2025)

### Tarea

Evaluar 200 casos donde ML e IAG asignaron categorías diferentes, determinando cuál clasificación es más apropiada o si ambas son equivalentes.

### Escala de evaluación

Para cada caso, asignar UNO de estos valores:

| Código | Significado | Cuándo usar |
|--------|-------------|-------------|
| 1 | ML es mejor | La categoría ML captura mejor el concepto ciudadano |
| 2 | IAG es mejor | La categoría IAG es más precisa o específica |
| 3 | Equivalentes | Ambas clasificaciones son válidas |
| 4 | Ambas incorrectas | Ninguna refleja adecuadamente el concepto |
| 9 | No evaluable | Texto ambiguo o insuficiente información |

### Criterios de evaluación

- **Precisión semántica:** ¿Cuál refleja mejor el significado del texto?
- **Especificidad apropiada:** ¿Es demasiado genérica o específica?
- **Coherencia con fundamento:** ¿Es consistente con la argumentación?
- **Cobertura del concepto:** ¿Captura el tema principal?

### Notas importantes

- Los datos están anonimizados
- Evaluar independientemente (no consultar con el otro experto)
- Usar la columna "notas" para comentarios sobre casos difíciles
- Algunos fundamentos son muy breves (~20 caracteres) — usar código 9 si no hay suficiente información

---

## Diseño muestral

- **Universo:** casos donde ML e IAG asignaron categorías distintas (39,3% del corpus, ~14.190 respuestas)
- **Depuración:** se consolidaron respuestas únicas, obteniendo un corpus superior a 6.000 registros
- **Muestra:** 200 casos seleccionados aleatoriamente, priorizando aquellos con mayor extensión en el campo "fundamento"

---

## Estructura de la planilla

| Columna | Descripción |
|---------|-------------|
| `pregunta` | Metacategoría (valores, derechos, deberes, instituciones) |
| `otro` | Texto libre original de la respuesta ciudadana |
| `fundamento` | Fundamento argumentativo original |
| `categoria_iag` | Categoría asignada por IAG |
| `categoria_ml` | Categoría(s) asignada(s) por ML |
| `evaluacion_eval1` | Evaluación del evaluador 1 (códigos 1, 2, 3, 4, 9) |
| `evaluacion_eval2` | Evaluación del evaluador 2 |
| `evaluacion_eval3` | Evaluación del evaluador 3 |
| `notas_eval1` | Comentarios del evaluador 1 |
| `notas_eval2` | Comentarios del evaluador 2 |
| `notas_eval3` | Comentarios del evaluador 3 |

---

## Resultados principales

| Métrica | Valor |
|---------|-------|
| Casos evaluados | 200 |
| Acuerdo observado promedio | 32,7% |
| Kappa de Cohen promedio (por par) | 0,089 |
| Kappa de Fleiss (3 evaluadores) | 0,059 |
| Interpretación | Acuerdo leve — refleja la naturaleza interpretativa de la clasificación temática constitucional |

### Distribución por mayoría simple (≥2 de 3 evaluadores)

| Código | Evaluación | Casos | % |
|--------|------------|-------|---|
| 1 | ML mejor | 41 | 20,5% |
| 2 | IAG mejor | 70 | 35,0% |
| 3 | Equivalentes | 19 | 9,5% |
| 4 | Ambas incorrectas | 7 | 3,5% |
| 9 | No evaluable | 1 | 0,5% |
| — | Sin consenso | 62 | 31,0% |
