import pyautogui
import cv2
import numpy as np
import time
import random

def encontrar_en_pantalla(template_img, threshold):
    screenshot = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(screen, template_img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        h, w = template_img.shape[:2]
        return True, (max_loc[0] + w // 2, max_loc[1] + h // 2), max_val
    return False, (0, 0), max_val

def generar_offset_aleatorio(rango=10):
    return (
        random.randint(-rango, rango),
        random.randint(-rango, rango)
    )

def mover_cursor_lento(x, y, duracion=0.5):
    pyautogui.moveTo(x, y, duration=duracion)

def buscar_y_presionar_boton(template_path, threshold=0.90, boton_done_path="assets/boton_done.png"):
    print(">> Iniciando búsqueda del botón")

    template = cv2.imread(template_path)
    template_done = cv2.imread(boton_done_path)

    if template is None:
        print(">> Imagen del botón no encontrada:", template_path)
        return
    if template_done is None:
        print(">> Imagen del botón done no encontrada:", boton_done_path)
        return

    start_search = time.time()
    while True:
        if time.time() - start_search > 15:
            print(">> No se detectó captcha en 15 segundos. Asumiendo acceso libre. Continuando")
            return

        encontrado, centro, val = encontrar_en_pantalla(template, threshold)
        if encontrado:
            print(f">> Botón detectado con {val * 100:.2f}% de precisión en {centro}")

            offset_click = generar_offset_aleatorio(10)
            centro_con_delta = (centro[0] + offset_click[0], centro[1] + offset_click[1])

            mover_cursor_lento(*centro_con_delta)
            time.sleep(1)
            pyautogui.mouseDown()
            print(">> Clic presionado. Buscando done por máximo 20 segundos")

            start_hold = time.time()
            while time.time() - start_hold < 20:
                time.sleep(1)
                done_encontrado, _, val_done = encontrar_en_pantalla(template_done, threshold)
                if done_encontrado:
                    print(f">> Botón done detectado con {val_done * 100:.2f}% de precisión.")
                    time.sleep(0.5)
                    pyautogui.mouseUp()
                    print(">> Clic liberado")

                    offset_grande = (
                        centro[0] + random.choice([-1, 1]) * random.randint(90, 110),
                        centro[1] + random.choice([-1, 1]) * random.randint(90, 110)
                    )

                    mover_cursor_lento(*offset_grande)
                    pyautogui.click()
                    print(f">> Clic adicional aleatorio en {offset_grande}")

                    print(">> Buscando de nuevo el botón original por 5 segundos")
                    start_retry = time.time()
                    while time.time() - start_retry < 5:
                        time.sleep(1)
                        nuevamente, _, val_nuevo = encontrar_en_pantalla(template, threshold)
                        if nuevamente:
                            print(f">> Botón encontrado nuevamente con {val_nuevo * 100:.2f}%. Reiniciando ciclo.")
                            break
                    else:
                        print(">> Botón no reapareció. Finalizando proceso.")
                        return
                    break
            else:
                print(">> Tiempo máximo alcanzado sin detectar botón done. Liberando clic y saliendo.")
                pyautogui.mouseUp()
                return
        else:
            print(">> Botón aún no detectado. Reintentando")
            time.sleep(1)
