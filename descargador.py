#!/usr/bin/env python3
"""
descargar_from_wikipedia_selenium.py

Para cada jugador en la lista:
 - abre Wikipedia
 - busca la página (usando la búsqueda interna)
 - extrae la primera imagen del infobox (si existe)
 - descarga la imagen y la guarda en ./jugadores/
 - espera aleatorio entre requests para no sobrecargar
"""

import os
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote

# ----------------------
# Config
# ----------------------
CARPETA = "jugadores"
os.makedirs(CARPETA, exist_ok=True)
REINTENTOS = 2
SLEEP_MIN = 4
SLEEP_MAX = 8
HEADLESS = True  # pon False si querés ver el navegador

# ----------------------
# Tu lista completa de jugadores (posición, nombre, país) -> usaremos solo 'nombre'
# Pega aquí tu lista completa o impórtala desde tu script.
# ----------------------
jugadores = [
     ("DC", "VIKTOR GYOKERES", "SUECIA"), ("DC", "VICTOR OSIMEH", "NIGERIA"), 
    ("DC", "MOISE KEAN", "FRANCIA"), ("DC", "ALVARO MORATA", "ESPAÑA"),
    ("DC", "TOMAS GONZALEZ", "ARGENTINA"), ("DC", "ROMELU LUKAKU", "BELGICA"),
    ("DC", "RONALDO NAZARIO", "BRASIL"), ("DC", "DIDIER DROGBA", "COSTA DE MARFIL"),
    ("DC", "ZLATAN IBRAHIMOVICH ESTADOS UNIDOS", "SUECIA"), ("DC", "KARIM BENZEMA ARABE", "FRANCIA"),
    ("DC", "ZLATAN IBRAIMOVICH PRIME", "SUECIA"), ("DC", "SAMUEL ETO´O", "CAMERUN"),
    ("DC", "KARIM BENZEMA PRIME", "FRANCIA"), ("DC", "ROBERT LEWANDOWSKI", "POLONIA"),
    ("DC", "WAYNE ROONEY", "INGLATERRA"), ("DC", "MIROSLAV KLOSE", "ALEMANIA"),
    ("DC", "SERGIO KUN AGUERO HOSPITALIZADO", "ARGENTINA"), ("DC", "SERGIO KUN AGUERO PRIME", "ARGENTINA"),
    ("DC", "ROBIN VAN PERSIE", "HOLANDA"),
]

# ----------------------
# Utiles
# ----------------------
def slugify(name: str) -> str:
    s = name.strip().lower()
    replacements = {
        " ": "_", "´":"", "’":"", "'":"", "ñ":"n",
        "á":"a","é":"e","í":"i","ó":"o","ú":"u","ü":"u",
        "/":"_", "\\":"_", ":":"", "*":"", "?":"", "\"":"", "<":"", ">":"", "|":""
    }
    for k,v in replacements.items():
        s = s.replace(k,v)
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789_-."
    s = "".join(ch for ch in s if ch in allowed)
    return s or "player"

def descargar_url(url, ruta_destino, timeout=12):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=timeout, stream=True)
        if r.status_code == 200:
            # si la ruta no tiene extensión: intentar detectar por headers
            base, ext = os.path.splitext(ruta_destino)
            if ext == "":
                ct = r.headers.get("content-type","").lower()
                if "png" in ct: ext = ".png"
                elif "webp" in ct: ext = ".webp"
                elif "gif" in ct: ext = ".gif"
                else: ext = ".jpg"
                ruta_destino = base + ext
            with open(ruta_destino, "wb") as fh:
                for chunk in r.iter_content(8192):
                    if chunk:
                        fh.write(chunk)
            return ruta_destino
    except Exception as e:
        print("  -> error descarga:", e)
    return None

# ----------------------
# Iniciar Selenium
# ----------------------
options = webdriver.ChromeOptions()
if HEADLESS:
    options.add_argument("--headless=new")
# Recomiendo algunas opciones para mayor estabilidad
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--lang=en-US")
# evadir detección basica
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_page_load_timeout(30)

