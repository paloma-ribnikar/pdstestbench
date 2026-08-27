#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio de Cuantización de un ADC (Análisis y Procesamiento de Señales)
Resuelto a partir del esqueleto de Mariano.

Conceptos Clave:
  1. Paso de cuantización: q = 2 * Vf / (2**B)
  2. Proceso de cuantización: srq = np.round(sr / q) * q
  3. Ruido de cuantización: nq = srq - sr  (distribuido uniforme entre -q/2 y +q/2)
  4. Potencia teórica del ruido de cuantización: Pq = q^2 / 12
"""

import numpy as np
import matplotlib.pyplot as plt

#%% Datos de la simulación

fs = 1000.0  # Frecuencia de muestreo (Hz)
N = 1000     # Cantidad de muestras

# Datos del ADC
B = 4        # Cantidad de bits del cuantizador (ej: 4 bits => 16 niveles)
Vf = 2.0     # Rango simétrico de +/- Vf Volts (VFS = 2*Vf = 4V)
q = (2.0 * Vf) / (2**B)  # Paso de cuantización de q Volts

# Datos del ruido
# Potencia del ruido de cuantización uniforme teórica: Pq = q^2 / 12
pot_ruido_cuant = (q**2) / 12.0  # Watts 
kn = 1.0  # Escala de la potencia de ruido analógico
pot_ruido_analog = pot_ruido_cuant * kn 

ts = 1.0 / fs  # Tiempo de muestreo
df = fs / N    # Resolución espectral
tt = np.arange(N) * ts

#%% Experimento:
"""
   Se desea simular el efecto de la cuantización sobre una señal senoidal de 
   frecuencia 1 Hz. La señal "analógica" tiene añadida una cantidad de 
   ruido gaussiano e incorrelado.
"""

# 1. Señal analógica pura (senoidal de 1 Hz y potencia 1 W -> Amplitud = sqrt(2))
analog_sig = np.sqrt(2) * np.sin(2 * np.pi * 1.0 * tt)

# 2. Ruido analógico gaussiano
nn = np.random.normal(loc=0.0, scale=np.sqrt(pot_ruido_analog), size=N)

# 3. Señal analógica de entrada al ADC (con ruido analógico)
sr = analog_sig + nn

# 4. Proceso de Cuantización (Normalizar por q, Redondear y Volver a multiplicar por q)
srq = np.round(sr / q) * q

# 5. Señal de ruido de cuantización
nq = srq - sr

#%% Visualización de resultados

# Cierro ventanas anteriores
plt.close('all')

##################
# 1. Señal temporal
##################

plt.figure(1, figsize=(10, 5))
plt.plot(tt, srq, lw=2, linestyle='', color='blue', marker='o', markersize=4, markerfacecolor='blue', markeredgecolor='blue', fillstyle='none', label='ADC out (cuantizada $s_Q$)')
plt.plot(tt, sr, lw=1, color='black', marker='x', ls='dotted', alpha=0.6, label='$s_R$ (analógica + ruido)')
plt.plot(tt, analog_sig, lw=1.5, color='red', label='$s$ (senoidal pura 1 W)')

plt.title('Señal muestreada por un ADC de {:d} bits - $\pm V_F= $ {:3.1f} V - q = {:3.3f} V'.format(B, Vf, q))
plt.xlabel('Tiempo [segundos]')
plt.ylabel('Amplitud [V]')
plt.xlim([0, 2]) # Muestro los primeros 2 segundos para apreciar los escalones
axes_hdl = plt.gca()
axes_hdl.legend(loc='upper right')
plt.grid(True)

###########
# 2. Espectro de Densidad de Potencia (dB)
###########

plt.figure(2, figsize=(10, 6))
ft_SR = (1/N) * np.fft.fft(sr)
ft_Srq = (1/N) * np.fft.fft(srq)
ft_As = (1/N) * np.fft.fft(analog_sig)
ft_Nq = (1/N) * np.fft.fft(nq)
ft_Nn = (1/N) * np.fft.fft(nn)

# Grilla de sampleo frecuencial
ff = np.linspace(0, (N-1)*df, N)
bfrec = ff <= fs/2

Nnq_mean = np.mean(np.abs(ft_Nq)**2)
nNn_mean = np.mean(np.abs(ft_Nn)**2)

plt.plot(ff[bfrec], 10 * np.log10(2 * np.abs(ft_As[bfrec])**2), color='orange', ls='dotted', label='$s$ (señal pura)')
plt.plot(np.array([ff[bfrec][0], ff[bfrec][-1]]), 10 * np.log10(2 * np.array([nNn_mean, nNn_mean])), '--r', label='$\\overline{n} =$ ' + '{:3.1f} dB'.format(10 * np.log10(2 * nNn_mean)))
plt.plot(ff[bfrec], 10 * np.log10(2 * np.abs(ft_SR[bfrec])**2), ':g', label='$s_R = s + n$')
plt.plot(ff[bfrec], 10 * np.log10(2 * np.abs(ft_Srq[bfrec])**2), lw=2, label='$s_Q = Q_{B,V_F}\\{s_R\\}$')
plt.plot(np.array([ff[bfrec][0], ff[bfrec][-1]]), 10 * np.log10(2 * np.array([Nnq_mean, Nnq_mean])), '--c', label='$\\overline{n_Q} =$ ' + '{:3.1f} dB'.format(10 * np.log10(2 * Nnq_mean)))
plt.plot(ff[bfrec], 10 * np.log10(2 * np.abs(ft_Nn[bfrec])**2), ':r', alpha=0.5)
plt.plot(ff[bfrec], 10 * np.log10(2 * np.abs(ft_Nq[bfrec])**2), ':c', alpha=0.5)
plt.axvline(x=fs/2, color='k', linestyle=':', label='BW (Nyquist)', lw=0.8)

plt.title('Señal muestreada por un ADC de {:d} bits - $\pm V_F= $ {:3.1f} V - q = {:3.3f} V'.format(B, Vf, q))
plt.ylabel('Densidad de Potencia [dB]')
plt.xlabel('Frecuencia [Hz]')
axes_hdl = plt.gca()
axes_hdl.legend(loc='upper right')
plt.grid(True)

#############
# 3. Histograma del Ruido de Cuantización
#############

plt.figure(3, figsize=(8, 5))
bins = 10
plt.hist(nq.flatten() / q, bins=bins, density=False, color='skyblue', edgecolor='black', alpha=0.7, label='Ruido Medido $n_q / q$')
plt.plot(np.array([-1/2, -1/2, 1/2, 1/2]), np.array([0, N/bins, N/bins, 0]), '--r', lw=2, label='Distribución Uniforme Teórica')
plt.title('Ruido de cuantización para {:d} bits - $\pm V_F= $ {:3.1f} V - q = {:3.3f} V'.format(B, Vf, q))
plt.xlabel('Pasos de cuantización ($q$) [V]')
plt.ylabel('Cantidad de Muestras')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
