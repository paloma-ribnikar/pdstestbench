import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sig
import scipy.io as sio
from matplotlib.patches import Rectangle

plt.close('all')

#%% Lectura de ECG

fs_ecg = 1000  # Hz

# Cargar ECG con ruido
mat_struct = sio.loadmat('ecg.mat')

ecg_one_leadruido = mat_struct['ecg_lead'].flatten()
#.flatten() transforma la matriz en un vector unidimensional

# Graficar señal original COMPLETA
plt.figure(figsize=(12, 4))
plt.plot(ecg_one_leadruido)
plt.title('ECG completo con ruido')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.grid()
plt.show()

# Graficar un tramo de la señal original (zoom)
plt.figure(figsize=(10, 4))
plt.plot(ecg_one_leadruido[5000:7000])
plt.title('ECG con ruido - Zoom')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.grid()
plt.show()

#%% Diseño de los filtros IIR

wp1 = 1    #[Hz]
ws1 = 0.1  #[Hz]
wp2 = 35   #[Hz]
ws2 = 50   #[Hz]

Gpass = 3  #[dB]
Gstop = 40 #[dB]

ripple = Gpass
att = Gstop

# Diseñamos con Gpass/2 y Gstop/2 por el sosfiltfilt (filtrado bidireccional)
sos_butt = sig.iirdesign(
    [wp1, wp2], [ws1, ws2], Gpass/2, Gstop/2,
    ftype='butter', fs=fs_ecg, output='sos'
)

sos_cheby2 = sig.iirdesign(
    [wp1, wp2], [ws1, ws2], Gpass/2, Gstop/2,
    ftype='cheby2', fs=fs_ecg, output='sos'
)

sos_cauer = sig.iirdesign(
    [wp1, wp2], [ws1, ws2], Gpass/2, Gstop/2,
    ftype='cauer', fs=fs_ecg, output='sos'
)

# Mostramos cuántas SOS y qué orden tiene cada filtro
print(f"Butterworth:   {sos_butt.shape[0]} SOS  -> Orden total: {sos_butt.shape[0]*2}")
print(f"Chebyshev II:  {sos_cheby2.shape[0]} SOS  -> Orden total: {sos_cheby2.shape[0]*2}")
print(f"Cauer:         {sos_cauer.shape[0]} SOS  -> Orden total: {sos_cauer.shape[0]*2}")

#%% Funciones de visualización y vector ff

y_min, y_max = -100, 5

# Construcción del vector ff combinando logspace y linspace
ff = np.append(
    np.logspace(np.log10(0.001), np.log10(2), 2000),
    np.logspace(np.log10(2.01), np.log10(50), 2000)
)
ff = np.append(ff, np.linspace(50, fs_ecg/2, 1000, endpoint=True))
ff = np.unique(np.append(ff, [0, ws1, wp1, wp2, ws2]))
ff = np.sort(ff)

def calc_freq_sos(sos):
    # Respuesta en frecuencia de una pasada
    f, h = sig.freqz_sos(sos, worN=ff, fs=fs_ecg)

    # Respuesta efectiva de sosfiltfilt (dos pasadas)
    # Se cuadran los módulos y la fase resultante es cero
    h_doble = np.abs(h)**2

    return f, h_doble


def calc_freq_fir(bfir):
    # Respuesta en frecuencia en Hz, de 0 a Nyquist
    resp_freq = sig.freqz(bfir, 1, worN=ff, fs=fs_ecg)
    return resp_freq


