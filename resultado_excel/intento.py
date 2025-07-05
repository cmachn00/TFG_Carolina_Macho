# -*- coding: utf-8 -*-
"""
Created on Sat Jun  7 17:52:50 2025

@author: USUARIO
"""

import tobii_research as tr
import time
import csv
import keyboard
from collections import defaultdict

# Variables globales
event_count = defaultdict(int)
key_pressed = False
recording = False
start_time = None
page_number = 0
global_csv_filename = "gaze_datos_completo.csv"

# Detectar el eye tracker
found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]

print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name: " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)

# Inicializar archivo CSV con cabecera
fieldnames = ['Fase', 'Página', 'Left Eye X', 'Left Eye Y', 'Right Eye X', 'Right Eye Y',
              'Pupil left eye', 'Pupil right eye', 'Timestamp device', 'Timestamp system',
              'Evento', 'Duración (segundos)']

with open(global_csv_filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

def escribir_fila_csv(fase, pagina, gaze_data=None, evento='', duracion=''):
    with open(global_csv_filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        row = {
            'Fase': fase,
            'Página': pagina,
            'Left Eye X': '',
            'Left Eye Y': '',
            'Right Eye X': '',
            'Right Eye Y': '',
            'Pupil left eye': '',
            'Pupil right eye': '',
            'Timestamp device': '',
            'Timestamp system': '',
            'Evento': evento,
            'Duración (segundos)': duracion
        }

        if gaze_data:
            row.update({
                'Left Eye X': float(gaze_data['left_gaze_point_on_display_area'][0]),
                'Left Eye Y': float(gaze_data['left_gaze_point_on_display_area'][1]),
                'Right Eye X': float(gaze_data['right_gaze_point_on_display_area'][0]),
                'Right Eye Y': float(gaze_data['right_gaze_point_on_display_area'][1]),
                'Pupil left eye': gaze_data['left_pupil_diameter'],
                'Pupil right eye': gaze_data['right_pupil_diameter'],
                'Timestamp device': gaze_data['device_time_stamp'],
                'Timestamp system': gaze_data['system_time_stamp'],
                'Evento': evento,
                'Duración (segundos)': duracion
            })

        writer.writerow(row)

def gaze_data_callback(gaze_data):
    global event_count, key_pressed, recording, page_number

    if not recording:
        return

    if keyboard.is_pressed('e') and not key_pressed:
        event_count['e'] += 1
        key_pressed = True
    elif not keyboard.is_pressed('e'):
        key_pressed = False

    evento = f"Evento {event_count['e']}"
    escribir_fila_csv("grabando", page_number, gaze_data, evento)

# Suscribirse al eye tracker
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

print("\nINSTRUCCIONES:")
print("1 → empezar a grabar página 1")
print("2 → parar página 1")
print("3 → empezar página 2")
print("4 → parar página 2")
print("5 → empezar página 3")
print("6 → parar página 3")
print("q → salir del experimento\n")

# Bucle principal
try:
    while True:
        if keyboard.is_pressed('1'):
            print("⏺️ Inicio página 1")
            page_number = 1
            recording = True
            start_time = time.time()
            escribir_fila_csv("inicio_pagina", page_number)
            time.sleep(0.3)

        elif keyboard.is_pressed('2') and recording and page_number == 1:
            end_time = time.time()
            duracion = round(end_time - start_time, 3)
            recording = False
            escribir_fila_csv("fin_pagina", page_number, evento="Fin página 1", duracion=duracion)
            print(f"⏹️ Fin página 1. Duración: {duracion} s")
            time.sleep(0.3)

        elif keyboard.is_pressed('3'):
            print("⏺️ Inicio página 2")
            page_number = 2
            recording = True
            start_time = time.time()
            escribir_fila_csv("inicio_pagina", page_number)
            time.sleep(0.3)

        elif keyboard.is_pressed('4') and recording and page_number == 2:
            end_time = time.time()
            duracion = round(end_time - start_time, 3)
            recording = False
            escribir_fila_csv("fin_pagina", page_number, evento="Fin página 2", duracion=duracion)
            print(f"Fin página 2. Duración: {duracion} s")
            time.sleep(0.3)

        elif keyboard.is_pressed('5'):
            print("Inicio página 3")
            page_number = 3
            recording = True
            start_time = time.time()
            escribir_fila_csv("inicio_pagina", page_number)
            time.sleep(0.3)

        elif keyboard.is_pressed('6') and recording and page_number == 3:
            end_time = time.time()
            duracion = round(end_time - start_time, 3)
            recording = False
            escribir_fila_csv("fin_pagina", page_number, evento="Fin página 3", duracion=duracion)
            print(f"Fin página 3. Duración: {duracion} s")
            time.sleep(0.3)

        elif keyboard.is_pressed('q'):
            print("Fin del experimento")
            break

        time.sleep(0.05)

finally:
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    print(f"\n✅ Todo se ha guardado en '{global_csv_filename}'")
