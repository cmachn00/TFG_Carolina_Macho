# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
from PIL import Image
from matplotlib import pyplot, image

# ========================
# CONFIGURACIÓN
# ========================

# Ruta al archivo CSV (ajústala si el nombre cambia)
csv_path = "C:/Users/USUARIO/Desktop/experimento_baxter/gaze_datos_completo.csv"
display_size = (1920, 1080)
alpha = 0.5
gaussianwh = 200
gaussiansd = None

# Carpeta de salida
output_folder = "C:/Users/USUARIO/Desktop/experimento_baxter/mapasCalorMemoria"
os.makedirs(output_folder, exist_ok=True)

# Imágenes de fondo
imagenes = {
    1: "C:/Users/USUARIO/Desktop/experimento_baxter/imagenes/PaginaWeb1.png",
    2: "C:/Users/USUARIO/Desktop/experimento_baxter/imagenes/PaginaWeb2.png",
    3: "C:/Users/USUARIO/Desktop/experimento_baxter/imagenes/PaginaWeb3.jpg"
}

# ========================
# FUNCIONES
# ========================

def draw_display(dispsize, imagefile=None):
    screen = np.zeros((dispsize[1], dispsize[0], 3), dtype='float32')
    if imagefile:
        if not os.path.isfile(imagefile):
            raise Exception(f"Imagen no encontrada: {imagefile}")
        img = image.imread(imagefile)
        if img.shape[2] == 4:
            img = img[:, :, :3]
        if img.dtype == np.uint8:
            img = img.astype('float32') / 255.0
        elif img.dtype in [np.float32, np.float64]:
            img = np.clip(img, 0, 1)
        img = Image.fromarray((img * 255).astype(np.uint8))
        img = img.resize(dispsize)
        img = np.asarray(img).astype('float32') / 255.0
        screen[:, :, :] = img
    dpi = 100.0
    figsize = (dispsize[0] / dpi, dispsize[1] / dpi)
    fig = pyplot.figure(figsize=figsize, dpi=dpi, frameon=False)
    ax = pyplot.Axes(fig, [0, 0, 1, 1])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.axis([0, dispsize[0], 0, dispsize[1]])
    ax.imshow(screen)
    return fig, ax

def gaussian(x, sx, y=None, sy=None):
    if y is None: y = x
    if sy is None: sy = sx
    xo, yo = x / 2, y / 2
    M = np.zeros([y, x], dtype=float)
    for i in range(x):
        for j in range(y):
            M[j, i] = np.exp(-1.0 * (((i - xo) ** 2 / (2 * sx ** 2)) + ((j - yo) ** 2 / (2 * sy ** 2))))
    return M

def draw_heatmap(gazepoints, dispsize, imagefile=None, alpha=0.5, savefilename=None, gaussianwh=200, gaussiansd=None):
    fig, ax = draw_display(dispsize, imagefile=imagefile)
    gwh = gaussianwh
    gsdwh = gwh / 6 if gaussiansd is None else gaussiansd
    gaus = gaussian(gwh, gsdwh)
    strt = gwh / 2
    heatmapsize = (int(dispsize[1] + 2 * strt), int(dispsize[0] + 2 * strt))
    heatmap = np.zeros(heatmapsize, dtype=float)
    for x, y, w in gazepoints:
        x = strt + x - int(gwh / 2)
        y = strt + y - int(gwh / 2)
        try:
            heatmap[int(y):int(y) + gwh, int(x):int(x) + gwh] += gaus * w
        except:
            continue
    heatmap = heatmap[int(strt):int(dispsize[1]) + int(strt), int(strt):int(dispsize[0]) + int(strt)]
    max_value = np.nanmax(heatmap)
    threshold = 0.15 * max_value
    heatmap[heatmap < threshold] = np.nan
    lowbound = np.nanmean(heatmap[heatmap > 0])
    heatmap[heatmap < lowbound] = np.nan
    ax.imshow(heatmap, cmap='jet', alpha=alpha)
    ax.invert_yaxis()
    if savefilename:
        fig.savefig(savefilename, dpi=100)
    return fig

# ========================
# PROCESAMIENTO
# ========================

df = pd.read_csv(csv_path, encoding="latin1")
df = df.dropna(subset=["Left Eye X", "Left Eye Y", "Right Eye X", "Right Eye Y"])
for col in ["Left Eye X", "Left Eye Y", "Right Eye X", "Right Eye Y"]:
    df[col] = df[col].astype(float)

df["x"] = ((df["Left Eye X"] + df["Right Eye X"]) / 2 * display_size[0]).astype(int)
df["y"] = ((df["Left Eye Y"] + df["Right Eye Y"]) / 2 * display_size[1]).astype(int)

for pagina, imagen in imagenes.items():
    subset = df[df["Página"] == pagina]
    gazepoints = list(zip(subset["x"], subset["y"], [1]*len(subset)))
    output_file = f"{output_folder}/heatmap_pagina_{pagina}.png"
    draw_heatmap(gazepoints, display_size, imagefile=imagen, alpha=alpha, savefilename=output_file)
    print(f"[✔] Mapa de calor generado para página {pagina}")
