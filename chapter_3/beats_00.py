import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

import librosa
import librosa.display


# Crear una señal de audio simulada (por simplicidad)
tiempo = np.linspace(0, 1, 1000)  # 1 segundo de audio
frecuencia = 2  # Frecuencia de pulsación en Hz
audio = np.sin(2 * np.pi * frecuencia * tiempo)
print('timepo: ',tiempo)
# Parámetros para el análisis de energía
ventana_tamaño = 0.1  # 100 milisegundos
muestras_por_ventana = int(ventana_tamaño * len(tiempo))
print('muestras_por_ventana: ', muestras_por_ventana)
energia = []

# Calcular la energía en ventanas de tiempo
for i in range(0, len(audio), muestras_por_ventana):
    ventana = audio[i:i + muestras_por_ventana]
    energia_ventana = np.sum(ventana**2)
    energia.append(energia_ventana)

# Crear una lista de tiempos en segundos para las ventanas de tiempo, comenzando desde 100 ms
ventana_tiempo = np.arange(ventana_tamaño, len(audio) / 1000 + ventana_tamaño, ventana_tamaño)  # Convertir a segundos

# Encontrar picos en la secuencia de energía
picos, _ = find_peaks(energia, height=0.1 * max(energia))  # Ajusta el umbral según sea necesario

# Visualizar la señal de audio y la energía en dos subplots
fig, axs = plt.subplots(2, figsize=(10, 6))

# Gráfico de la señal de audio
axs[0].plot(tiempo, audio)
axs[0].set_title('Señal de Audio')
axs[0].set_xlabel('Tiempo (segundos)')
axs[0].set_ylabel('Amplitud')
axs[0].grid(True)

# Gráfico de la energía
axs[1].plot(ventana_tiempo, energia)
axs[1].set_title('Análisis de Energía en Ventanas de Tiempo')
axs[1].set_xlabel('Tiempo (segundos)')
axs[1].set_ylabel('Energía')
axs[1].grid(True)

# Mostrar valores de energía en el gráfico
for i, e in enumerate(energia):
    axs[1].text(ventana_tiempo[i], e, f'{e:.2f}', ha='center', va='bottom')

# Resaltar picos en el gráfico de energía
axs[1].plot(np.array(ventana_tiempo)[picos], np.array(energia)[picos], 'ro', label='Picos de Energía')

# Añadir la descripción de encontrar picos
descripcion = "Buscar picos en la secuencia de energía. La energía suele corresponder a los eventos de ritmo, es decir, los golpes en la música."
plt.figtext(0.5, 0.01, descripcion, ha='center', fontsize=10, bbox={"facecolor":"lightgray", "alpha":0.7, "pad":5})

plt.tight_layout()

# Estimación del tempo
if len(picos) >= 2:
    print('picos:',picos)
    print('ventana_tiempo: ', ventana_tiempo)
    diferencias_temporales = np.diff(np.array(ventana_tiempo)[picos])
    print('diferencias_temporales: ', diferencias_temporales)
    tempo_estimado = 60 / np.mean(diferencias_temporales)
    
    print(f"Tempo estimado: {tempo_estimado:.2f} BPM")
    # Gráfico para mostrar la estimación del tempo
    """
    Esto significa que estamos determinando cuántos pulsos (picos) 
    ocurren en un minuto, basándonos en las diferencias temporales 
    entre los picos de energía en la secuencia. El resultado obtenido 
    representa el tempo musical en términos de BPM, que es una medida 
    comúnmente utilizada para describir la velocidad o ritmo de una pieza musical.
    """
        # Gráfico para mostrar la estimación del tempo con valor de BPM
    # Gráfico para mostrar la estimación del tempo con valor de BPM deseado
    plt.figure()
    plt.plot(np.array(ventana_tiempo)[picos][1:], [tempo_estimado] * (len(picos) - 1), 'bo-', label=f'Tempo Estimado Promedio: {tempo_estimado:.2f} BPM')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Tempo (BPM)')
    plt.title('Estimación del Tempo')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

        
    # Estimación del tempo utilizando librosa con la señal simuladatempo_librosa, _ = librosa.beat.beat_track(y=audio, sr=1000, hop_length=len(audio), n_fft=512)
    tempo_librosa, _ = librosa.beat.beat_track(y=audio, sr=44100, units='time')

    # Utiliza hop_length=len(audio)
    print(f'Tempo estimado con librosa (Simulado): {tempo_librosa:.2f} BPM')



plt.show()
