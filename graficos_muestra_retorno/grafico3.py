#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 13:29:06 2025

@author: carolinamachonieto
"""

import matplotlib.pyplot as plt

# datos totales de la página 3
areas = ['Área 1', 'Área 2', 'Área 3']
muestras = [4278, 7515, 0]
retornos = [41, 28, 0]

# --------- GRÁFICO 1: muestras con azul claro ----------
plt.figure(figsize=(8,5))
plt.bar(areas, muestras, color='#ADD8E6')  # azul clarito
plt.title('Total de muestras por área - Página 3')
plt.ylabel('Número de muestras')
plt.xlabel('Áreas')
plt.show()

# --------- GRÁFICO 2: retornos con verde pastel ----------
plt.figure(figsize=(8,5))
plt.bar(areas, retornos, color='#90EE90')  # verde pastel
plt.title('Total de retornos por área - Página 3')
plt.ylabel('Número de retornos')
plt.xlabel('Áreas')
plt.show()
