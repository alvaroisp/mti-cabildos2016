# Clasificación automática de categorías constitucionales usando IA Generativa

Repositorio del proyecto de investigación desarrollado como parte del trabajo de titulación del Magíster en Tecnologías de Información de la Universidad Técnica Federico Santa María, 2026.

**Título:** Clasificación automática de categorías constitucionales del proceso constitucional chileno de 2016, usando IA generativa  
**Autor:** Álvaro Sandoval Pizarro  
**Profesor guía:** Carlos Valle Vidal, PhD  

---

## Descripción

Este proyecto evalúa si la Inteligencia Artificial Generativa (IAG) puede clasificar masivamente las respuestas "otros" del Proceso Constituyente Chileno de 2016, con resultados comparables o superiores al proceso de clasificación realizado en 2020 mediante Machine Learning clásico (ML).

La etapa participativa del proceso constituyente (abril–agosto 2016) recopiló más de 264.000 respuestas ciudadanas en cabildos locales (ELA), provinciales y regionales. La categoría "otros" —donde los participantes aportaron conceptos constitucionales no incluidos en el listado oficial— concentró la mayor frecuencia en todas las instancias de cabildo, representando un desafío de sistematización a gran escala.

La solución desarrollada utiliza la API de OpenAI (modelo gpt-4.1-mini) para clasificar más de 36.000 respuestas "otros" en una taxonomía de conceptos constitucionales estructurada en cuatro metacategorías: Valores y Principios, Derechos, Deberes y Responsabilidades, e Instituciones del Estado.

---

## Estructura del repositorio

```
mti-cabildos2016/
│
├── datos_originales/
│   ├── dataset_gobierno/          # Enlaces al dataset original publicado como datos abiertos
│   │   └── README.md              # Fuente, descripción y enlaces de descarga
│   └── informes_oficiales/        # Informes oficiales del proceso constituyente 2016
│       └── README.md              # Descripción y enlaces a documentos en BCN
│
├── clasificacion_iag/
│   ├── clasificador-texto.py      # Script Python de clasificación automática
│   ├── input/
│   │   ├── raw-data.json          # Registros de todas las metacategorías
│   │   └── taxonomias/            # Taxonomías de categorías por metacategoría
│   │       ├── valores.json
│   │       ├── derechos.json
│   │       ├── deberes.json
│   │       └── instituciones.json
│   ├── output/
│   │   └── resultados-datos.json  # Resultados de clasificación IAG
│   └── README.md                  # Descripción del proceso y parámetros utilizados
│
├── evaluacion_experta/
│   ├── encuesta_evaluacion.xlsx   # Planilla con evaluaciones de los 3 expertos
│   └── README.md                  # Descripción del instrumento y resultados
│
├── notebook/
│   ├── analisis_clasificacion_constitucional.ipynb  # Notebook con análisis completo
│   ├── figura_6_valores.png        # Frecuencias comparadas ML vs IAG — Valores y Principios
│   ├── figura_7_derechos.png       # Frecuencias comparadas ML vs IAG — Derechos
│   ├── figura_8_deberes.png        # Frecuencias comparadas ML vs IAG — Deberes y Responsabilidades
│   ├── figura_9_instituciones.png  # Frecuencias comparadas ML vs IAG — Instituciones del Estado
│   ├── figura_10_otros_valores.png        # Concentración de "otros" — Valores y Principios
│   ├── figura_11_otros_derechos.png       # Concentración de "otros" — Derechos
│   ├── figura_12_otros_deberes.png        # Concentración de "otros" — Deberes y Responsabilidades
│   ├── figura_13_otros_instituciones.png  # Concentración de "otros" — Instituciones del Estado
│   └── README.md                   # Descripción del notebook y requisitos
│
└── README.md                      # Este archivo
```

---

## Antecedentes históricos

### Dataset original
Los resultados de la etapa participativa del Proceso Constituyente 2016 fueron publicados por el gobierno de Chile como datos abiertos en 2017. Este repositorio incluye únicamente los datos de las instancias de cabildo (ELA, provincial y regional). Ver [`datos_originales/dataset_gobierno/README.md`](datos_originales/dataset_gobierno/README.md) para los enlaces de descarga.

### Informes oficiales
Se enlazan los informes metodológicos y de resultados elaborados durante el proceso constituyente de 2016, alojados en servidores de la Biblioteca del Congreso Nacional de Chile. Ver [`datos_originales/informes_oficiales/README.md`](datos_originales/informes_oficiales/README.md).

---

## Proceso de clasificación IAG

El script `clasificador-texto.py` implementa la clasificación automática con las siguientes características:

- **Modelo:** gpt-4.1-mini (OpenAI API)
- **Temperatura:** 0
- **Procesamiento:** paralelo mediante ThreadPoolExecutor
- **Trazabilidad:** registro de cada clasificación con metadatos y tiempos de ejecución
- **Recuperación:** capacidad de reanudar el proceso ante interrupciones
- **Output:** archivo JSON único con id_categoria, categoria y fundamento_aporta por registro

El proceso clasificó el 99,36% de las 36.322 respuestas "otros" de las instancias local, provincial y regional, con un costo total de USD 18 y 9,9 horas de procesamiento.

---

## Evaluación experta

Se seleccionó una muestra aleatoria de 200 casos donde ML e IAG asignaron categorías distintas. Tres expertos de distintas disciplinas evaluaron cada caso de manera independiente. Ver [`evaluacion_experta/README.md`](evaluacion_experta/README.md) para el instrumento completo, la escala de evaluación y los resultados.

---

## Resultados principales

- **Coincidencia exacta ML–IAG:** 58,1% de las respuestas "otros"
- **Cobertura IAG:** 99,36% (vs 93,39% de ML)
- **Concordancia inter-evaluadora:** Kappa de Fleiss = 0,059 (nivel leve), reflejo de la naturaleza interpretativa de la clasificación temática constitucional
- **Diversidad distributiva:** IAG presenta mayor diversidad que ML (Shannon: 4,588 vs 4,549; número efectivo de categorías: 98,3 vs 94,5)
- **Categorías emergentes activadas:** 147 (IAG) vs 90 (ML)

---

## Notebook de análisis

El notebook `notebook/analisis_clasificacion_constitucional.ipynb` documenta y reproduce los cálculos, indicadores y gráficos incluidos en el informe final. Está publicado con todos los outputs ejecutados, por lo que es legible directamente en GitHub sin necesidad de instalación. Ver [`notebook/README.md`](notebook/README.md) para el detalle de contenidos, gráficos y requisitos de ejecución.

---

## Licencias

- **Código** (scripts Python, notebooks): [MIT License](LICENSE-MIT)
- **Datos y documentos** (JSONs, planilla de evaluación): [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE-CC-BY)

Al usar o citar este repositorio, por favor referenciar:

> Sandoval Pizarro, Á. (2026). *Clasificación automática de categorías constitucionales del proceso constitucional chileno de 2016, usando IA generativa*. Magíster en Tecnologías de Información, Universidad Técnica Federico Santa María.

---

## Contacto

Álvaro Sandoval Pizarro  
alsandoval@bcn.cl  
Biblioteca del Congreso Nacional de Chile
