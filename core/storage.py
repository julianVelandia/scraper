import os
import json

def cargar_urls_procesadas(path):
    if not os.path.exists(path):
        return set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return {item.get("url_origen") for item in datos if "url_origen" in item}
    except:
        return set()

def guardar_json_append(datos, archivo):
    existentes = []
    if os.path.exists(archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if contenido:
                    existentes = json.loads(contenido)
        except:
            pass
    existentes.extend(datos)
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(existentes, f, indent=4, ensure_ascii=False)
