# Notebook de análisis

## Descripción

Este notebook documenta y reproduce los cálculos, indicadores y gráficos incluidos en el informe final de tesis. Está publicado con todos los outputs ejecutados, por lo que es legible directamente en GitHub sin necesidad de instalación.

---

## Contenido del notebook

| Sección | Descripción |
|---------|-------------|
| 0. Configuración | Conexión a base de datos PostgreSQL mediante SQLAlchemy |
| 1. Concentración de respuestas "otros" | Distribución de frecuencias por metacategoría antes de clasificación automática, destacando la predominancia de "otros" |
| 2. Proceso ML (2020) | Totales del corpus, clasificación manual por metacategoría y resultados de asignación |
| 3. Tiempos de ejecución IAG (2025) | Estadísticas descriptivas de los tiempos de procesamiento por registro durante la clasificación con IAG |
| 4. Proceso IAG (2025) | Cobertura de clasificación y distribución de categorías originales vs emergentes |
| 5. Comparativo ML vs IAG | Cálculo de coincidencia exacta entre ambos métodos |
| 6. Diversidad distributiva | Índices de Shannon, número efectivo de categorías e índice de Simpson |
| 7. Concentración temática | Categorías necesarias para explicar el 80% de la frecuencia por taxonomía |
| 8. Gráficos comparados ML vs IAG | Frecuencias ML vs IAG por metacategoría (Figuras 6 a 9) |
| 9. Evaluación experta | Kappa de Cohen por par, Kappa de Fleiss y distribución por mayoría simple |

---

## Gráficos incluidos

| Archivo | Descripción |
|---------|-------------|
| `figura_6_valores.png` | Frecuencias comparadas ML vs IAG — Valores y Principios |
| `figura_7_derechos.png` | Frecuencias comparadas ML vs IAG — Derechos |
| `figura_8_deberes.png` | Frecuencias comparadas ML vs IAG — Deberes y Responsabilidades |
| `figura_9_instituciones.png` | Frecuencias comparadas ML vs IAG — Instituciones del Estado |
| `figura_10_otros_valores.png` | Concentración de respuestas "otros" — Valores y Principios |
| `figura_11_otros_derechos.png` | Concentración de respuestas "otros" — Derechos |
| `figura_12_otros_deberes.png` | Concentración de respuestas "otros" — Deberes y Responsabilidades |
| `figura_13_otros_instituciones.png` | Concentración de respuestas "otros" — Instituciones del Estado |

Los gráficos de frecuencia comparada (figuras 6 a 9) muestran las 25 categorías más frecuentes por método, con etiquetas de frecuencia y en orden descendente. Los gráficos de concentración (figuras 10 a 13) destacan la categoría "otros" en naranja frente a las categorías predefinidas en azul.

---

## Requisitos para ejecutar

La conexión a la base de datos PostgreSQL requiere definir la variable `DB_PASSWORD` en un archivo `.env` en la raíz del proyecto:

```
DB_PASSWORD=tu_contraseña
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Los datos de entrada provienen de la base de datos local de la BCN y no están incluidos en el repositorio.