def calc_resp(resp_freq, leg_str, fig_n_axes, ax_retardo):
    (f, h) = resp_freq

    # Módulo en dB y fase desenrollada en radianes
    modulo_db = 20 * np.log10(np.maximum(np.abs(h), 1e-12))
    fase_rad = np.unwrap(np.angle(h))

    # Retardo de grupo: -d(fase)/d(omega)
    omega = 2 * np.pi * f
    retardo_s = -np.gradient(fase_rad, omega)

    umbral_db = -80
    valido = modulo_db > umbral_db
    retardo_s_plot = np.where(valido, retardo_s, np.nan)

    (fig, (ax_mod, ax_fase)) = fig_n_axes

    # Módulo
    ax_mod.plot(f, modulo_db, linewidth=1.5, label=leg_str)
    ax_mod.set_ylim(y_min, y_max)
    ax_mod.set_ylabel("Módulo (dB)")
    ax_mod.set_title("Respuesta en frecuencia y plantilla de los filtros IIR")
    ax_mod.grid(True)

    # Fase
    ax_fase.plot(f, fase_rad, label=leg_str, linewidth=1.2)
    for borde in (ws1, wp1, wp2, ws2):
        ax_fase.axvline(borde, color="gray", linestyle=":")
    ax_fase.set_xlabel("Frecuencia (Hz)")
    ax_fase.set_ylabel("Fase (rad)")
    ax_fase.grid(True)

    # Retardo
    ax_retardo.plot(f, retardo_s_plot, label=leg_str)

#%% Graficar respuestas de los filtros IIR

fig_n_axes = plt.subplots(2, 1, sharex=True, figsize=(10, 7), constrained_layout=True)
fig_retardo, ax_retardo = plt.subplots(figsize=(10, 4))

# Respuestas IIR
calc_resp(calc_freq_sos(sos_butt), 'Butterworth (Ord 16)', fig_n_axes, ax_retardo)
calc_resp(calc_freq_sos(sos_cheby2), 'Chebyshev II (Ord 8)', fig_n_axes, ax_retardo)
calc_resp(calc_freq_sos(sos_cauer), 'Cauer (Ord 6)', fig_n_axes, ax_retardo)

# Ploteo de la plantilla
(fig, (ax_mod, ax_fase)) = fig_n_axes

# Banda pasante
rect_pasante = Rectangle(
    (wp1, y_min), wp2-wp1, -ripple-y_min,
    facecolor="red", alpha=0.12, edgecolor="red", hatch="xxx", linewidth=1.2, label='Plantilla'
)
ax_mod.add_patch(rect_pasante)

# Rechazo inferior
rect_rechazo_inf = Rectangle(
    (0, -att), ws1, y_max+att,
    facecolor="red", alpha=0.12, edgecolor="red", hatch="xxx", linewidth=1.2
)
ax_mod.add_patch(rect_rechazo_inf)

# Rechazo superior
rect_rechazo = Rectangle(
    (ws2, -att), fs_ecg/2-ws2, y_max+att,
    facecolor="red", alpha=0.12, edgecolor="red", hatch="xxx", linewidth=1.2
)
ax_mod.add_patch(rect_rechazo)

for borde in (ws1, wp1, wp2, ws2):
    ax_mod.axvline(borde, color="gray", linestyle=":")

ax_mod.text((wp1+wp2)/2, y_max-6, "Banda pasante\npermitida: 0 a −3 dB", ha="center", va="top", fontsize=9)
ax_mod.text((ws2+100)/2, y_max-6, "Banda de rechazo\npermitida: ≤ −40 dB", ha="center", va="top", fontsize=9)
ax_mod.text((wp2+ws2)/2, y_min+5, "Transición", ha="center", va="bottom", fontsize=9)

ax_mod.set_xlim(0, 100)
ax_mod.legend(loc="lower left", fontsize=8)
ax_fase.legend(loc="lower left", fontsize=8)

# Retardo
for fc, ls in zip([ws1, wp1, wp2, ws2], ['--', '--', ':', ':']):
    ax_retardo.axvline(fc, color="gray", linestyle=ls)

ax_retardo.set_xlabel("Frecuencia (Hz)")
ax_retardo.set_ylabel("Retardo de grupo (s)")
ax_retardo.set_title("Retardo de grupo efectivo de los filtros IIR")
ax_retardo.set_xlim(0, 70)
ax_retardo.grid(True)
ax_retardo.legend()

plt.show()

#%% Aplicar filtros IIR al ECG

