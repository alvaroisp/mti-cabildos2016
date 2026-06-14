import pandas as pd
import json
import openai
import os
import time
import re
import argparse
from openai import OpenAI
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

# Configurar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Archivos de log por defecto
LOG_RESPUESTAS = "log_respuestas_modelo.txt"
LOG_ERRORES = "log_errores_modelo.txt"
PROGRESO_PATH = "progreso_temporal.json"

# Propuestas por la metodología oficial
DEFINICIONES_TAXONOMIA = {
    1: "Valores y principios: Son directrices de mayor importancia que orientan el accionar y que son estimados y compartidos por una comunidad. Suelen ser incorporados en el preámbulo o en los primeros capítulos de las constituciones, pues constituyen la base sobre la cual la sociedad se ordena jurídica, social, económica y políticamente.",
    2: "Derechos: Se refiere a los derechos básicos que la sociedad estima como más valiosos. En la mayoría de las constituciones estos se suelen clasificar entre Derechos Políticos (que facultan la participación de los ciudadanos y ciudadanas en la conducción del Estado), Derechos Civiles (que aseguran la libertad y autonomía de las personas) y Derechos Económicos, Sociales y Culturales (que facultan exigir del Estado acciones que permitan a las personas satisfacer sus necesidades básicas como seres humanos).",
    3: "Deberes y responsabilidades: Para que los derechos se cumplan efectivamente, es necesario que vayan acompañados de deberes y responsabilidades. Los deberes que se establecen para las personas que viven dentro de un país y que son imprescindibles para alcanzar el bien común. Por su parte, las responsabilidades alcanzan a aquellas obligaciones que la Constitución dispone específicamente a los poderes públicos (responsabilidad política, civil, administrativa o penal).",
    4: "Instituciones del Estado: Las Instituciones son el conjunto de entidades, órganos, autoridades y procedimientos establecidos por la Constitución y que tienen como propósito permitir el correcto funcionamiento del Estado, propender al bien común, buscar que se alcancen los valores constitucionales y dar satisfacción y protección a los derechos fundamentales."
}


NOMBRES_TAXONOMIA = {
    1: "valores",
    2: "derechos",
    3: "deberes",
    4: "instituciones"
}

