# Clasificación automática de respuestas "otros" usando IAG

## Descripción

Script Python que implementa la clasificación automática de respuestas ciudadanas de texto libre (categoría "otros") del Proceso Constituyente 2016, utilizando la API de OpenAI con el modelo gpt-4.1-mini.

---

## Requisitos

- Python 3.8 o superior
- Clave de API de OpenAI disponible como variable de entorno `OPENAI_API_KEY`

### Dependencias

```bash
pip install openai pandas tqdm matplotlib numpy openpyxl
```

---

## Estructura de archivos

```
clasificacion_iag/
├── clasificador-texto.py      # Script principal
├── input/                     # Datos de entrada
│   ├── raw-data.json          # Registros de todas las metacategorías (campo id_taxonomia discrimina)
│   └── taxonomias/            # Archivos JSON con taxonomías de categorías
│       ├── valores.json
│       ├── derechos.json
│       ├── deberes.json
│       └── instituciones.json
└── output/
    └── resultados-datos.json  # Resultados de clasificación de todas las metacategorías
```

---

## Modos de uso

El script opera en cuatro modos mediante el argumento `--modo`:

### 1. Preparar datos (`preparar`)
Convierte archivos Excel a JSON para su procesamiento.

```bash
# Convertir taxonomías
python clasificador-texto.py --modo preparar --taxonomias ./taxonomias

# Convertir datos de entrada
python clasificador-texto.py --modo preparar --datos_entrada ./input
```

### 2. Clasificar muestra (`muestra`)
Clasifica una muestra del dataset para validación previa.

```bash
python clasificador-texto.py --modo muestra \
  --taxonomias ./taxonomias \
  --datos_entrada ./input/valores.json \
  --datos_salida ./output/valores.json
```

### 3. Clasificar corpus completo (`completo`)
Clasifica el corpus completo. El archivo de entrada `raw-data.json` contiene todos los registros de todas las metacategorías. El script utiliza el campo `id_taxonomia` de cada registro para seleccionar la taxonomía correspondiente y construir el prompt adecuado.

```bash
python clasificador-texto.py --modo completo \
  --taxonomias ./input/taxonomias \
  --datos_entrada ./input/raw-data.json \
  --datos_salida ./output/resultados-datos.json \
  --guardar_cada 100
```

> **Nota:** El argumento `--guardar_cada 100` guarda el progreso cada 100 iteraciones, permitiendo reanudar el proceso ante interrupciones sin perder trabajo previo.

---

### 4. Exportar resultados a Excel (`exportar_excel`)
Convierte el JSON de resultados a Excel para revisión manual.

```bash
python clasificador-texto.py --modo exportar_excel \
  --entrada_json ./output/resultados-datos.json \
  --salida_excel ./output/resultados-datos-revision.xlsx
```

### 5. Generar histograma de tiempos (`histograma`)
Genera un histograma de tiempos de procesamiento por iteración.

```bash
python clasificador-texto.py --modo histograma \
  --entrada_json ./output/resultados-datos.json \
  --salida_histograma ./output/histograma_tiempos.png \
  --mostrar
```

---

## Parámetros del modelo

| Parámetro | Valor |
|-----------|-------|
| Modelo | gpt-4.1-mini |
| Temperatura | 0 |
| Reintentos máximos | 5 |
| Workers paralelos | 3 |
| Guardado de progreso | cada 50 iteraciones (configurable) |

---

## Prompt de clasificación

**System prompt:**
```
Eres un asistente experto en categorizar ideas ciudadanas dentro de una taxonomía constitucional.
Dado un texto libre y su fundamento, debes:
1. Asignar la categoría más adecuada de la lista proporcionada.
2. Indicar si el fundamento aporta o no a la clasificación.
Responde siempre con un JSON que tenga las siguientes claves:
- id_categoria
- categoria
- fundamento_aporta (true/false)
```

**User prompt:** construido dinámicamente para cada registro, incluye el texto libre (respuesta "otro"), el fundamento, la definición de la metacategoría según la guía metodológica oficial del proceso constituyente, y la lista completa de categorías específicas de la taxonomía correspondiente.

---

## Formato de salida

Cada registro clasificado incluye los siguientes campos:

| Campo | Descripción |
|-------|-------------|
| `id_taxonomia` | Metacategoría (1=Valores, 2=Derechos, 3=Deberes, 4=Instituciones) |
| `id_cabildo` | Identificador del cabildo de origen |
| `tipo_eleccion` | Tipo de proceso participativo |
| `tipo_cabildo` | Tipo de cabildo |
| `otro` | Texto libre original de la respuesta ciudadana |
| `fundamento` | Fundamento argumentativo original |
| `id_categoria` | Identificador numérico de la categoría asignada |
| `categoria` | Nombre textual de la categoría asignada |
| `fundamento_aporta` | Indica si el fundamento aportó información útil para la clasificación |
| `duracion` | Tiempo de procesamiento en segundos |

---

## Trazabilidad

Por cada ejecución el script genera:
- `log_respuestas_modelo.txt` — registro completo de cada clasificación con entrada y respuesta del modelo
- `log_errores_modelo.txt` — registro de errores de la API
- `progreso_temporal.json` — archivo de avance que permite reanudar el proceso ante interrupciones

---

## Resultados de la ejecución definitiva (diciembre 2025)

| Parámetro | Valor |
|-----------|-------|
| Modelo utilizado | gpt-4.1-mini |
| Total respuestas procesadas | 36.322 |
| Respuestas clasificadas exitosamente | 36.079 (99,36%) |
| Respuestas no clasificadas | 205 (0,56%) |
| Tiempo total de procesamiento | 9,9 horas |
| Promedio por iteración | 0,98 entradas/segundo |
| Costo total API | USD 18 |
| Tokens procesados | 38.896.283 |
