

# Zillow Puerto Rico Scraper

## Objetivo

Desarrollar un scraper que extraiga todos los anuncios de propiedades listadas en Puerto Rico en Zillow (https://www.zillow.com/pr/) al momento de la ejecución.

El scraper debe poder pausarse y retomarse sin pérdida de progreso.

---

## Demo


[![Ver demo en YouTube](https://img.youtube.com/vi/pZ78jvGnTcA/0.jpg)](https://youtu.be/pZ78jvGnTcA)


---

## Alcance

- Extrae información estructurada de cada anuncio.
- Maneja obstáculos como CAPTCHAs y detección de bots.
- Ejecuta de forma local.
- Almacena los datos en formato estructurado (simula un data lake en JSON, puede adaptarse a PostgreSQL o MinIO fácilmente).

---

## Estructura del proyecto

```
zillow_scraper/
├── main.py
├── config.py
├── data/
│   └── resultados.json
├── assets/
│   ├── boton.png
│   └── boton_done.png
├── core/
│   ├── controller.py
│   ├── driver.py
│   ├── parser.py
│   └── storage.py
└── utils/
    ├── visual.py
    └── helpers.py
```

---

## Proceso seguido

### 1. **Primer intento: extracción directa por URL**
Se intentó obtener los datos accediendo directamente a endpoints internos. En ocasiones funcionaba, pero era inconsistente y fallaba al cargar completamente. Esto sugiere que Zillow utiliza **server-side rendering con protección anti-bot**, impidiendo acceder a los datos completos mediante `requests`

### 2. **Segundo intento: interceptar respuestas del frontend**
Se intentó identificar las llamadas AJAX del sitio usando herramientas como las DevTools. Sin embargo, las URLs no eran públicas o estaban firmadas temporalmente, por lo que tampoco fue viable, solo estaban las de google ads

![image](https://github.com/user-attachments/assets/41bd65af-871c-4285-82da-0f97b67fda3e)

### 3. **Solución implementada: scraping con renderizado y visión artificial**
Se optó por usar `undetected-chromedriver` junto con Selenium para abrir la página como un navegador humano. Sin embargo, incluso con `headless=False` y navegadores configurados, Zillow detectaba automatización y presentaba un CAPTCHA personalizado.

Este CAPTCHA consistía en:
- Un botón que debía presionarse con el mouse.
- El tiempo de presión debía ser **exacto**. Si se presionaba por poco tiempo, mucho tiempo o se soltaba en el momento incorrecto, se bloqueaba el acceso.
- En algunos casos, el CAPTCHA se repetía varias veces si no se resolvía a tiempo (en menos de 30 segundos).

![image](https://github.com/user-attachments/assets/114dccd1-56d9-4df4-a4d8-407ac968f667)

Se usaron técnicas de visión por computadora (`opencv`) y simulación humana (`pyautogui`) para:
- Detectar el botón en pantalla (por imagen).
- Presionar el botón durante un tiempo variable hasta que apareciera una señal visual (otra imagen).
- Repetir el proceso si era necesario.

Si no aparecía el CAPTCHA en los primeros 15 segundos, se asumía que no era requerido y se continuaba.

---

## Campos extraídos por anuncio

- `@type`
- `address` (estructura completa: calle, ciudad, estado, código postal)
- `offers.price`
- `url`
- `geo.latitude`, `geo.longitude`
- `url_origen` (página desde la que se extrajo el dato)

Se guarda el JSON completo del bloque `ld+json` de tipo `SingleFamilyResidence`, por lo que se almacenan todos los campos disponibles directamente desde Zillow.

---

## Reanudación y persistencia

El archivo `data/resultados.json` almacena todos los anuncios extraídos. El proceso se puede pausar y continuar automáticamente sin repetir páginas ya procesadas gracias al campo `"url_origen"`.

---

## Ejecución

1. Clona el repositorio.
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Asegúrate de tener las imágenes `boton.png` y `boton_done.png` en la carpeta `assets/`.
4. Ejecuta el scraper:
   ```bash
   python main.py
   ```

---

## Dependencias 

Es preferible usar Python 3.10 o 3.11. Python 3.13 puede generar incompatibilidades con algunas librerías visuales.

---

## Manejo de errores

- Se ignoran páginas que ya fueron procesadas.
- Se manejan archivos corruptos o vacíos en `resultados.json`.
- Se hace logging por consola paso a paso.
- Si el botón no aparece en pantalla, el script espera y asume que no hubo CAPTCHA.