# ----------------------
# Loop sobre jugadores
# ----------------------
try:
    for idx, (pos, nombre, pais) in enumerate(jugadores, start=1):
        nombre_clean = nombre.strip()
        base_filename = os.path.join(CARPETA, slugify(nombre_clean))
        # saltar si ya existe
        already = False
        for ext_try in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
            if os.path.exists(base_filename + ext_try):
                print(f"[{idx}/{len(jugadores)}] {nombre_clean} -> ya existe {base_filename + ext_try}")
                already = True
                break
        if already:
            continue

        print(f"[{idx}/{len(jugadores)}] Buscando {nombre_clean} en Wikipedia...")

        success = False
        for intento in range(1, REINTENTOS+1):
            try:
                # Intentar abrir la página directa del jugador
                search_url = f"https://en.wikipedia.org/wiki/{nombre_clean.replace(' ', '_')}"
                driver.get(search_url)
                time.sleep(2 + random.random())

                # Si la página no existe (Wikipedia muestra "Wikipedia does not have an article with this exact name.")
                if "Wikipedia does not have an article" in driver.page_source or "may refer to:" in driver.page_source:
                    # usar búsqueda
                    driver.get(f"https://en.wikipedia.org/w/index.php?search={nombre_clean.replace(' ', '+')}")
                    time.sleep(2 + random.random())

                time.sleep(2 + random.random()*1.5)

                # ahora estamos en la página (o en resultados). sacamos HTML y parseamos
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                # 2) intentar seleccionar la imagen del infobox
                infobox = soup.find("table", class_="infobox")
                img_url = None
                if infobox:
                    img_tag = infobox.find("img")
                    if img_tag and img_tag.get("src"):
                        src = img_tag["src"]
                        # URLs en Wikipedia pueden ser relativas: //upload.wikimedia...
                        if src.startswith("//"):
                            src = "https:" + src
                        elif src.startswith("/"):
                            src = urljoin("https://en.wikipedia.org", src)
                        img_url = src

                # 3) si no encontramos en 'en', intentar en 'es' (es.wikipedia)
                if not img_url:
                    # try spanish
                    driver.get("https://es.wikipedia.org/wiki/" + nombre_clean.replace(" ", "_"))
                    time.sleep(1.5 + random.random())
                    html2 = driver.page_source
                    soup2 = BeautifulSoup(html2, "html.parser")
                    infobox2 = soup2.find("table", class_="infobox")
                    if infobox2:
                        img_tag2 = infobox2.find("img")
                        if img_tag2 and img_tag2.get("src"):
                            src2 = img_tag2["src"]
                            if src2.startswith("//"):
                                src2 = "https:" + src2
                            elif src2.startswith("/"):
                                src2 = urljoin("https://es.wikipedia.org", src2)
                            img_url = src2

                # 4) si no hay img_url, intentar buscar en la página de resultados de búsqueda (fallback)
                if not img_url:
                    # buscar primer .mw-search-result img (si hay)
                    imgs = soup.select(".mw-search-result img")
                    if imgs:
                        src = imgs[0].get("src")
                        if src and src.startswith("//"):
                            src = "https:" + src
                        img_url = src

                if img_url:
                    print("  → encontrada imagen:", img_url)
                    ruta_guardada = descargar_url(img_url, base_filename)
                    if ruta_guardada:
                        print("  ✅ guardada:", ruta_guardada)
                        success = True
                        break
                    else:
                        print("  ❌ fallo guardando imagen")
                else:
                    print("  ⚠ no se encontró imagen en Wikipedia para", nombre_clean)

            except Exception as e:
                print("  ⚠ excepción en intento:", e)
            # espera entre reintentos
            wait = random.uniform(2.5, 6.0)
            print(f"  esperando {wait:.1f}s antes del siguiente intento...")
            time.sleep(wait)

        if not success:
            print(f"  ❌ No se pudo obtener imagen para {nombre_clean}. Pasando al siguiente.")

        # espera entre jugadores para no sobrecargar
        delay = random.uniform(SLEEP_MIN, SLEEP_MAX)
        print(f"⏳ Esperando {delay:.1f}s antes del siguiente jugador...\n")
        time.sleep(delay)

finally:
    driver.quit()

print("\n🏁 Proceso completado. Las imágenes están en la carpeta:", CARPETA)
