#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 12:35:24 2025

@author: carolinamachonieto
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 12:31:07 2025

@author: carolinamachonieto
"""

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
    "Area1": (0, 0, 244, 1080),
    "Area2": (244, 0, 1920, 972),
    "Area3": (244, 972, 1920, 1080)
}

# ------------------------------
# Cargar CSV hasta encontrar fin_pagina
# ------------------------------
csv_file = "/Users/carolinamachonieto/Desktop/TFG/excel/gaze_datos_completo_luisPedro.csv"

# leer cabecera
with open(csv_file, encoding="latin1") as f:
    header = f.readline()

lines = []
line_number = 2
inicio_pagina_count = 0
recording = False

with open(csv_file, encoding="latin1") as f:
    next(f)  # saltar cabecera
    for line in f:
        first_column = line.split(",")[0].strip().lower()
        
        if first_column.startswith("inicio_pagina"):
            inicio_pagina_count += 1
            print(f"Detectado inicio_pagina número {inicio_pagina_count} en la línea {line_number}.")
            
            if inicio_pagina_count == 3:
                # comenzar a guardar desde la tercera aparición
                recording = True
                print(f"Comenzamos a grabar desde la línea {line_number+1}")
                continue  # no guardar la propia línea de inicio_pagina
        
        if recording:
            lines.append(line)
        
        line_number += 1

# concatenar cabecera + líneas guardadas
data_str = header + "".join(lines)

# pasar a pandas
from io import StringIO
df = pd.read_csv(StringIO(data_str), encoding="latin1")

print(f"Se han leído desde la tercera aparición de inicio_pagina hasta el final del archivo, total {len(df)} filas.")

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
img_file = "/Users/carolinamachonieto/Desktop/TFG/PaginaWeb3.jpg"

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
