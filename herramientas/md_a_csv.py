"""Convierte un 04-PROMPTS.md (formato Goods Uncovered) en un CSV para generar_imagenes.py.

Uso:
    python herramientas/md_a_csv.py videos-largos/001-el-nino-2026/04-PROMPTS.md prompts.csv

Toma cada bloque así:
    ### 01 · Título
    `id-de-la-imagen`
    ```
    prompt completo...
    ```
El prompt ya trae estilo y "No text…", por eso la columna estilo sale en 0.
Si el prompt dice 9:16 el formato sale 9:16; si no, 16:9.
"""
import csv
import re
import sys

if len(sys.argv) != 3:
    sys.exit("Uso: python herramientas/md_a_csv.py 04-PROMPTS.md salida.csv")

texto = open(sys.argv[1], encoding="utf-8").read()
bloques = re.findall(r"^###[^\n]*\n`([^`\n]+)`\s*\n```\n(.*?)\n```", texto, re.S | re.M)
if not bloques:
    sys.exit("No encontré bloques '### … / `id` / ```prompt```' en el archivo.")

with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "prompt", "estilo", "formato"])
    vistos, saltados = set(), []
    for id_, prompt in bloques:
        id_ = id_.strip()
        if id_ in vistos:  # la sección de videos repite el id de la imagen: solo va la imagen
            saltados.append(id_)
            continue
        vistos.add(id_)
        prompt = " ".join(prompt.split())
        w.writerow([id_, prompt, "0", "9:16" if "9:16" in prompt else "16:9"])
print(f"{len(vistos)} prompts de imagen → {sys.argv[2]}")
if saltados:
    print(f"Saltados (prompts de video con el mismo id): {', '.join(saltados)}")
