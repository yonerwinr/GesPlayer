import tkinter as tk
from tkinter import ttk
import threading
import sounddevice as sd
import numpy as np

def update_decibel_meter(indata, frames, time, status):
    # Calcula el nivel de decibeles RMS
    rms = np.sqrt(np.mean(indata**2))
    decibels = 20 * np.log10(rms)

    # Actualiza el valor de la barra de progreso según el nivel de decibeles
    for i, progressbar in enumerate(ttk.Progressbar):
        progressbar['value'] = decibels * (i + 1)

def start_decibel_meter():
    # Configura el dispositivo de audio y la frecuencia de muestreo
    duration = 0.1  # Duración de cada muestra en segundos
    fs = 44100  # Frecuencia de muestreo en Hz

    # Crea las barras de progreso
    num_bars = 13
    progressbars = []
    for i in range(num_bars):
        progressbar = ttk.Progressbar(root, orient='vertical', length=200, mode='determinate')
        progressbar.pack(side=tk.LEFT, padx=5)
        progressbars.append(progressbar)

    # Inicia los medidores de decibeles en un hilo separado
    with sd.InputStream(callback=update_decibel_meter, channels=1, samplerate=fs):
        sd.sleep(int(duration * 1000))

root = tk.Tk()
root.geometry("800x400")
root.title("Barras de Progreso de Decibeles")

# Iniciar el medidor de decibeles en un hilo separado
start_decibel_meter_thread = threading.Thread(target=start_decibel_meter)
start_decibel_meter_thread.daemon = True
start_decibel_meter_thread.start()

root.mainloop()