# Filtrado hacia adelante y hacia atrás con sosfiltfilt
ecg_butt = sig.sosfiltfilt(sos_butt, ecg_one_leadruido)
ecg_cheby2 = sig.sosfiltfilt(sos_cheby2, ecg_one_leadruido)
ecg_cauer = sig.sosfiltfilt(sos_cauer, ecg_one_leadruido)

# Comparación del ECG completo: con ruido vs filtrado
plt.figure(figsize=(12, 4))
plt.plot(ecg_one_leadruido, label='ECG con ruido (original)', alpha=0.5, color='gray')
plt.plot(ecg_cauer, label='ECG filtrado (Cauer IIR)', color='crimson', linewidth=0.8)
plt.title('ECG completo: Original vs Filtrado (Eliminación de línea de base)')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.legend(loc='upper right')
plt.grid()
plt.show()

# Zoom sobre un tramo con latidos
plt.figure(figsize=(11, 4))
plt.plot(ecg_one_leadruido[5000:6500], label='ECG original', alpha=0.4, color='black')
plt.plot(ecg_butt[5000:6500], label='Butterworth (Ord 16)', linewidth=1.2)
plt.plot(ecg_cheby2[5000:6500], label='Chebyshev II (Ord 8)', linewidth=1.2, linestyle='--')
plt.plot(ecg_cauer[5000:6500], label='Cauer (Ord 6)', linewidth=1.2, linestyle=':')
plt.title('Zoom ECG: Comparación de filtros IIR')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.legend(loc='upper right')
plt.grid()
plt.show()

# FIR DESIGN

# Si elijo tipo 2, el problema es la simetría porque quiero demora entera.
# Preferimos N impar para obtener un retardo entero.

taps_win_hamm = 2651
taps_win_box = 2651
taps_win_hann = 2651
delta_w = 5

# Filtro FIR por ventanas
ws1_modif = 0.5

b_win_hann = sig.firwin2(
    taps_win_hann,
    [0.0, ws1_modif, wp1, wp2, ws2, fs_ecg/2],
    [0.0, 0.0, 0.995, 0.995, 0.0, 0.0],
    window='hann', fs=fs_ecg
)


#%% Comparación de ventanas: Boxcar, Hamming y Hann

# Diseños auxiliares para comparar las ventanas
# Mismas frecuencias, ganancias y cantidad de taps

b_boxcar_comp = sig.firwin2(
    taps_win_box,
    [0.0, ws1_modif, wp1, wp2, ws2, fs_ecg/2],
    [0.0, 0.0, 0.995, 0.995, 0.0, 0.0],
    window='boxcar', fs=fs_ecg
)

b_hamming_comp = sig.firwin2(
    taps_win_hamm,
    [0.0, ws1_modif, wp1, wp2, ws2, fs_ecg/2],
    [0.0, 0.0, 0.995, 0.995, 0.0, 0.0],
    window='hamming', fs=fs_ecg
)

#%% Graficar la respuesta de las ventanas

# Dos gráficos: plantilla completa y zoom de la transición inferior
fig, (ax_mod, ax_zoom) = plt.subplots(
    1, 2, figsize=(16, 5.5), sharey=True,
    constrained_layout=True
)

# Respuestas de los filtros FIR por ventanas
filtros_ventanas = [
    (b_boxcar_comp, 'FIR Boxcar'),
    (b_hamming_comp, 'FIR Hamming'),
    (b_win_hann, 'FIR Hann')
]

for b, nombre in filtros_ventanas:

    # Reutilizamos la función original calc_freq_fir()
    f, h = calc_freq_fir(b)

    modulo_db = 20 * np.log10(np.maximum(np.abs(h), 1e-12))

    ax_mod.plot(f, modulo_db, linewidth=1.5, label=nombre)
    ax_zoom.plot(f, modulo_db, linewidth=1.5, label=nombre)


# Ploteo de la plantilla en ambos gráficos

