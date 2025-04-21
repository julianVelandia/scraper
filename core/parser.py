from bs4 import BeautifulSoup
import json

def extraer_propiedades(html, url):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script", {"type": "application/ld+json"})
    propiedades = []

    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get("@type") == "SingleFamilyResidence":
                data["url_origen"] = url
                propiedades.append(data)
        except json.JSONDecodeError:
            continue
    return propiedades
