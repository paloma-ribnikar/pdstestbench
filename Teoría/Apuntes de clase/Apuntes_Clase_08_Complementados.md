# Apuntes Complementados - Clase 8: Convolución por Bloques (OLA/OLS), Cuantización en ADC y Detección de Pulsos
**Fecha de la clase:** 27/08  
**Institución:** Universidad Nacional de San Martín (UNSAM) - Campus Miguelete  
**Materia:** Análisis y Procesamiento de Señales (APS) / Métodos Numéricos  
**Docentes:** Prof. Mariano y Ayudante David  
**Fuentes integradas:** Apuntes manuscritos (Páginas 3, 4 y 5 del PDF), transcripción de audio de clase (`transcripcion_bolivia_20_a_25.md`), script del profesor (`Mariano.py`) y script de evidencia entregado (`Evidencia.py`).

---

> [!NOTE]
> Este documento unifica y explica exhaustivamente todo el contenido teórico, algebraico, gráfico y computacional desarrollado en la **Clase 8**. Se abordan los algoritmos de filtrado rápido por bloques (**Overlap-Add** y **Overlap-Save**), el modelo físico y estadístico del **Conversor A/D (ADC)**, la cuantización, la deducción teórica de la varianza $P_q = q^2/12$, la regla de $6.02 B + 1.76\text{ dB}$, el test de incorrelación mediante autocorrelación, la detección de pulsos en ruido mediante correlación cruzada y la explicación línea por línea del código de evidencia entregado.

---

