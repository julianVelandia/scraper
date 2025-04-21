import time
from datetime import datetime

def timestamp_log():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def retry(func, times=3, delay=2):
    for i in range(times):
        try:
            return func()
        except Exception as e:
            print(f"{timestamp_log()} Intento {i+1} fallido: {e}")
            time.sleep(delay)
    raise Exception(f"{timestamp_log()} Todos los intentos fallaron.")

def limpiar_texto(texto):
    return texto.strip().replace("\n", " ").replace("\r", "")
