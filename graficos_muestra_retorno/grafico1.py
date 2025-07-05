#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 13:21:43 2025

@author: carolinamachonieto
"""
import matplotlib.pyplot as plt
import numpy as np

# datos totales de la página 1
areas = ['Área 1', 'Área 2', 'Área 3']
muestras = [2855, 9017, 272]
retornos = [68, 96, 30]

# --------- GRÁFICO 1: muestras por área ----------
plt.figure(figsize=(8,5))
plt.bar(areas, muestras, color='#ADD8E6')
plt.title('Total de muestras por área - Página 1')
plt.ylabel('Número de muestras')
plt.xlabel('Áreas')
plt.show()

# --------- GRÁFICO 2: retornos por área ----------
plt.figure(figsize=(8,5))
plt.bar(areas, retornos, color='#90EE90')
plt.title('Total de retornos por área - Página 1')
plt.ylabel('Número de retornos')
plt.xlabel('Áreas')
plt.show()