def exportar_json_a_excel(archivo_json, archivo_excel, sobrescribir=False):
    """
    Convierte un archivo JSON (lista de dicts) a Excel para revisión manual.
    """

    if os.path.exists(archivo_excel) and not sobrescribir:
        confirm = input(f"El archivo {archivo_excel} ya existe. ¿Deseas sobrescribirlo? [s/N]: ").strip().lower()
        if confirm != "s":
            print("❌ Exportación cancelada.")
            return

    # Leer JSON
    with open(archivo_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("El JSON debe ser una lista de objetos/diccionarios.")

    # Convertir a DataFrame
    df = pd.json_normalize(data)

    # Columnas recomendadas (ajusta según tu salida real)
    columnas_preferidas = [
        "id_taxonomia", "pregunta", "id_cabildo",
        "tipo_eleccion", "tipo_cabildo",
        "otro", "fundamento",
        "id_categoria", "categoria", "fundamento_aporta"
    ]

    # Agregar columnas que existan primero (en orden), y luego el resto
    cols_existentes = [c for c in columnas_preferidas if c in df.columns]
    cols_restantes = [c for c in df.columns if c not in cols_existentes]
    df = df[cols_existentes + cols_restantes]

    # Guardar Excel
    df.to_excel(archivo_excel, index=False)
    print(f"✅ Exportación completada: {archivo_excel}")

def convertir_archivos_excel_a_json(directorio, columnas_validas, sobrescribir=False):
    for nombre_archivo in os.listdir(directorio):
        if nombre_archivo.endswith(".xlsx"):
            ruta_excel = os.path.join(directorio, nombre_archivo)
            nombre_sin_extension = os.path.splitext(nombre_archivo)[0]
            ruta_json = os.path.join(directorio, f"{nombre_sin_extension}.json")
            if os.path.exists(ruta_json) and not sobrescribir:
                confirm = input(f"El archivo {ruta_json} ya existe. ¿Deseas sobrescribirlo? [s/N]: ").lower()
                if confirm != "s":
                    print(f"❌ Operación cancelada. No se sobrescribió {ruta_json}")
                    return
            try:
                df = pd.read_excel(ruta_excel)
                for columna_valida in columnas_validas:
                    if columna_valida not in df.columns:
                        print(f"⚠️  '{nombre_archivo}' no contiene columnas válidas.")
                        continue
                df = df.dropna(how="all")
                data_json = df[columnas_validas].to_dict(orient="records")
                with open(ruta_json, "w", encoding="utf-8") as f:
                    json.dump(data_json, f, ensure_ascii=False, indent=2)
                print(f"✅ Convertido: {nombre_archivo} → {nombre_sin_extension}.json")
            except Exception as e:
                print(f"❌ Error procesando '{nombre_archivo}': {e}")

# Convertir taxonomías en Excel a JSON
def convertir_taxonomias_excel_a_json(directorio,sobrescribir=False):
    columnas_validas = ["id_categoria", "Categoría"]
    convertir_archivos_excel_a_json(directorio, columnas_validas, sobrescribir)

def convertir_datos_excel_a_json(directorio,sobrescribir=False):
    columnas_validas = ["id_taxonomia","id_cabildo","otro","fundamento","tipo_eleccion","tipo_cabildo"]
    convertir_archivos_excel_a_json(directorio, columnas_validas, sobrescribir)

def registrar_log(texto, fundamento, respuesta_raw):
    with open(LOG_RESPUESTAS, "a", encoding="utf-8") as log:
        log.write("=== ENTRADA ===\n")
        log.write(f"Texto libre: {texto}\n")
        log.write(f"Fundamento: {fundamento}\n")
        log.write("=== RESPUESTA MODELO ===\n")
        log.write(f"{respuesta_raw}\n\n")


def registrar_error(texto, fundamento, error):
    with open(LOG_ERRORES, "a", encoding="utf-8") as log:
        log.write("=== ERROR ===\n")
        log.write(f"Texto libre: {texto}\n")
        log.write(f"Fundamento: {fundamento}\n")
        log.write(f"Error: {str(error)}\n\n")


def cargar_taxonomia_por_id(directorio, id_taxonomia):
    nombre = NOMBRES_TAXONOMIA.get(id_taxonomia)
    ruta = os.path.join(directorio, f"{nombre}.json")
    with open(ruta, 'r', encoding='utf-8') as file:
        return json.load(file)


def extraer_json(texto):
    match = re.search(r"\{.*\}", texto, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    raise ValueError("No se encontró JSON válido en la respuesta del modelo.")


class ClasificadorOpenAI:
    def __init__(self, directorio_taxonomias, modelo="gpt-4.1-mini"):
        self.directorio_taxonomias = directorio_taxonomias
        self.modelo = modelo
        self.max_reintentos = 5
        self.resultados = []
        self.estadisticas_por_pregunta = defaultdict(list)
        self.errores_por_pregunta = defaultdict(int)
        self.exitos_por_pregunta = defaultdict(int)

    def construir_prompt_usuario(self, texto, fundamento, id_taxonomia):
        taxonomia = cargar_taxonomia_por_id(self.directorio_taxonomias, id_taxonomia)
        definicion = DEFINICIONES_TAXONOMIA.get(id_taxonomia, "")
        categorias = "\n".join([f"{x['id categoria']}: {x['Categoría']}" for x in taxonomia])
        entrada = f"""
Texto libre: {texto}
Fundamento: {fundamento}

Definición de la categoría general: {definicion}

Categorías específicas:
{categorias}
"""
        return entrada

    def clasificar_entrada(self, fila):
        texto = fila.get("otro", "")
        fundamento = fila.get("fundamento", "")
        id_taxonomia = int(fila.get("id_taxonomia", 0))
        if id_taxonomia in [1,2,3,4]:
            pregunta = NOMBRES_TAXONOMIA[id_taxonomia]
        else:
            pregunta = "desconocida"

        prompt_usuario = self.construir_prompt_usuario(texto, fundamento, id_taxonomia)

        for intento in range(self.max_reintentos):
            try:
                inicio = time.time()
                respuesta = client.chat.completions.create(
                    model=self.modelo,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt_usuario}
                    ],
                    temperature=0
                )
                fin = time.time()
                duracion = fin - inicio
                mensaje = respuesta.choices[0].message.content
                registrar_log(texto, fundamento, mensaje)
                if not mensaje:
                    raise ValueError("La respuesta del modelo está vacía.")
                salida = extraer_json(mensaje.strip())
                salida.update({
                    "id_cabildo": fila.get("id_cabildo", None),
                    "tipo_cabildo": fila.get("tipo_cabildo", None),
                    "tipo_eleccion": fila.get("tipo_eleccion", None),
                    "otro": texto,
                    "fundamento": fundamento,
                    "pregunta": pregunta,
                    "id_taxonomia": id_taxonomia,
                    "duracion": duracion
                })
                #self.resultados.append(salida)
                self.estadisticas_por_pregunta[pregunta].append(duracion)
                self.exitos_por_pregunta[pregunta] += 1
                return salida
            except openai.RateLimitError as e:
                if "insufficient_quota" in str(e):
                    registrar_error(texto, fundamento, "CUOTA AGOTADA - ejecución detenida")
                    print("🚨 CUOTA AGOTADA. Deteniendo ejecución para evitar bloqueo.")
                    self.guardar_resultados_temporal()
                    raise SystemExit("Cuota OpenAI agotada")
                else:
                    time.sleep(2 ** intento)
            except openai.error.RateLimitError:
                time.sleep(2 ** intento)
            except Exception as e:
                registrar_error(texto, fundamento, e)
                self.errores_por_pregunta[pregunta] += 1
                time.sleep(2 ** intento)

        return {
            "id_categoria": None,
            "categoria": None,
            "fundamento_aporta": None,
            "id_cabildo": fila.get("id_cabildo", None),
            "tipo_cabildo": fila.get("tipo_cabildo", None),
            "tipo_eleccion": fila.get("tipo_eleccion", None),
            "otro": texto,
            "fundamento": fundamento,
            "pregunta": pregunta,
            "id_taxonomia": id_taxonomia,
            "duracion": duracion
        }

    def guardar_resultados_temporal(self):
        """
        Guardado atómico con backup.
        Escribe primero en un .tmp, respalda el progreso anterior como .bak y luego reemplaza de forma atómica.
        Evita corrupción del archivo si hay interrupciones durante la escritura.
        """
        import shutil

        tmp_path = PROGRESO_PATH + ".tmp"
        bak_path = PROGRESO_PATH + ".bak"

        try:
            # 1) Escribir primero en archivo temporal
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.resultados, f, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())  # fuerza escritura a disco

            # 2) Respaldo del progreso anterior (si existe)
            if os.path.exists(PROGRESO_PATH):
                shutil.copy2(PROGRESO_PATH, bak_path)

            # 3) Reemplazo atómico (seguro en Windows)
            os.replace(tmp_path, PROGRESO_PATH)

        except Exception as e:
            print(f"❌ Error al guardar progreso atómico: {e}")

    def cargar_progreso(self):
        """
        Carga progreso desde PROGRESO_PATH.
        Si el archivo principal está corrupto, intenta cargar el backup (.bak).
        """
        bak_path = PROGRESO_PATH + ".bak"

        if not os.path.exists(PROGRESO_PATH):
            return []

        try:
            with open(PROGRESO_PATH, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception:
            if os.path.exists(bak_path):
                print("⚠️ Progreso principal corrupto. Cargando backup...")
                try:
                    with open(bak_path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception as e:
                    print(f"❌ Error al cargar backup: {e}")

        print("❌ No se pudo cargar progreso ni backup.")
        return []

    def procesar_json(self, archivo_json, max_workers=3, guardar_cada=50):
        with open(archivo_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        self.resultados = self.cargar_progreso()

        # ✅ Clave única correcta: (id_taxonomia, id_cabildo, otro)
        procesados_keys = {
            (r.get("id_taxonomia"), r.get("id_cabildo"), r.get("otro"))
            for r in self.resultados
            if r.get("id_cabildo") is not None
        }

        datos_restantes = [
            fila for fila in datos
            if (fila.get("id_taxonomia"), fila.get("id_cabildo"), fila.get("otro")) not in procesados_keys
        ]

        print(f"📌 Entradas totales: {len(datos)}")
        print(f"✅ Ya procesadas (según progreso): {len(self.resultados)}")
        print(f"⏳ Restantes por procesar: {len(datos_restantes)}")

        buffer_resultados = []
        contador = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futuras = [executor.submit(self.clasificar_entrada, fila) for fila in datos_restantes]

            for future in tqdm(as_completed(futuras), total=len(futuras), desc="Procesando", ncols=80):
                resultado = future.result()
                buffer_resultados.append(resultado)
                contador += 1

                # Guardar cada N iteraciones
                if contador % guardar_cada == 0:
                    self.resultados.extend(buffer_resultados)
                    buffer_resultados.clear()
                    self.guardar_resultados_temporal()
                    print(f"💾 Guardado parcial: {contador} nuevos resultados")

        # Guardar lo último pendiente
        if buffer_resultados:
            self.resultados.extend(buffer_resultados)
            self.guardar_resultados_temporal()
            print(f"💾 Guardado final: {len(buffer_resultados)} nuevos resultados")

        return self.resultados

    def imprimir_resumen(self, directorio):
        resumen_txt = []
        resumen_txt.append("=== RESUMEN DEL PROCESAMIENTO POR PREGUNTA ===")
        resumen_txt.append(f"Modelo utilizado: {self.modelo}")

        for pregunta in sorted(set(self.exitos_por_pregunta) | set(self.errores_por_pregunta)):
            total = self.exitos_por_pregunta.get(pregunta, 0) + self.errores_por_pregunta.get(pregunta, 0)
            resumen_txt.append(f"\n📌 Pregunta: {pregunta}")
            resumen_txt.append(f"  Total procesado: {total}")
            resumen_txt.append(f"  ✔ Éxitos: {self.exitos_por_pregunta.get(pregunta, 0)}")
            resumen_txt.append(f"  ❌ Errores: {self.errores_por_pregunta.get(pregunta, 0)}")

            print(f"\n📌 Pregunta: {pregunta}")
            print(f"  Total procesado: {total}")
            print(f"  ✔ Éxitos: {self.exitos_por_pregunta.get(pregunta, 0)}")
            print(f"  ❌ Errores: {self.errores_por_pregunta.get(pregunta, 0)}")

            if self.estadisticas_por_pregunta[pregunta]:
                tiempos = self.estadisticas_por_pregunta[pregunta]
                promedio = sum(tiempos) / len(tiempos)

                resumen_txt.append(f"  ⏱ Tiempo promedio por entrada: {promedio:.2f} segundos")
                print(f"  ⏱ Tiempo promedio por entrada: {promedio:.2f} segundos")

                plt.hist(tiempos, bins=20, color='skyblue', edgecolor='black')
                plt.title(f"Distribución de tiempos - Pregunta: {pregunta}")
                plt.xlabel("Segundos por entrada")
                plt.ylabel("Frecuencia")
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.tight_layout()

                archivo_histograma = os.path.join(directorio, f"tiempos_pregunta_{pregunta}.png")
                plt.savefig(archivo_histograma)
                plt.clf()

                resumen_txt.append(f"  📊 Histograma guardado como '{archivo_histograma}'")
                print(f"  📊 Histograma guardado como '{archivo_histograma}'")

        # Guardar resumen en archivo de texto
        archivo_resumen = os.path.join(directorio, "resumen_procesamiento.txt")
        try:
            with open(archivo_resumen, "w", encoding="utf-8") as f:
                f.write("\n".join(resumen_txt))
            print(f"\n📝 Resumen guardado como '{archivo_resumen}'")
        except Exception as e:
            print(f"❌ Error al guardar resumen: {e}")

def main():
    parser = argparse.ArgumentParser(description="Clasificador OpenAI para respuestas ciudadanas")
    parser.add_argument("modo", choices=["preparar", "exportar_excel", "muestra", "completo", "histograma"], help="Modo de ejecución")
    parser.add_argument("--taxonomias", help="Ruta a directorio de archivos Excel o JSON con taxonomías")
    parser.add_argument("--datos_entrada", help="Archivo JSON con respuestas a clasificar")
    parser.add_argument("--datos_salida", help="Archivo JSON donde guardar resultados clasificados")
    parser.add_argument("--progreso", help="Archivo JSON para guardar progreso temporal")
    parser.add_argument("--sobrescribir", action="store_true", help="Sobrescribir archivo existente")
    parser.add_argument("--entrada_json", help="Archivo JSON de entrada")
    parser.add_argument("--entrada_excel", help="Archivo Excel de entrada")
    parser.add_argument("--salida_excel", help="Archivo Excel (.xlsx) de salida")
    parser.add_argument("--salida_histograma", default="histograma_duracion_general.png", help="Archivo PNG de salida")
    parser.add_argument("--bins", type=int, default=30, help="Cantidad de bins del histograma")
    parser.add_argument("--mostrar", action="store_true", help="Mostrar histograma en pantalla")
    parser.add_argument("--guardar_cada", type=int, default=50, help="Guardar progreso cada N iteraciones")

    args = parser.parse_args()

    global PROGRESO_PATH
    if args.progreso:
        PROGRESO_PATH = args.progreso

    if args.modo == "preparar":
        if not args.taxonomias and not args.datos_entrada:
            print("Debes indicar --taxonomias o --datos_entrada con el directorio de Excel.")
            return
        if args.taxonomias:
            convertir_taxonomias_excel_a_json(args.taxonomias,sobrescribir=args.sobrescribir)

        if args.datos_entrada:
            convertir_datos_excel_a_json(args.datos_entrada,sobrescribir=args.sobrescribir)

    elif args.modo in ["muestra", "completo"]:
        if not all([args.taxonomias, args.datos_entrada, args.datos_salida]):
            print("Debes indicar --taxonomias, --datos_entrada y --datos_salida")
            return
        directorio = os.path.dirname(args.datos_salida)
        global LOG_RESPUESTAS
        global LOG_ERRORES
        global LOG_RESPUESTAS
        LOG_RESPUESTAS = os.path.join(directorio, LOG_RESPUESTAS)
        LOG_ERRORES = os.path.join(directorio, LOG_ERRORES)
        PROGRESO_PATH = os.path.join(directorio, PROGRESO_PATH)

        clasificador = ClasificadorOpenAI(args.taxonomias)
        resultados = clasificador.procesar_json(args.datos_entrada, max_workers=3, guardar_cada=args.guardar_cada)
        with open(args.datos_salida, "w", encoding="utf-8") as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
        print(f"\nResultados guardados en '{args.datos_salida}'")
        print(f"Trazabilidad registrada en '{LOG_RESPUESTAS}' y errores en '{LOG_ERRORES}'")
        clasificador.imprimir_resumen(directorio)
    elif args.modo == "exportar_excel":
        exportar_json_a_excel(
            archivo_json=args.entrada_json,
            archivo_excel=args.salida_excel,
            sobrescribir=args.sobrescribir
        )
    elif args.modo == "histograma":
        if args.entrada_json or args.entrada_excel:
            if args.entrada_json:
                if not os.path.exists(args.entrada_json):
                    print(f"❌ No se encontró el archivo de entrada: {args.entrada_json}")
                    return
                duraciones, faltantes, invalidas = cargar_duraciones(args.entrada_json)
            else:
                if not os.path.exists(args.entrada_excel):
                    print(f"❌ No se encontró el archivo de entrada: {args.entrada_excel}")
                    return
                duraciones, faltantes, invalidas = cargar_duraciones_excel(args.entrada_excel)

            if duraciones:
                imprimir_estadisticas(duraciones, faltantes, invalidas)

                generar_histograma(
                    duraciones=duraciones,
                    salida_png=args.salida_histograma,
                    bins=args.bins,
                    mostrar=args.mostrar,
                    titulo="Distribución general de duración por iteración (OpenAI)"
                )
            else:
                print("❌ No se encontraron valores válidos en la llave 'duracion'.")

def cargar_duraciones(path_json):
    """
    Carga un archivo JSON (lista de dicts) y extrae el campo 'duracion'
    si existe y es numérico.
    """

    duraciones = []
    faltantes = 0
    invalidas = 0

    with open(path_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, reg in enumerate(data):
        if "duracion" not in reg:
            faltantes += 1
            continue

        val = reg["duracion"]
        try:
            val = float(val)
            if val >= 0:
                duraciones.append(val)
            else:
                invalidas += 1
        except Exception:
            invalidas += 1

    return duraciones, faltantes, invalidas

def cargar_duraciones_excel(path_excel, columna="duracion"):
    """
    Carga un archivo Excel y extrae la columna 'duracion' si existe
    y es numérica (o convertible a float).

    Retorna:
        duraciones (list[float])
        faltantes (int) -> registros sin columna o sin valor
        invalidas (int) -> valores no convertibles o negativos
    """

    duraciones = []
    faltantes = 0
    invalidas = 0

    df = pd.read_excel(path_excel)

    if columna not in df.columns:
        print(f"⚠️ La columna '{columna}' no existe en el archivo.")
        return [], len(df), 0

    for i, val in enumerate(df[columna]):
        if pd.isna(val):
            faltantes += 1
            continue

        try:
            val = float(val)
            if val >= 0:
                duraciones.append(val)
            else:
                invalidas += 1
        except Exception:
            invalidas += 1

    return duraciones, faltantes, invalidas

def imprimir_estadisticas(duraciones, faltantes, invalidas):
    arr = np.array(duraciones)
    print("\n=== ESTADÍSTICAS GENERALES DE DURACIÓN ===")
    print(f"Total registros leídos: {len(duraciones) + faltantes + invalidas}")
    print(f"Duraciones válidas: {len(duraciones)}")
    print(f"Duraciones faltantes: {faltantes}")
    print(f"Duraciones inválidas: {invalidas}")
    print(f"Promedio: {arr.mean():.3f} s")
    print(f"Mediana (p50): {np.percentile(arr, 50):.3f} s")
    print(f"p90: {np.percentile(arr, 90):.3f} s")
    print(f"p95: {np.percentile(arr, 95):.3f} s")
    print(f"p99: {np.percentile(arr, 99):.3f} s")
    print(f"Mínimo: {arr.min():.3f} s")
    print(f"Máximo: {arr.max():.3f} s")

def generar_histograma(duraciones, salida_png, bins=30, mostrar=False, titulo=None):
    if not duraciones:
        print("❌ No hay duraciones válidas para graficar.")
        return

    plt.figure(figsize=(10, 6))
    plt.hist(duraciones, bins=bins, edgecolor='black')
    plt.xlabel("Segundos por iteración")
    plt.ylabel("Frecuencia")

    if titulo:
        plt.title(titulo)
    else:
        plt.title("Distribución general de tiempos de ejecución (duración)")

    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Guardar figura
    plt.savefig(salida_png)
    print(f"\n📊 Histograma guardado en: {salida_png}")

    if mostrar:
        plt.show()

    plt.close()

if __name__ == "__main__":
    SYSTEM_PROMPT = """
Eres un asistente experto en categorizar ideas ciudadanas dentro de una taxonomía constitucional. 
Dado un texto libre y su fundamento, debes:
1. Asignar la categoría más adecuada de la lista proporcionada.
2. Indicar si el fundamento aporta o no a la clasificación.
Responde siempre con un JSON que tenga las siguientes claves:
- id_categoria
- categoria
- fundamento_aporta (true/false)
"""
    main()