for ax in (ax_mod, ax_zoom):

    # Banda pasante: zona no permitida por debajo de -ripple
    rect_pasante = Rectangle(
        (wp1, y_min), wp2-wp1, -ripple-y_min,
        facecolor="red", alpha=0.12,
        edgecolor="red", hatch="xxx", linewidth=1.2,
        label='Plantilla'
    )
    ax.add_patch(rect_pasante)

    # Banda de rechazo: zona no permitida por encima de -att

    # Rechazo inferior
    rect_rechazo_inf = Rectangle(
        (0, -att), ws1, y_max+att,
        facecolor="red", alpha=0.12,
        edgecolor="red", hatch="xxx", linewidth=1.2
    )
    ax.add_patch(rect_rechazo_inf)

    # Rechazo superior
    rect_rechazo = Rectangle(
        (ws2, -att), fs_ecg/2-ws2, y_max+att,
        facecolor="red", alpha=0.12,
        edgecolor="red", hatch="xxx", linewidth=1.2
    )
    ax.add_patch(rect_rechazo)

    # Límites de la plantilla
    for borde in (ws1, wp1, wp2, ws2):
        ax.axvline(borde, color="gray", linestyle=":")

    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Frecuencia (Hz)")
    ax.set_ylabel("Módulo (dB)")
    ax.grid(True)
    ax.legend(loc="lower left", fontsize=8)


# --- Gráfico 1: plantilla completa ---

ax_mod.set_title("Respuesta en frecuencia y plantilla")
ax_mod.set_xlim(0, 100)

# Etiquetas de zonas
ax_mod.text(
    (wp1+wp2)/2, y_max-6,
    "Banda pasante\npermitida: 0 a −3 dB",
    ha="center", va="top", fontsize=9
)

ax_mod.text(
    (ws2+100)/2, y_max-6,
    "Banda de rechazo\npermitida: ≤ −40 dB",
    ha="center", va="top", fontsize=9
)

ax_mod.text(
    (wp2+ws2)/2, y_min+5,
    "Transición",
    ha="center", va="bottom", fontsize=9
)


# --- Gráfico 2: zoom de la transición inferior ---

ax_zoom.set_title("Zoom: transición inferior (0 a 2 Hz)")
ax_zoom.set_xlim(0, 2)

plt.show()

#%% FIR design Least Squares

taps_firls = 2251
wp2_diseno_ls = 43
ws2_diseno_ls = 45

b_firls = sig.firls(
    taps_firls,
    [0.0, ws1, wp1, wp2_diseno_ls, ws2_diseno_ls, fs_ecg/2],
    [0.0, 0.0, 0.98, 0.98, 0.0, 0.0],
    weight=[500.0, 5.0, 500.0],
    fs=fs_ecg
)

#%% FIR design Parks-McClellan

taps_remez = 1251

b_remez = sig.remez(
    taps_remez,
    [0.0, ws1, wp1, wp2_diseno_ls, ws2_diseno_ls, fs_ecg/2],
    [0.0, 0.9, 0.0],
    weight=[100.0, 10.0, 100.0],
    fs=fs_ecg
)

#%% Verificación conjunta de la plantilla FIR

fig, (ax_mod, ax_zoom) = plt.subplots(
    1, 2, figsize=(16, 5.5), sharey=True,
    constrained_layout=True
)

# Respuestas de los tres filtros FIR
filtros_fir = [
    (b_win_hann, 'FIR Hann'),
    (b_firls, 'FIR LS'),
    (b_remez, 'FIR Parks-McClellan')
]

for b, nombre in filtros_fir:

    # Reutilizamos calc_freq_fir()
    f, h = calc_freq_fir(b)

    modulo_db = 20 * np.log10(np.maximum(np.abs(h), 1e-12))

    ax_mod.plot(f, modulo_db, linewidth=1.5, label=nombre)
    ax_zoom.plot(f, modulo_db, linewidth=1.5, label=nombre)


# Ploteo de la plantilla original en ambos gráficos