## Índice de la Clase
1. [Página 3: Convolución por Bloques — Algoritmos Overlap-Add (OLA) y Overlap-Save (OLS)](#página-3-convolución-por-bloques--algoritmos-overlap-add-ola-y-overlap-save-ols)
   - 1.1 Filtrado de Señales Continuas/Largas con FFT
   - 1.2 Algoritmo Overlap-Add (OLA)
   - 1.3 Algoritmo Overlap-Save (OLS)
2. [Página 4: Modelo Físico del ADC, Ruido y Deducción Teórica de Cuantización](#página-4-modelo-físico-del-adc-ruido-y-deducción-teórica-de-cuantización)
   - 2.1 Convolución Circular y Efectos de Borde
   - 2.2 Modelo de Ruido Analógico $n_A$ vs. Ruido de Cuantización $n_q$
   - 2.3 Densidad de Probabilidad Uniforme $U(-q/2, q/2)$ y Varianza $P_{n_q} = q^2/12$
   - 2.4 Deducción Formal de la $\text{SNR}_q$ y la "Regla de Pulgar" ($6\text{ dB/bit}$)
   - 2.5 Factor de Carga y Excursión Analógica
3. [Página 5: Detección de Pulsos por Correlación y Práctica en dB](#página-5-detección-de-pulsos-por-correlación-y-práctica-en-db)
   - 3.1 Unidades de Amplitud vs. Potencia en dB ($10\log |x|^2$ vs. $20\log |x|$)
   - 3.2 Principio de Correlación para Detectar Pulsos Ocultos en Ruido
   - 3.3 Parámetros del ADC en Laboratorio ($V_{max} = \sqrt{2}\text{ V}$, Rango $3.3\text{ V}$)
4. [Análisis Completo del Código de Evidencia (`Evidencia.py`)](#análisis-completo-del-código-de-evidencia-evidenciapy)
   - 4.1 Módulo 1: Definición de Parámetros y Generación de Senoidal + Ruido Gaussiano
   - 4.2 Módulo 2: FFT, Módulo en dB, Fase y Máscara de Fase
   - 4.3 Módulo 3: Bloque Cuantizador (`np.round(xx/qq)*qq`)
   - 4.4 Módulo 4: Histograma del Error Normalizado, Media y Varianza ($1/12$)
   - 4.5 Módulo 5: Autocorrelación del Ruido de Cuantización (Verificación de Ruido Blanco)

---

## Página 3: Convolución por Bloques — Algoritmos Overlap-Add (OLA) y Overlap-Save (OLS)

### 1.1 Filtrado de Señales Continuas/Largas con FFT

En el procesamiento en tiempo real o al trabajar con archivos de audio/señales muy largas ($L_x \to \infty$), no es viable aplicar la FFT a toda la señal completa debido al costo computacional $\mathcal{O}(L_x \log_2 L_x)$ y al retardo de latencia inaceptable.

Para resolver esto, se divide la señal de entrada $x[n]$ en bloques de longitud finita $L_x$ y se convolucionan secuencialmente con la respuesta al impulso del filtro $h[n]$ de longitud $L_h$ utilizando la FFT de tamaño $N$:

$$N \ge L_x + L_h - 1$$

Existen dos estrategias clásicas para reconstruir la convolución lineal continua a partir de las FFTs circulares de cada bloque: **Overlap-Add** y **Overlap-Save**.

---

### 1.2 Algoritmo Overlap-Add (OLA)

#### Principio de funcionamiento:
1. **División:** La señal $x[n]$ se divide en bloques **no solapados** de longitud $L_x$:
   $$x_m[n] = x[n + m L_x], \quad 0 \le n \le L_x - 1$$
2. **Zero-Padding:** Cada bloque $x_m[n]$ se rellena con ceros hasta alcanzar la longitud $N = L_x + L_h - 1$.
3. **Convolución Circular vía FFT:** Se calcula la FFT de $N$ puntos del bloque y del filtro:
   $$Y_m[k] = \text{FFT}_N(x_m[n]) \cdot \text{FFT}_N(h[n]) \implies y_m[n] = \text{IFFT}_N(Y_m[k])$$
   Dado que $N = L_x + L_h - 1$, **la convolución circular equivale exactamente a la convolución lineal de ese bloque**. Cada bloque producido $y_m[n]$ tiene una longitud de $N$ muestras.
4. **Solapamiento y Suma (Overlap & Add):** Las últimas $L_h - 1$ muestras de la salida del bloque $m$ se solapan en el tiempo con las primeras $L_h - 1$ muestras de la salida del bloque $m+1$ y se **suman**:

```
Bloque 1 (y_1):  [====================][ Cola L_h-1 ]
Bloque 2 (y_2):                        [ Cola L_h-1 ][====================][ Cola L_h-1 ]
                                              +
Salida Total:    [====================][  SUMA OLA  ][====================]
```

> [!TIP]
> **Ventaja de Overlap-Add:** Como se agrega el padding con ceros adecuado desde el principio, la circularidad de la FFT no contamina el bloque; la cola transitoria cae de forma natural en la región rellenada con ceros y la suma reconstruye la convolución lineal pura.

---

### 1.3 Algoritmo Overlap-Save (OLS)

#### Principio de funcionamiento:
1. **División con Solapamiento:** La señal $x[n]$ se divide en bloques que **se solapan intencionalmente** en $L_h - 1$ muestras. Cada bloque de entrada tiene una longitud total de $N = L_x + L_h - 1$.
2. **Convolución Circular directa vía FFT:** Se aplica la FFT de $N$ puntos directamente sobre el bloque solapado sin agregar ceros adicionales:
   $$Y_m[k] = \text{FFT}_N(x_m[n]) \cdot \text{FFT}_N(h[n]) \implies y_m[n] = \text{IFFT}_N(Y_m[k])$$
3. **Efecto de Aliasing Circular:** Como el bloque no se rellenó con ceros hasta la longitud completa lineal, las primeras $L_h - 1$ muestras de cada salida $y_m[n]$ quedan **corrompidas/contaminadas** por la rotación circular del transitorio de apagado.
4. **Descarte y Concatenación (Save & Discard):** Se **descartan** las primeras $L_h - 1$ muestras de cada bloque $y_m[n]$ y se **guardan/concatenan** las restantes $L_x$ muestras válidas directamente, sin realizar ninguna operación de suma.

```
Bloque y_m resultante (N pts):  [ CONTAMINADO (L_h - 1) ][ VÁLIDO (L_x) ]
Acción:                         [       DESCARTAR       ][   CONCATENAR ]
```

---

## Página 4: Modelo Físico del ADC, Ruido y Deducción Teórica de Cuantización

### 2.1 Convolución Circular y Efectos de Borde

Como se observó en los apuntes manuscritos (Página 4), la convolución circular es una consecuencia de operar en un dominio discreto y periódico. Los extremos de la señal se ven alterados por el fenómeno de borde (*aliasing temporal*).

---

### 2.2 Modelo de Ruido Analógico $n_A$ vs. Ruido de Cuantización $n_q$

El diagrama de bloques del canal de adquisición digital es:

```
 Senoidal Útil                     Entrada ADC                Salida Digital
    s[n] --------->( + )---------> s_R[n] ------->[ Q ]-------> s_Q[n]
                    ^                              B bits
                    |                              +/- Vf
                 n_A[n] Ruido Analógico
```

1. **Señal de entrada real ($s_R[n]$):** $s_R[n] = s[n] + n_A[n]$, donde $n_A[n] \sim \mathcal{N}(0, \sigma_A^2)$ representa el ruido térmico/analógico ambiental.
2. **Error de Cuantización ($n_q[n]$):** Es el error introducido por el redondeo digital al asignar la tensión continua a uno de los $2^B$ niveles discretos:
   $$n_q[n] = s_Q[n] - s_R[n]$$

---

### 2.3 Densidad de Probabilidad Uniforme y Varianza $P_{n_q} = q^2/12$

El error instantáneo $n_q$ está estrictamente acotado entre $-\frac{q}{2}$ y $+\frac{q}{2}$. Para señales complejas que varían abarcando múltiples escalones, el error se modela como una **variable aleatoria uniforme**:

$$p(n_q) = \begin{cases} \frac{1}{q} & \text{si } -\frac{q}{2} \le n_q \le +\frac{q}{2} \\ 0 & \text{en otro caso} \end{cases}$$

#### Deducción Formal de la Varianza / Potencia Teórica:
La potencia media de ruido $P_{n_q}$ es la esperanza matemática de $n_q^2$:

$$P_{n_q} = \sigma_q^2 = \mathbb{E}[n_q^2] = \int_{-q/2}^{q/2} x^2 \cdot \frac{1}{q} \, dx$$

$$\sigma_q^2 = \frac{1}{q} \left[ \frac{x^3}{3} \right]_{-q/2}^{q/2} = \frac{1}{3q} \left( \left(\frac{q}{2}\right)^3 - \left(-\frac{q}{2}\right)^3 \right) = \frac{1}{3q} \left( \frac{q^3}{8} + \frac{q^3}{8} \right) = \frac{1}{3q} \left( \frac{q^3}{4} \right) = \frac{q^2}{12}$$

> [!IMPORTANT]
> **Potencia de Ruido de Cuantización Teórica:**  
> $$P_{n_q} = \frac{q^2}{12} \quad [\text{Watts}]$$

---

### 2.4 Deducción Formal de la $\text{SNR}_q$ y la "Regla de Pulgar" ($6\text{ dB/bit}$)

Para una senoidal pura de amplitud máxima que ocupa la totalidad de la escala del ADC ($A = V_f \implies P_{\text{señal}} = \frac{V_f^2}{2}$):

El paso de cuantización es:
$$q = \frac{2 V_f}{2^B}$$

Reemplazando en la fórmula de la relación señal a ruido de cuantización ($\text{SQNR}$):

$$\text{SQNR}_{\text{dB}} = 10 \log_{10} \left( \frac{P_{\text{señal}}}{P_{n_q}} \right) = 10 \log_{10} \left( \frac{V_f^2 / 2}{q^2 / 12} \right) = 10 \log_{10} \left( \frac{V_f^2 / 2}{\frac{4 V_f^2}{12 \cdot 2^{2B}}} \right)$$

$$\text{SQNR}_{\text{dB}} = 10 \log_{10} \left( \frac{3}{2} \cdot 2^{2B} \right) = 10 \log_{10}(1.5) + 20 B \log_{10}(2)$$

$$\text{SQNR}_{\text{dB}} = 1.76 + 6.02 \cdot B \quad [\text{dB}]$$

> 💡 **"Regla de Pulgar" (Rule of Thumb):**  
> Cada bit ($B$) adicional de resolución en un ADC mejora la relación señal a ruido de cuantización en aproximadamente **$6\text{ dB}$**.

---

### 2.5 Factor de Carga y Excursión Analógica

El **Factor de Carga ($\gamma$)** expresa la proporción del rango dinámico que utiliza la señal de entrada:

$$\gamma = \frac{V_{max}}{V_{fs}}$$

Como explicaron el profesor Mariano y los ayudantes en la clase:
- Si la señal es muy pequeña ($\gamma \ll 1$), el paso $q$ representa un porcentaje alto de la señal, degradando drásticamente la SNR.
- Si la señal supera el 100% ($\gamma > 1$), ocurre **saturación (clipping)**, introduciendo armónicos de distorsión no lineal muy graves.
- **Rango óptimo recomendado:** Utilizar entre el **80% y 90%** de la excursión analógica ($\gamma \approx 0.8 \dots 0.9$).

---

## Página 5: Detección de Pulsos por Correlación y Práctica en dB

### 3.1 Unidades de Amplitud vs. Potencia en dB

En la práctica del laboratorio se enfatizó la distinción entre medir amplitud o potencia al convertir a escala logarítmica:

$$\text{Amplitud en dB} = 20 \log_{10}\left(\frac{|X|}{X_{\text{ref}}}\right)$$
$$\text{Potencia en dB} = 10 \log_{10}\left(\frac{|X|^2}{P_{\text{ref}}}\right)$$

Ambas expresiones son numéricamente equivalentes debido a la propiedad del exponente logarítmico: $10 \log_{10}(|X|^2) = 20 \log_{10}(|X|)$.

---

### 3.2 Principio de Correlación para Detectar Pulsos Ocultos en Ruido

En la segunda mitad del laboratorio (audios *Bolivia 22 y 25*), se explicó la técnica de **Filtro Adaptado / Correlación Cruzada** para detectar patrones o pulsos conocidos sepultados bajo niveles intensos de ruido:

$$R_{xy}[l] = \sum_{n} x[n] \cdot p[n - l]$$

- El ruido no correlacionado suma de forma incoherente tendiendo a cero.
- Al alinearse el retardo $l$ con la posición real del pulso $p[n]$, la correlación produce un **pico pronunciado y destacado**, superando ampliamente el piso de ruido.

---

### 3.3 Parámetros del ADC en Laboratorio

Para la experiencia en Python, se fijaron las siguientes especificaciones físicas:
- Frecuencia de muestreo: $f_s = 1000\text{ Hz}$ ($N = 1000$ muestras $\implies \Delta f = 1\text{ Hz}$).
- Amplitud senoidal de $1\text{ W}$ sobre resistencia de $1\,\Omega \implies V_{max} = \sqrt{2} \approx 1.414\text{ V}$.
- Conversor ADC de $B = 8$ bits con rango simétrico $V_{fs} = \pm 1.65\text{ V}$ (rango total de $3.3\text{ V}$).
- Paso de cuantización: $q = \frac{3.3}{2^8} = \frac{3.3}{256} \approx 0.01289\text{ V}$.

---

## Análisis Completo del Código de Evidencia (`Evidencia.py`)

A continuación se presenta y desglosa en detalle el script entregado como evidencia de la práctica de la Clase 8:

```python
# -*- coding: utf-8 -*-
"""
TP / Evidencia Clase 8 - Cuantización, Ruido y FFT
Autores: Ribnikar / Díaz
"""

#%% LIBRERÍAS
import numpy as np
import matplotlib.pyplot as plt

plt.close('all') # Cierra ventanas previas

#%% DEFINICIONES Y PARÁMETROS DEL ADC
fs = 1000   # Frecuencia de muestreo (Hz) -> F_Nyquist = 500 Hz
N = 1000    # Cantidad de muestras (Delta_f = 1 Hz)

# Senoidal útil de 1 Watt de potencia
vmax = np.sqrt(2)  # Amplitud pico (Volts)
dc = 0             # Valor medio / offset
ff = 3             # Frecuencia de la senoidal (Hz)
ph = 0             # Fase inicial (rad)

# Configuración del ADC
B = 8              # Bits de resolución
Vfs = 1.65         # Rango simétrico +/- 1.65 V (3.3 V total)
qq = 2 * Vfs / (2**B) # Paso de cuantización q

#%% FUNCIONES
def mi_funcion_sen(vmax=np.sqrt(2), dc=0, ff=1, ph=0, nn=N, fs=fs):
    tt = np.arange(nn) / fs
    xx = vmax * np.sin(2 * np.pi * ff * tt + ph) + dc
    return tt, xx

def generar_ruido(SNR=0, loc=dc, size=N):
    sigma_nq = 10**(-SNR/20)
    n_q = np.random.normal(loc=loc, scale=sigma_nq, size=size)
    return n_q
```

---

### Módulo 1: Generación Temporal con Distintos Niveles de SNR (20 dB, 0 dB, -10 dB)

```python
#%% CASOS DE SIMULACIÓN TEMPORAL
tt, xx = mi_funcion_sen(vmax=vmax, dc=0, ff=ff, ph=0, nn=N, fs=fs)

# Caso SNR = 20 dB (Señal muy clara)
n_q_20 = generar_ruido(SNR=20, loc=dc, size=N)
xx_ruidosa_20 = xx + n_q_20

# Caso SNR = 0 dB (Misma potencia de señal y ruido)
n_q_0 = generar_ruido(SNR=0, loc=dc, size=N)
xx_ruidosa_0 = xx + n_q_0

# Caso SNR = -10 dB (Ruido 10 veces más potente en amplitud)
n_q_m10 = generar_ruido(SNR=-10, loc=dc, size=N)
xx_ruidosa_m10 = xx + n_q_m10
```

> **Explicación Teórica:** Muestra el deterioro progresivo de la forma de onda temporal a medida que el ruido térmico domina sobre la senoidal.

---

### Módulo 2: FFT, Módulo en dB, Fase y Máscara de Fase

```python
#%% APLICO FFT A SENOIDAL LIMPIA Y RUIDOSA
ff_vector = np.fft.fftfreq(N, d=1/fs)

# Senoidal limpia
salida = np.fft.fft(xx)
salida_abs = np.absolute(salida)
salida_fase = np.angle(salida)

# Normalización de Potencia: ((2 * |X|) / N)^2 / 2
salida_potencia = ((2 * salida_abs[:N//2]) / N)**2 / 2

# Senoidal ruidosa (SNR = -10 dB)
salida_ruidosa = np.fft.fft(xx_ruidosa_m10)
salida_ruidosa_abs = np.absolute(salida_ruidosa)
salida_ruidosa_fase = np.angle(salida_ruidosa)
salida_ruidosa_potencia = ((2 * salida_ruidosa_abs[:N//2]) / N)**2 / 2
```

> **MÁSCARA DE FASE (`salida_fase[salida_abs < 1e-5] = 0`):**  
> Como explicó el profesor Mariano, cuando la magnitud espectral es casi nula (piso de ruido numérico), la fase de `np.angle()` arroja valores aleatorios ruidosos ("serrucho"). Aplicar la máscara limpia el gráfico eliminando valores sin energía significativa.

---

### Módulo 3: Algoritmo del Cuantizador y Extracción del Error

```python
#%% PROCESO DE CUANTIZACIÓN DIGITAL
# Algoritmo de 4 pasos condensado:
xx_q = np.round(xx / qq) * qq  # Normalizar -> Redondear -> Escalar

# Error / Ruido de Cuantización instantáneo
nq = xx_q - xx

# Gráfica de la señal escalonada y del error
plt.figure()
plt.plot(xx, 'x', label='Analógica s_R')
plt.plot(xx_q, ':v', label='Cuantizada s_Q')
plt.title("Señal Cuantizada (Escalones q)")

plt.figure()
plt.plot(nq / qq, ':x')
plt.title("Ruido de Cuantización Normalizado [en unidades de q]")
plt.xlabel('Muestra n')
plt.ylabel('nq / q')
plt.grid(True)
plt.show()
```

---

### Módulo 4: Histograma del Error Normalizado, Media y Varianza ($1/12$)

```python
#%% DISTRIBUCIÓN Y ESTADÍSTICA DEL RUIDO DE CUANTIZACIÓN
nq_normalizado = nq / qq

# Histograma de densidad de probabilidad
plt.figure()
plt.hist(nq_normalizado, bins=20, density=True, color='skyblue', edgecolor='black')
plt.title('Distribución del Ruido de Cuantización')
plt.xlabel('Error [q]')
plt.ylabel('Densidad de Probabilidad')
plt.grid(True)
plt.show()

# Cálculo numérico de momentos estadísticos
media_nq = np.mean(nq_normalizado)
varianza_nq = np.var(nq_normalizado)

print(f"Media del ruido de cuantización = {media_nq:.6f} (Teórico: 0.0)")
print(f"Varianza del ruido = {varianza_nq:.6f} (Teórico: 1/12 = 0.083333)")
```

> **Verificación Empírica:**  
> Se comprueba en la consola que la varianza estimada por la simulación es aproximadamente **$0.0833 \approx 1/12$**, validando cuantitativamente la deducción teórica de la integral de varianza de la distribución uniforme.

---

### Módulo 5: Autocorrelación del Ruido de Cuantización (Verificación de Ruido Blanco)

```python
#%% AUTOCORRELACIÓN DEL RUIDO DE CUANTIZACIÓN
autocorr = np.correlate(nq_normalizado, nq_normalizado, mode='full')
autocorr_norm = autocorr / np.max(autocorr) # Normalizado a pico 1 en lag 0

retardos = np.arange(-(N-1), N)

plt.figure()
plt.plot(retardos, autocorr_norm)
plt.xlim(-50, 50)
plt.xlabel('Retardo (Lag l)')
plt.ylabel('Autocorrelación Normalizada')
plt.title('Autocorrelación del Ruido de Cuantización (Demostración de Delta / Incorrelación)')
plt.grid(True)
plt.show()
```

> [!TIP]
> **Conclusión Físico-Matemática:**  
> La gráfica de autocorrelación del error de cuantización arroja un pico aislado en el retardo $l=0$ y valores prácticamente nulos para todo $l \neq 0$. Esto demuestra cuantitativamente que el ruido de cuantización se comporta como un **proceso estocástico blanco e incorrelado en el tiempo**.

---

> **Apuntes de Clase 8 completados.**  
> Todos los contenidos de convolución por bloques, cuantización en ADC, deducciones estadísticas, correlación de pulsos y códigos resueltos han sido integrados con máxima precisión.
