import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sig
import scipy.io as sio
from scipy.interpolate import CubicSpline

plt.close('all')

# Configuración de visualización
plt.style.use('default')

# Frecuencia de muestreo del registro
fs_ecg = 1000  # Hz

# Carga de datos del registro
mat_struct = sio.loadmat('ECG_TP4.mat')
ecg_one_leadruido = mat_struct['ecg_lead'].flatten()
qrs_detections_ref = mat_struct['qrs_detections'].flatten().astype(int)
qrs_pattern1 = mat_struct['qrs_pattern1'].flatten()

cant_muestras = len(ecg_one_leadruido)

print("Datos cargados correctamente:")
print(f" - Muestras totales de ECG: {cant_muestras:,} ({cant_muestras/fs_ecg:.1f} s)")
print(f" - Cantidad de latidos de referencia en el registro: {len(qrs_detections_ref)}")
print(f" - Longitud del patrón QRS (qrs_pattern1): {len(qrs_pattern1)} muestras")

#%% ESTIMACIÓN DE LA LÍNEA DE BASE CON MEDIANA

# Primera etapa: ventana de 201 muestras (elimina QRS)
b_200 = sig.medfilt(ecg_one_leadruido, 201)

# Segunda etapa: ventana de 601 muestras sobre la salida anterior (elimina ondas T y P)
b_mediana = sig.medfilt(b_200, 601)

# Señal de ECG corregida por sustracción
ecg_mediana = ecg_one_leadruido - b_mediana

print("Estimación de mediana calculada con éxito.")

# Visualización de la estimación en dos regiones de interés
regs_mediana = ([4000, 5500], [720000, 744000])

for inicio, fin in regs_mediana:
    zoom_r = np.arange(inicio, fin)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 6), sharex=True, constrained_layout=True)
    
    # Estimación de la línea de base
    ax1.plot(zoom_r, ecg_one_leadruido[zoom_r], color='gray', alpha=0.6, label='ECG original')
    ax1.plot(zoom_r, b_200[zoom_r], color='steelblue', linestyle='--', label='1ra Mediana (201 muestras)')
    ax1.plot(zoom_r, b_mediana[zoom_r], color='darkorange', linewidth=2, label='Línea de base estimada b̂ (601 muestras)')
    ax1.set_title(f'Estimación de Línea de Base por Mediana - Intervalo [{inicio}:{fin}]', fontweight='bold')
    ax1.set_ylabel('Amplitud')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right')
    
    # ECG corregido
    ax2.plot(zoom_r, ecg_mediana[zoom_r], color='crimson', linewidth=1, label='ECG corregido (x - b̂_mediana)')
    ax2.set_title('ECG Corregido', fontweight='bold')
    ax2.set_xlabel('Muestras (#)')
    ax2.set_ylabel('Amplitud')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right')
    
    plt.show()

#%% LOCALIZACIÓN DE SEGMENTOS PQ E INTERPOLACIÓN SPLINE

qrd_det = qrs_detections_ref.copy()

# Ventana de 20 muestras situada entre 60 y 40 ms antes de cada QRS
start_win = qrd_det - 60
end_win = qrd_det - 40

# Filtrar índices válidos dentro del rango de la señal
validos = (start_win >= 0) & (end_win <= cant_muestras)
qrd_det = qrd_det[validos]
start_win = start_win[validos]
end_win = end_win[validos]

# Tiempo medio de cada ventana PQ
pq_t_hat = np.array([np.mean([a, b]) for a, b in zip(start_win, end_win)])

# Amplitud media sobre el ECG original (construcción de la estimación)
pq_hat = np.array([np.mean(ecg_one_leadruido[a:b]) for a, b in zip(start_win, end_win)])

# Amplitud media sobre el ECG corregido por mediana (para verificación visual de cercanía a cero)
pq_mediana = np.array([np.mean(ecg_mediana[a:b]) for a, b in zip(start_win, end_win)])

# 1. Verificación de la ubicación de los puntos PQ en dos casos contrastantes
regs_pq = ([92000, 95000], [720000, 723000])

for inicio, fin in regs_pq:
    zoom_r = np.arange(inicio, fin)
    qrs_r = qrd_det[(qrd_det >= inicio) & (qrd_det < fin)]
    pq_r = (pq_t_hat >= inicio) & (pq_t_hat < fin)
    
    plt.figure(figsize=(13, 4.5))
    plt.plot(zoom_r, ecg_mediana[zoom_r], color='steelblue', label='ECG corregido (mediana)')
    for q in qrs_r:
        plt.axvline(q, color='red', linestyle='--', alpha=0.5)
        plt.axvspan(q-60, q-40, color='green', alpha=0.2)
    plt.plot(pq_t_hat[pq_r], pq_mediana[pq_r], 'og', markersize=6, label='Promedio PQ estimado')
    
    plt.title(f'Verificación de Puntos PQ en Intervalo [{inicio}:{fin}]', fontweight='bold')
    plt.xlabel('Muestras (#)')
    plt.ylabel('Amplitud')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    plt.show()