for ax in (ax_mod, ax_zoom):

    # Banda pasante: zona no permitida por debajo de -ripple
    rect_pasante = Rectangle(
        (wp1, y_min), wp2-wp1, -ripple-y_min,
        facecolor="red", alpha=0.12,
        edgecolor="red", hatch="xxx", linewidth=1.2,
        label='Plantilla'
    )
    ax.add_patch(rect_pasante)

    # Banda de rechazo: zona no permitida por encima de -att

    # Rechazo inferior
    rect_rechazo_inf = Rectangle(
        (0, -att), ws1, y_max+att,
        facecolor="red", alpha=0.12,
        edgecolor="red", hatch="xxx", linewidth=1.2
    )
    ax.add_patch(rect_rechazo_inf)

    # Rechazo superior
    rect_rechazo = Rectangle(
        (ws2, -att), fs_ecg/2-ws2, y_max+att,
        facecolor="red", alpha=0.12,
        edgecolor="red", hatch="xxx", linewidth=1.2
    )
    ax.add_patch(rect_rechazo)

    # Límites de la plantilla
    for borde in (ws1, wp1, wp2, ws2):
        ax.axvline(borde, color="gray", linestyle=":")

    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Frecuencia (Hz)")
    ax.set_ylabel("Módulo (dB)")
    ax.grid(True)
    ax.legend(loc="lower left", fontsize=8)


# --- Gráfico 1: plantilla completa ---

ax_mod.set_title("Respuesta en frecuencia y plantilla FIR")
ax_mod.set_xlim(0, 100)

# Etiquetas originales
ax_mod.text(
    (wp1+wp2)/2, y_max-6,
    "Banda pasante\npermitida: 0 a −3 dB",
    ha="center", va="top", fontsize=9
)

ax_mod.text(
    (ws2+100)/2, y_max-6,
    "Banda de rechazo\npermitida: ≤ −40 dB",
    ha="center", va="top", fontsize=9
)

ax_mod.text(
    (wp2+ws2)/2, y_min+5,
    "Transición",
    ha="center", va="bottom", fontsize=9
)


# --- Gráfico 2: transición inferior ---

ax_zoom.set_title("Zoom: transición inferior (0 a 2 Hz)")
ax_zoom.set_xlim(0, 2)

plt.show()

#%% Comparación de fase y retardo de grupo FIR

fig, (ax_fase, ax_retardo) = plt.subplots(
    1, 2, figsize=(15, 5),
    constrained_layout=True
)

filtros_fir = [
    (b_win_hann, 'FIR Hann'),
    (b_firls, 'FIR LS'),
    (b_remez, 'FIR Parks-McClellan')
]

for b, nombre in filtros_fir:

    # Respuesta en frecuencia original
    f, h = calc_freq_fir(b)

    # Analizamos únicamente la banda pasante
    banda_pasante = (f >= wp1) & (f <= wp2)

    f_paso = f[banda_pasante]
    h_paso = h[banda_pasante]

    # Fase desenrollada
    fase_rad = np.unwrap(np.angle(h_paso))

    # Retardo de grupo: -d(fase)/d(omega)
    omega = 2 * np.pi * f_paso
    retardo_s = -np.gradient(fase_rad, omega)

    # Gráficos
    ax_fase.plot(f_paso, fase_rad, label=nombre)
    ax_retardo.plot(f_paso, retardo_s, label=nombre)


# --- Fase ---

ax_fase.set_title("Fase de los filtros FIR")
ax_fase.set_xlabel("Frecuencia (Hz)")
ax_fase.set_ylabel("Fase (rad)")
ax_fase.set_xlim(wp1, wp2)
ax_fase.grid()
ax_fase.legend()


# --- Retardo de grupo ---

ax_retardo.set_title("Retardo de grupo de los filtros FIR")
ax_retardo.set_xlabel("Frecuencia (Hz)")
ax_retardo.set_ylabel("Retardo de grupo (s)")
ax_retardo.set_xlim(wp1, wp2)
ax_retardo.grid()
ax_retardo.legend()

plt.show()
