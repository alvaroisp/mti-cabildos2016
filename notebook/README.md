# Notebook de análisis

## Descripción

Este notebook documenta y reproduce los cálculos, indicadores y gráficos incluidos en el informe final de tesis. Está publicado con todos los outputs ejecutados, por lo que es legible directamente en GitHub sin necesidad de instalación.

---

## Contenido del notebook

| Sección | Descripción |
|---------|-------------|
| 0. Configuración | Conexión a base de datos PostgreSQL mediante SQLAlchemy |
| 1. Proceso ML | Totales del corpus, clasificación manual por metacategoría y resultados de asignación |
| 2. Proceso IAG | Cobertura de clasificación y distribución de categorías originales vs emergentes |
| 3. Comparativo ML vs IAG | Cálculo de coincidencia exacta entre ambos métodos |
| 4. Diversidad distributiva | Índices de Shannon, número efectivo de categorías e índice de Simpson |
| 5. Concentración temática | Categorías necesarias para explicar el 80% de la frecuencia por taxonomía |
| 6. Gráficos comparados | Frecuencias ML vs IAG por metacategoría (Figuras 6 a 9) |
| 7. Evaluación experta | Kappa de Cohen por par, Kappa de Fleiss y distribución por mayoría simple |

---

## Gráficos incluidos

| Archivo | Descripción |
|---------|-------------|
| `figura_6_valores.png` | Frecuencias comparadas ML vs IAG — Valores y Principios |
| `figura_7_derechos.png` | Frecuencias comparadas ML vs IAG — Derechos |
| `figura_8_deberes.png` | Frecuencias comparadas ML vs IAG — Deberes y Responsabilidades |
| `figura_9_instituciones.png` | Frecuencias comparadas ML vs IAG — Instituciones del Estado |

Cada gráfico muestra las 25 categorías más frecuentes por método, con etiquetas de frecuencia y en orden descendente. La comparación entre ambos paneles permite identificar visualmente la estabilidad del núcleo temático dominante y las diferencias en categorías emergentes.

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