# 2. Construcción de la interpolación Spline Cúbica
spline = CubicSpline(pq_t_hat, pq_hat, bc_type='natural')
n = np.arange(cant_muestras)

# Estimación de la línea de base y corrección del ECG
b_spline = spline(np.clip(n, pq_t_hat[0], pq_t_hat[-1]))
ecg_spline = ecg_one_leadruido - b_spline

print("Interpolación por Splines Cúbicos completada con éxito.")

#%% COMPARACIÓN DIRECTA: LÍNEA DE BASE ESTIMADA (MEDIANA VS SPLINE)

# Gráfico del registro completo
plt.figure(figsize=(14, 4.5))
plt.plot(b_mediana, label='Estimación b̂ por Mediana', color='darkorange', alpha=0.8, linewidth=1)
plt.plot(b_spline, label='Estimación b̂ por Spline Cúbico', color='purple', alpha=0.8, linewidth=1)
plt.title('Comparación de Estimaciones de Línea de Base en todo el Registro', fontweight='bold')
plt.xlabel('Muestras (#)')
plt.ylabel('Amplitud')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper right')
plt.show()

# Zooms representativos
zooms_comp = ([4000, 5500], [720000, 744000], [900000, 912000])

for inicio, fin in zooms_comp:
    zoom_r = np.arange(inicio, fin)
    plt.figure(figsize=(13, 4.5))
    plt.plot(zoom_r, ecg_one_leadruido[zoom_r], color='lightgray', label='ECG original con ruido')
    plt.plot(zoom_r, b_mediana[zoom_r], label='b̂ Mediana (201+601)', color='darkorange', linewidth=1.5)
    plt.plot(zoom_r, b_spline[zoom_r], label='b̂ Spline Cúbico', color='purple', linewidth=1.5)
    plt.title(f'Comparación de Estimaciones - Intervalo [{inicio}:{fin}]', fontweight='bold')
    plt.xlabel('Muestras (#)')
    plt.ylabel('Amplitud')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    plt.show()

# 1. Patrón conocido
qrs_p1 = qrs_pattern1.copy()

# Visualización del patrón original e invertido
plt.figure(figsize=(10, 3.5))
plt.plot(qrs_p1, label='Patrón QRS original (qrs_pattern1)', color='navy', linewidth=1.5)
plt.plot(qrs_p1[::-1], label='Patrón invertido temporalmente (qrs_p1[::-1])', color='crimson', linestyle='--', linewidth=1.5)
plt.title('Patrón QRS para el Filtro Adaptado', fontweight='bold')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.show()

#%% FILTRO ADAPTADO Y COMPENSACIÓN DE RETARDO

# 2. Filtrado adaptado sobre el ECG corregido por spline
qrs_matched = sig.lfilter(qrs_p1[::-1], 1, ecg_spline)

# 3. Normalización (media cero y desviación estándar 1) para comparación
ecg_norm = (ecg_spline - np.mean(ecg_spline)) / np.std(ecg_spline)
matched_norm = (qrs_matched - np.mean(qrs_matched)) / np.std(qrs_matched)

# 4. Medición del retardo en una región con latidos normales
# Medimos la distancia temporal entre el pico del ECG y el máximo del filtro adaptado
retardo = 69  # muestras (~69 ms)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 6), sharex=True, constrained_layout=True)

# Señal sin compensar
ax1.plot(ecg_norm, label='ECG normalizado', color='gray', alpha=0.7)
ax1.plot(matched_norm, label='Salida del Filtro Adaptado', color='darkorange', linewidth=1.2)
ax1.set_xlim(92000, 95000)
ax1.set_title('Salida del Filtro Adaptado (Sin Compensar Retardo)', fontweight='bold')
ax1.set_ylabel('Amplitud normalizada')
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='upper right')

# Señal compensada
ax2.plot(ecg_norm[:-retardo], label='ECG normalizado', color='gray', alpha=0.7)
ax2.plot(matched_norm[retardo:], label=f'Filtro Adaptado (Compensado {retardo} muestras)', color='teal', linewidth=1.2)
ax2.set_xlim(92000, 95000)
ax2.set_title('Salida del Filtro Adaptado con Retardo Compensado', fontweight='bold')
ax2.set_xlabel('Muestras (#)')
ax2.set_ylabel('Amplitud normalizada')
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='upper right')

plt.show()

#%% ENVOLVENTE MEDIANTE FILTRO DE ORDEN (PERCENTIL 90) Y DETECCIÓN DE LATIDOS

# Módulo rectificado de la salida
matched_abs = np.abs(matched_norm)

# Filtro de orden estadístico: ventana de 41 muestras, rank 36 (~percentil 90)
ventana = 41
rank = 36
envolvente_raw = sig.order_filter(matched_abs, np.ones(ventana), rank)

