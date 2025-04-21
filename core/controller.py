from core.driver import configurar_navegador
from core.parser import extraer_propiedades
from core.storage import guardar_json_append, cargar_urls_procesadas
from utils.visual import buscar_y_presionar_boton
from config import *

import time

def obtener_datos_html(url):
    driver = configurar_navegador()
    driver.get(url)
    buscar_y_presionar_boton(BOTON_PATH, threshold=THRESHOLD, boton_done_path=BOTON_DONE_PATH)
    time.sleep(10)
    contenido = driver.page_source
    driver.quit()
    return contenido

def process_url(url, archivo_salida=DATA_PATH):
    html = obtener_datos_html(url)
    propiedades = extraer_propiedades(html, url)
    guardar_json_append(propiedades, archivo_salida)
    print(f">> Se guardaron {len(propiedades)} propiedades en {archivo_salida}")

def procesar_batch_paginas(base_url="https://www.zillow.com/pr", max_paginas=100, archivo=DATA_PATH):
    urls_procesadas = cargar_urls_procesadas(archivo)
    for i in range(1, max_paginas + 1):
        url = f"{base_url}/{i}_p/"
        if url in urls_procesadas:
            print(f">> Página ya procesada: {url}. Saltando...")
            continue
        try:
            process_url(url, archivo)
        except Exception as e:
            print(f">> Error procesando {url}: {e}")
            continue
