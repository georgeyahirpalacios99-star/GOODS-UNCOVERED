"""Genera imágenes en lote con la API de Google GenAI a partir de un CSV de prompts.

Uso:
    pip install google-genai
    export GEMINI_API_KEY="tu_clave"            # https://aistudio.google.com/apikey
    python herramientas/generar_imagenes.py prompts.csv --salida videos-largos/002-tema/imagenes

CSV (cabecera obligatoria; solo `id` y `prompt` son obligatorias):
    id,prompt,estilo,formato
    lluvia-charco,"Close-up of raindrops hitting a puddle at night",A,16:9
    archivo-1998,"People wading through floodwater in a coastal town",B,

- `id`: nombre del archivo de salida (sin extensión). Es el mismo nombre que usa video.json.
- `estilo`: A, B, C o D (los mismos bloques del agente de Flow). Vacío = A.
  0 = el prompt ya trae su estilo completo (así salen los CSV de `md_a_csv.py`).
- `formato`: 16:9, 9:16, 1:1, 4:3 o 3:4. Vacío = el de --formato.

Si un archivo ya existe se salta, así que se puede cortar y volver a correr sin repetir gastos.
Al final escribe `_registro.csv` con el resultado de cada fila.
"""
import argparse
import csv
import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types

ESTILOS = {
    "A": "Cinematic documentary photograph, realistic, muted teal and navy color grade, soft natural light, subtle film grain, shot on 35mm.",
    "B": "Black and white archival press photograph from the late 1990s, grainy, documentary.",
    "C": "Black and white photograph from the 1940s, grainy, slightly faded, documentary.",
    "D": "Warm sepia-toned vintage photograph.",
}
SIN_TEXTO = "No text, no letters, no numbers, no logos, no watermarks."
FORMATOS = {"16:9", "9:16", "1:1", "4:3", "3:4"}


def leer_csv(ruta):
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f))
    if not filas or "id" not in filas[0] or "prompt" not in filas[0]:
        sys.exit("El CSV necesita al menos las columnas 'id' y 'prompt'.")
    ids = [r["id"].strip() for r in filas]
    repetidos = {i for i in ids if ids.count(i) > 1}
    if repetidos:
        sys.exit(f"IDs repetidos en el CSV: {', '.join(sorted(repetidos))}")
    return filas


def armar_prompt(fila):
    clave = (fila.get("estilo") or "A").strip().upper()
    if clave == "0":
        return fila["prompt"].strip()
    base = fila["prompt"].strip().rstrip(".")
    return f"{base}. {ESTILOS.get(clave, ESTILOS['A'])} {SIN_TEXTO}"


def generar_imagen(cliente, modelo, prompt, formato):
    """Devuelve los bytes de la imagen. Soporta modelos Imagen y modelos Gemini de imagen."""
    if modelo.startswith("imagen"):
        r = cliente.models.generate_images(
            model=modelo,
            prompt=prompt,
            config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio=formato),
        )
        if not r.generated_images:
            raise RuntimeError("la API no devolvió imagen (posible filtro de seguridad)")
        return r.generated_images[0].image.image_bytes
    r = cliente.models.generate_content(
        model=modelo,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio=formato),
        ),
    )
    for parte in (r.candidates[0].content.parts if r.candidates else []):
        if parte.inline_data and parte.inline_data.data:
            return parte.inline_data.data
    raise RuntimeError("la API no devolvió imagen (posible filtro de seguridad)")


def con_reintentos(fn, intentos=4):
    for i in range(intentos):
        try:
            return fn()
        except Exception as e:  # la API responde 429 o 503 cuando hay límite de uso
            msg = str(e)
            reintentable = any(c in msg for c in ("429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE", "deadline"))
            if not reintentable or i == intentos - 1:
                raise
            espera = 2 ** (i + 2)
            print(f"   límite de la API, reintento en {espera} s…")
            time.sleep(espera)


def main():
    p = argparse.ArgumentParser(description="Genera imágenes en lote desde un CSV con Google GenAI.")
    p.add_argument("csv", help="archivo CSV con columnas id,prompt[,estilo,formato]")
    p.add_argument("--salida", default="imagenes", help="carpeta donde guardar las imágenes")
    p.add_argument("--modelo", default="gemini-2.5-flash-image",
                   help="modelo de imagen: gemini-2.5-flash-image (Nano Banana) o un modelo imagen-* ")
    p.add_argument("--formato", default="16:9", choices=sorted(FORMATOS), help="formato por defecto")
    p.add_argument("--pausa", type=float, default=2.0, help="segundos entre imágenes (evita el límite de uso)")
    p.add_argument("--solo", help="generar solo estos ids, separados por coma")
    p.add_argument("--prueba", action="store_true", help="muestra lo que haría sin llamar a la API")
    a = p.parse_args()

    filas = leer_csv(a.csv)
    if a.solo:
        quiero = {x.strip() for x in a.solo.split(",")}
        filas = [f for f in filas if f["id"].strip() in quiero]
    salida = Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)

    cliente = None if a.prueba else genai.Client()  # lee GEMINI_API_KEY (o GOOGLE_API_KEY) del entorno
    registro, hechas, saltadas, fallidas = [], 0, 0, 0
    for n, fila in enumerate(filas, 1):
        id_ = fila["id"].strip()
        formato = (fila.get("formato") or a.formato).strip()
        if formato not in FORMATOS:
            formato = a.formato
        destino = salida / f"{id_}.png"
        if destino.exists():
            saltadas += 1
            registro.append({"id": id_, "estado": "ya existía", "archivo": str(destino)})
            continue
        prompt = armar_prompt(fila)
        print(f"[{n}/{len(filas)}] {id_} ({formato})")
        if a.prueba:
            print(f"   {prompt[:120]}…")
            continue
        try:
            datos = con_reintentos(lambda: generar_imagen(cliente, a.modelo, prompt, formato))
            destino.write_bytes(datos)
            hechas += 1
            registro.append({"id": id_, "estado": "ok", "archivo": str(destino)})
        except Exception as e:
            fallidas += 1
            registro.append({"id": id_, "estado": f"error: {e}"[:200], "archivo": ""})
            print(f"   error: {e}")
        time.sleep(a.pausa)

    if a.prueba:
        print(f"\nPrueba: {len(filas) - saltadas} imágenes por generar · {saltadas} ya existían. No se llamó a la API.")
        return
    with open(salida / "_registro.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "estado", "archivo"])
        w.writeheader()
        w.writerows(registro)
    print(f"\nListo: {hechas} nuevas · {saltadas} ya existían · {fallidas} con error")
    if fallidas:
        print("Vuelve a correr el mismo comando: solo intenta las que faltan.")


if __name__ == "__main__":
    main()