# Compensamos el retardo temporal
envolvente = envolvente_raw[retardo:]

# Comparación del módulo crudo vs envolvente suavizada
plt.figure(figsize=(13, 4.5))
plt.plot(matched_abs[92000+retardo:95000+retardo], label='Módulo rectificado sin suavizar', color='lightgray')
plt.plot(envolvente[92000:95000], label='Envolvente suavizada (Filtro de orden, Percentil 90)', color='darkorange', linewidth=2)
plt.title('Efecto del Filtro de Orden sobre la Salida del Filtro Adaptado', fontweight='bold')
plt.xlabel('Muestras (#)')
plt.ylabel('Amplitud')
plt.xlim(0, 3000)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.show()

# Detección de picos con find_peaks
# distance=400 muestras (400 ms de período refractario mínimo entre latidos)
# height=0.5 (umbral mínimo de amplitud para descartar ruido)
picos, propiedades = sig.find_peaks(envolvente, distance=400, height=0.5)

print(f"Cantidad total de latidos detectados por el algoritmo: {len(picos):,}")

# Verificación gráfica de las detecciones en una región del registro
zoom_det = np.arange(794800, 798500)
qrs_det_r = qrd_det[(qrd_det >= 794800) & (qrd_det < 798500)]
picos_r = picos[(picos >= 794800) & (picos < 798500)]

plt.figure(figsize=(14, 5))
plt.plot(zoom_det, ecg_norm[zoom_det], label='ECG normalizado (sin línea de base)', color='steelblue', alpha=0.6)
plt.plot(zoom_det, envolvente[zoom_det], label='Envolvente de detección', color='darkorange', linewidth=2)
plt.plot(picos_r, envolvente[picos_r], 'rx', markersize=9, markeredgewidth=2, label='Latidos detectados (find_peaks)')
for q in qrs_det_r:
    plt.axvline(q, color='green', linestyle='--', alpha=0.6, label='QRS de referencia' if q == qrs_det_r[0] else "")
plt.title('Verificación de Detecciones QRS frente a Referencias en Intervalo [794800:798500]', fontweight='bold')
plt.xlabel('Muestras (#)')
plt.ylabel('Amplitud normalizada')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper right')
plt.show()

#%% MATRIZ DE CONFUSIÓN, SENSIBILIDAD Y VALOR PREDICTIVO POSITIVO (VPP)

qrs_ref = np.sort(qrs_detections_ref)
picos_ordenados = np.sort(picos)

tolerancia = 100  # muestras (±100 ms)

TP = 0
i = 0
j = 0

# Algoritmo de emparejamiento temporal de eventos
while i < len(picos_ordenados) and j < len(qrs_ref):
    if abs(picos_ordenados[i] - qrs_ref[j]) <= tolerancia:
        TP += 1
        i += 1
        j += 1
    elif picos_ordenados[i] < qrs_ref[j]:
        i += 1
    else:
        j += 1

FP = len(picos_ordenados) - TP
FN = len(qrs_ref) - TP

sensibilidad = 100 * TP / len(qrs_ref)
vpp = 100 * TP / len(picos_ordenados)

print("=" * 45)
print("             MATRIZ DE CONFUSIÓN")
print("=" * 45)
print("                   Detectado       No detectado")
print(f"QRS real (Ref)     {TP:8d} (TP)   {FN:8d} (FN)   | Total Ref: {len(qrs_ref)}")
print(f"No QRS (Falsos)    {FP:8d} (FP)          -        | Total Det: {len(picos_ordenados)}")
print("=" * 45)
print(f"Sensibilidad (Recall):            {sensibilidad:.2f}%")
print(f"Valor Predictivo Positivo (VPP):   {vpp:.2f}%")
print("=" * 45)

# Gráfico general comparativo de detecciones vs referencias
plt.figure(figsize=(14, 4.5))
plt.plot(ecg_spline, label='ECG corregido (spline)', color='gray', alpha=0.5, linewidth=0.6)
plt.plot(picos_ordenados, ecg_spline[picos_ordenados], 'rx', markersize=6, label=f'Detecciones propias (N={len(picos_ordenados)})')
plt.plot(qrs_ref, ecg_spline[qrs_ref], 'go', fillstyle='none', markersize=6, label=f'Referencias cátedra (N={len(qrs_ref)})')
plt.title('Comparación Global: Detecciones Propias vs Referencias de la Cátedra', fontweight='bold')
plt.xlabel('Muestras (#)')
plt.ylabel('Amplitud')
plt.xlim(720000, 735000)  # Zoom representativo
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper right')
plt.show()

# Buscamos la referencia y la detección alrededor de la muestra 732.900 (para analizar no detecto bien)
print("Referencia cátedra:", qrs_ref[(qrs_ref >= 732800) & (qrs_ref <= 733000)])
print("Deteccion por filtro:", picos[(picos >= 732800) & (picos <= 733000)])
