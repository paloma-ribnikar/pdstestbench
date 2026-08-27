#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 14:58:13 2025

@author: mariano
"""

#%% módulos y funciones a importar
import numpy as np
import matplotlib.pyplot as plt

#%% Datos de la simulación

fs = 1000.0  # frecuencia de muestreo (Hz)
N = 1000     # cantidad de muestras

# Datos del ADC
B = 4        # bits
Vf = 2.0     # rango simétrico de +/- Vf Volts
q = (2.0 * Vf) / (2**B)  # paso de cuantización de q Volts

# datos del ruido (potencia de la señal normalizada, es decir 1 W)
pot_ruido_cuant = (q**2) / 12.0  # Watts 
kn = 1.0     # escala de la potencia de ruido analógico
pot_ruido_analog = pot_ruido_cuant * kn # 

ts = 1.0 / fs  # tiempo de muestreo
df = fs / N    # resolución espectral
tt = np.arange(N) * ts

#%% Experimento: 
"""
   Se desea simular el efecto de la cuantización sobre una señal senoidal de 
   frecuencia 1 Hz. La señal "analógica" podría tener añadida una cantidad de 
   ruido gausiano e incorrelado.
   
   Se pide analizar el efecto del muestreo y cuantización sobre la señal 
   analógica. Para ello se proponen una serie de gráficas que tendrá que ayudar
   a construir para luego analizar los resultados.
   
"""

# Señales

analog_sig = np.sqrt(2) * np.sin(2 * np.pi * 1.0 * tt)  # señal analógica sin ruido (1 W => A = sqrt(2))
nn = np.random.normal(loc=0.0, scale=np.sqrt(pot_ruido_analog), size=N)  # señal de ruido analógico
sr = analog_sig + nn  # señal analógica de entrada al ADC (con ruido analógico)

# Proceso de cuantización: normalizar por q, redondear y desnormalizar (* q)
srq = np.round(sr / q) * q  # señal cuantizada
nq = srq - sr  # señal de ruido de cuantización


#%% Visualización de resultados

# cierro ventanas anteriores
plt.close('all')

##################
# Señal temporal
##################

plt.figure(1)

plt.plot(tt, srq, lw=2, linestyle='', color='blue', marker='o', markersize=4, markerfacecolor='blue', markeredgecolor='blue', fillstyle='none', label='ADC out (cuantizada)')
plt.plot(tt, sr, lw=1, color='black', marker='x', ls='dotted', alpha=0.6, label='$ s_R $ (analog + ruido)')
plt.plot(tt, analog_sig, lw=1.5, color='red', label='$ s $ (senoidal pura 1W)')

plt.title('Señal muestreada por un ADC de {:d} bits - $\pm V_F= $ {:3.1f} V - q = {:3.3f} V'.format(B, Vf, q) )
plt.xlabel('tiempo [segundos]')
plt.ylabel('Amplitud [V]')
plt.xlim([0, 2])
axes_hdl = plt.gca()
axes_hdl.legend(loc='upper right')
plt.grid(True)
plt.show()


###########
# Espectro
###########

plt.figure(2)
ft_SR = (1/N) * np.fft.fft(sr)
ft_Srq = (1/N) * np.fft.fft(srq)
ft_As = (1/N) * np.fft.fft(analog_sig)
ft_Nq = (1/N) * np.fft.fft(nq)
ft_Nn = (1/N) * np.fft.fft(nn)

# grilla de sampleo frecuencial
ff = np.linspace(0, (N-1)*df, N)

bfrec = ff <= fs/2

Nnq_mean = np.mean(np.abs(ft_Nq)**2)
nNn_mean = np.mean(np.abs(ft_Nn)**2)

plt.plot( ff[bfrec], 10* np.log10(2*np.abs(ft_As[bfrec])**2), color='orange', ls='dotted', label='$ s $ (sig.)' )
plt.plot( np.array([ ff[bfrec][0], ff[bfrec][-1] ]), 10* np.log10(2* np.array([nNn_mean, nNn_mean]) ), '--r', label= '$ \\overline{n} = $' + '{:3.1f} dB'.format(10* np.log10(2* nNn_mean)) )
plt.plot( ff[bfrec], 10* np.log10(2*np.abs(ft_SR[bfrec])**2), ':g', label='$ s_R = s + n $' )
plt.plot( ff[bfrec], 10* np.log10(2*np.abs(ft_Srq[bfrec])**2), lw=2, label='$ s_Q = Q_{B,V_F}\\{s_R\\}$' )
plt.plot( np.array([ ff[bfrec][0], ff[bfrec][-1] ]), 10* np.log10(2* np.array([Nnq_mean, Nnq_mean]) ), '--c', label='$ \\overline{n_Q} = $' + '{:3.1f} dB'.format(10* np.log10(2* Nnq_mean)) )
plt.plot( ff[bfrec], 10* np.log10(2*np.abs(ft_Nn[bfrec])**2), ':r', alpha=0.5)
plt.plot( ff[bfrec], 10* np.log10(2*np.abs(ft_Nq[bfrec])**2), ':c', alpha=0.5)
plt.plot( np.array([ ff[bfrec][-1], ff[bfrec][-1] ]), plt.ylim(), ':k', label='BW', lw = 0.5  )

plt.title('Señal muestreada por un ADC de {:d} bits - $\pm V_F= $ {:3.1f} V - q = {:3.3f} V'.format(B, Vf, q) )
plt.ylabel('Densidad de Potencia [dB]')
plt.xlabel('Frecuencia [Hz]')
axes_hdl = plt.gca()
axes_hdl.legend(loc='upper right')
plt.grid(True)
plt.show()

#############
# Histograma
#############

plt.figure(3)
bins = 10
plt.hist(nq.flatten()/(q), bins=bins, color='skyblue', edgecolor='black', alpha=0.7)
plt.plot( np.array([-1/2, -1/2, 1/2, 1/2]), np.array([0, N/bins, N/bins, 0]), '--r', lw=2 )
plt.title( 'Ruido de cuantización para {:d} bits - $\pm V_F= $ {:3.1f} V - q = {:3.3f} V'.format(B, Vf, q))

plt.xlabel('Pasos de cuantización (q) [V]')
plt.grid(True)
plt.show()
