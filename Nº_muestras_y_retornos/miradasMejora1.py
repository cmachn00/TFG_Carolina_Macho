#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 12:18:41 2025

@author: carolinamachonieto
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from io import StringIO

# ------------------------------
# Áreas de interés en coordenadas absolutas
# ------------------------------
AOIS = { 
    "Area1": (0, 0, 1920, 302),
    "Area2": (0, 302, 1920, 937),
    "Area3": (0, 937, 1920, 1080)
}

# ------------------------------
# Cargar CSV hasta encontrar fin_pagina
# ------------------------------
csv_file = "/Users/carolinamachonieto/Desktop/TFG/excel/gaze_datos_completo_oscar.csv"

# leer cabecera
with open(csv_file, encoding="latin1") as f:
    header = f.readline()

# leer línea a línea hasta encontrar fin_pagina
lines = []
line_number = 2  # porque empiezas desde línea 2 (contando desde 1)
with open(csv_file, encoding="latin1") as f:
    next(f)  # saltar cabecera
    for line in f:
        first_column = line.split(",")[0].strip().lower()
        if first_column.startswith("fin_pagina"):
            print(f"Se detectó fin_pagina en la línea {line_number} del archivo.")
            break
        lines.append(line)
        line_number += 1

print(f"Se han leído desde la línea 2 hasta la línea {line_number - 1} del archivo.")


# concatenar cabecera + líneas válidas
data_str = header + "".join(lines)

# pasar a pandas
df = pd.read_csv(StringIO(data_str), encoding="latin1")

# ------------------------------
# Preprocesamiento
# ------------------------------
df = df.dropna(subset=["Left Eye X", "Left Eye Y", "Right Eye X", "Right Eye Y"])

# convertir a píxeles
df["x"] = ((df["Left Eye X"] + df["Right Eye X"]) / 2 * 1920)
df["y"] = ((df["Left Eye Y"] + df["Right Eye Y"]) / 2 * 1080)
df["y"] = 1080 - df["y"]  # invertir eje Y

# tiempo
df["Timestamp"] = df["Timestamp device"] / 1000.0
t0 = df["Timestamp"].min()

# ------------------------------
# Conteo muestras y retornos
# ------------------------------
for area, (x1,y1,x2,y2) in AOIS.items():
    dentro = df[(df["x"] >= x1) & (df["x"] <= x2) & (df["y"] >= y1) & (df["y"] <= y2)]
    muestras = len(dentro)
    
    todos = df.copy()
    todos["in_aoi"] = (todos["x"] >= x1) & (todos["x"] <= x2) & (df["y"] >= y1) & (df["y"] <= y2)
    retornos = todos["in_aoi"].astype(int).diff().fillna(0)
    n_retornos = (retornos == 1).sum()
    
    print(f"\nResultados para {area}:")
    print(f"- Número total de muestras (mínima mirada): {muestras}")
    print(f"- Número de retornos: {n_retornos}")

# ------------------------------
# Visualización
# ------------------------------
screen_width, screen_height = 1920, 1080
img_file = "/Users/carolinamachonieto/Desktop/TFG/PaginaWeb1.png"

img = mpimg.imread(img_file)

fig, ax = plt.subplots(figsize=(12,7))
ax.imshow(img, extent=[0,screen_width,screen_height,0])

colors = {
    "Area1": 'magenta',
    "Area2": 'blue',
    "Area3": 'green'
}

for area, (x1, y1, x2, y2) in AOIS.items():
    rect = patches.Rectangle(
        (x1, y1),
        (x2 - x1),
        (y2 - y1),
        linewidth=2,
        edgecolor='black',
        facecolor=colors[area],
        alpha=0.3,
        label=area
    )
    ax.add_patch(rect)

ax.set_xlim(0, screen_width)
ax.set_ylim(screen_height, 0)
ax.set_title("Visualización de áreas de interés ajustadas y no solapadas")
plt.legend()
plt.show()
