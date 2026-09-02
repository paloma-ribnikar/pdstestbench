# Apuntes Complementados - Clase 7: Convolución Lineal vs. Circular y Simetrías de la DFT
**Fecha de la clase:** 26/08  
**Institución:** Universidad Nacional de San Martín (UNSAM) - Campus Miguelete  
**Materia:** Análisis y Procesamiento de Señales (APS) / Métodos Numéricos  
**Docentes:** Prof. Mariano y Ayudante David  
**Fuentes integradas:** Apuntes manuscritos (Páginas 1 y 2 del PDF), transcripción de audio de clase (`transcripcion_san_martin_11.md`), y script práctico del profesor (`Mariano.py`).

---

> [!NOTE]
> Este documento unifica y profundiza el desarrollo teórico, algebraico, gráfico y computacional de la **Clase 7**. Se analiza en detalle la convolución lineal frente a la convolución circular, la respuesta en frecuencia de un filtro promediador (Boxcar), las propiedades de simetría conjugada de la DFT ($N=7$ impar vs. $N=8$ par), la grilla frecuencial y el código en Python implementado en clase.

---

## Índice de la Clase
1. [Página 1: Convolución Lineal — Resolución Analítica y Numérica](#página-1-convolución-lineal--resolución-analítica-y-numérica)
   - 1.1 Modelo del Sistema LTI y Filtro Promediador (Boxcar)
   - 1.2 Resolución Analítica de la Respuesta del Filtro
   - 1.3 Resolución Numérica en el Pizarrón y Expansión Vectorial
   - 1.4 Modos de `numpy.convolve` (`full`, `same`, `valid`) y Transitorios
2. [Página 2: Convolución Circular, Circular Shift y Simetrías de la DFT](#página-2-convolución-circular-circular-shift-y-simetrías-de-la-dft)
   - 2.1 Definición Matemática de la Convolución Circular
   - 2.2 Desplazamiento Circular (*Circular Shift*) Módulo $N$
   - 2.3 Simetría Conjugada de la DFT y Frecuencia de Nyquist ($N=8$ vs. $N=7$)
3. [Código de Laboratorio del Profesor (`Mariano.py`)](#código-de-laboratorio-del-profesor-marianopy)
   - 3.1 Generación de Señal Senoidal y Filtro FIR Promediador
   - 3.2 Convolución Circular vía FFT/IFFT vs. Convolución Lineal con `scipy.signal.convolve`
   - 3.3 Análisis Comparativo y Conclusiones Gráficas

---

## Página 1: Convolución Lineal — Resolución Analítica y Numérica

### 1.1 Modelo del Sistema LTI y Filtro Promediador (Boxcar)

En la primera parte de la clase, el profesor Mariano planteó un ejercicio práctico de filtrado empleando un sistema discreto lineal e invariante en el tiempo (LTI).

#### Definición de la señal de entrada:
$$x[n] = \sin\left(\omega_0 n\right) = \sin\left(\frac{2\pi}{7} n\right)$$

donde la frecuencia angular discreta es $\omega_0 = \frac{2\pi}{7}\text{ rad/muestra}$ (es decir, la senoidal completa realiza un ciclo exacto en $N=7$ muestras).

#### Definición de la respuesta al impulso del filtro ($h[n]$):
Se utiliza un **filtro promediador de ventana rectangular (Boxcar)** de longitud $S = 5$ muestras:

$$h[n] = \begin{cases} \frac{1}{S} = \frac{1}{5} & \text{para } n = 1, 2, \dots, S \\ 0 & \text{en otro caso} \end{cases}$$

> [!NOTE]
> Aunque el filtro está pensado para filtrado en tiempo real, operativamente realiza la suma móvil ponderada de $S$ muestras contiguas, comportándose como un **filtro pasabajo discreto**.

---

### 1.2 Resolución Analítica de la Respuesta del Filtro

Dado que el sistema es LTI, la entrada de una senoidal pura produce a la salida otra **senoidal de la misma frecuencia $\omega_0$**, pero modificada en **amplitud** y **fase** por la respuesta en frecuencia del filtro $H(e^{j\omega})$:

$$y[n] = x[n] * h[n] = \mathcal{F}^{-1} \left\{ X(e^{j\omega}) \cdot H(e^{j\omega}) \right\}$$

#### Expresión en Exponenciales Complejas:
Expresando la señal de entrada como:
$$x[n] = \frac{e^{j\omega_0 n} - e^{-j\omega_0 n}}{2j}$$

La respuesta del filtro pasabajo promediador de $S$ puntos desplazado tiene por respuesta en frecuencia:

$$H(e^{j\omega}) = \sum_{n=1}^{S} \frac{1}{S} e^{-j\omega n} = \frac{1}{S} e^{-j \omega \frac{S+1}{2}} \frac{\sin\left(\frac{S \omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)}$$

Evaluando en $\omega = \omega_0 = \frac{2\pi}{7}$ para $S = 5$:

$$Y(n) = \frac{1}{2j} \cdot \frac{1}{S} \frac{\sin\left(\frac{S \omega_0}{2}\right)}{\sin\left(\frac{\omega_0}{2}\right)} \left[ e^{j(\omega_0 n - 3\omega_0)} - e^{-j(\omega_0 n - 3\omega_0)} \right]$$

Reagrupando en forma trigonométrica:

$$Y(n) = \underbrace{\frac{1}{S} \left( \frac{\sin\left(\frac{S \omega_0}{2}\right)}{\sin\left(\frac{\omega_0}{2}\right)} \right)}_{A (\text{Ganancia de Amplitud})} \cdot \sin(\omega_0 n - 3\omega_0)$$

#### Análisis de la fórmula analítica:
1. **Factor de Amplitud ($A$):** Corresponde al valor de la **función Sinc discreta (Kernel de Dirichlet)** del filtro evaluado en $\omega_0 = 2\pi/7$. Modifica la amplitud pico de la senoidal.
2. **Desfasaje / Retardo de Grupo:** Aparece un retardo de $3$ muestras ($-3\omega_0$), originado por el centro de gravedad del filtro promediador de $5$ muestras ($n=1, 2, 3, 4, 5 \implies \text{centro en } n=3$).
3. **Ceros de la Sinc:** Cuando el tamaño del bloque coincide con un múltiplo entero, el filtro anula exactamente componentes espectrales (ceros de transmisión del filtro).

---

### 1.3 Resolución Numérica en el Pizarrón y Expansión Vectorial

Para contrastar el resultado analítico con el cálculo computacional, el profesor guio a los alumnos a resolver a mano la convolución lineal discreta para $N = 7$ puntos de $x[n]$ y $h[n]$:

#### Muestras de la señal ($x_1 \in \mathbb{R}^7$):
$$x_1 = [0,\; 0.782,\; 0.975,\; 0.434,\; -0.434,\; -0.975,\; -0.782]$$

#### Muestras del filtro ($h \in \mathbb{R}^7$):
$$h = [0,\; 1/5,\; 1/5,\; 1/5,\; 1/5,\; 1/5,\; 0]$$

#### Dimensión del espacio vectorial resultante:
La convolución lineal entre dos secuencias de longitudes $L_x = 7$ y $L_h = 7$ genera un vector de salida en $\mathbb{R}^{L_x + L_h - 1} = \mathbb{R}^{7+7-1} = \mathbb{R}^{13}$.

#### Algoritmo del Producto Escalar Móvil:
Matemáticamente, la convolución lineal se define como:

$$y[n] = x[n] * h[n] = \sum_{m=-\infty}^{\infty} x[m] \cdot h[n - m]$$

Para computar esto numéricamente, se realiza un **inversión temporal (flip)** de $h[m]$ y un **desplazamiento gradual ($n$)**, calculando el producto escalar entre los dos vectores alineados:

```
Paso n=0:  X expandido:  [0, 0, 0, 0, 0, 0, X0, X1, X2, X3, X4, X5, X6]
           h_flipped:    [0, 1/5, 1/5, 1/5, 1/5, 1/5, 0, 0, 0, 0, 0, 0, 0]
           y[0] = 0

Paso n=1:  h_flipped(1): [0, 0, 1/5, 1/5, 1/5, 1/5, 1/5, 0, 0, 0, 0, 0, 0]
           y[1] = 0

Paso n=2:  Solape inicial de 1 muestra con X0:
           y[2] = X0 * (1/5) = 0 * 0.2 = 0 (o primera muestra no nula 0.782 * 0.2 = 0.156)

Valores numéricos resultantes:
y[0] = 0.000
y[1] = 0.000
y[2] = 0.156
y[3] = 0.351
y[4] = 0.438
y[5] = 0.351
y[6] = -0.156
```

---

### 1.4 Modos de `numpy.convolve` (`full`, `same`, `valid`) y Transitorios

Durante la clase, se analizó cómo la librería `numpy` implementa la función `numpy.convolve(a, b, mode)` y qué significa cada modo de cálculo:

```python
import numpy as np

y_full = np.convolve(x, h, mode='full')   # Longitud N + M - 1 = 13
y_same = np.convolve(x, h, mode='same')   # Longitud max(N, M) = 7
y_valid = np.convolve(x, h, mode='valid') # Longitud N - M + 1 = 1
```

```
CONVOLUCIÓN LINEAL FULL (Longitud 13):
+--------------------+------------------------+--------------------+
|  Transitorio de    |    Régimen Permanente  |   Transitorio de   |
|  Entrada (Prendido)|  (Solapamiento Total)  |   Salida (Apagado) |
+--------------------+------------------------+--------------------+
0                    L_h                      L_x                 12
```

> [!IMPORTANT]
> **Aclaración del Profesor Mariano sobre las muestras "Válidas":**  
> "No tomen lo del modo `valid` de numpy como 'válido vs. inválido' en términos absolutos. Las muestras de los transitorios de entrada y salida son los valores **reales y correctos** de la convolución de dos señales finitas. El modo `valid` únicamente retorna la región donde los dos vectores están totalmente solapados sin necesitar ceros de relleno (*padding*)."

---

## Página 2: Convolución Circular, Circular Shift y Simetrías de la DFT

### 2.1 Definición Matemática de la Convolución Circular

A diferencia de la convolución lineal, la **Convolución Circular** (o periódica) opera sobre señales definidas en un dominio periódico o de longitud fija $N$:

$$y[n] = x[n] \circledast h[n] = \sum_{m=0}^{N-1} x[m] \cdot h[(n - m) \pmod N]$$

donde el índice $(n - m) \pmod N$ representa el **resto de la división entera** por $N$. Esto obliga a que cualquier muestra que sea desplazada fuera del rango $[0, N-1]$ reingrese por el extremo opuesto.

---

### 2.2 Desplazamiento Circular (*Circular Shift*) Módulo $N$

En los apuntes manuscritos (Página 2), se detalla explícitamente cómo rota el vector del filtro $h[n]$ según el índice de tiempo $n$:

Sea $h[n] = [0,\; 1/5,\; 1/5,\; 1/5,\; 1/5,\; 1/5,\; 0]$ con $N=7$:

1. **Para $n = 0$ ($h[(-m) \pmod 7]$):**
   $$h[(-m)_7] = [0,\; 1/5,\; 1/5,\; 1/5,\; 1/5,\; 1/5,\; 0]$$
2. **Para $n = 1$ ($h[(1-m) \pmod 7]$):**
   $$h[(1-m)_7] = [0,\; 0,\; 1/5,\; 1/5,\; 1/5,\; 1/5,\; 1/5]$$
3. **Para $n = 2$ ($h[(2-m) \pmod 7]$):**
   $$h[(2-m)_7] = [1/5,\; 0,\; 0,\; 1/5,\; 1/5,\; 1/5,\; 1/5]$$

> 💡 **Explicación Intuitiva:** El desplazamiento circular actúa como una ruleta o buffer circular. Las muestras desplazadas a la derecha rotan hacia el inicio del vector, provocando que la cola de la señal se mezcle con el frente.

---

### 2.3 Simetría Conjugada de la DFT y Frecuencia de Nyquist ($N=8$ vs. $N=7$)

En la última sección del pizarrón de la Clase 7 (Página 2), el profesor analizó la estructura del espectro de la DFT para secuencias reales según la paridad de $N$:

Para toda señal real $x[n] \in \mathbb{R}$, se cumple la **Simetría Hermitiana**:

$$X[k] = X^*[N - k]$$

```
CASO 1: N = 8 (Par)
Bins: [0, 1, 2, 3, 4, 5, 6, 7]
       |  |  |  |  |  |  |  |
       DC \--+--+--|--+--+--/ Conjugados
                   Nyquist (k=4, estrictamente real: X[4] = X*[4])

Parejas Conjugadas:
- X[1] = X*[7]
- X[2] = X*[6]
- X[3] = X*[5]
- Bin k=4 (Nyquist fs/2): cae EXACTAMENTE en la grilla entera.

CASO 2: N = 7 (Impar)
Bins: [0, 1, 2, 3, 4, 5, 6]
       |  |  |  |  |  |  |
       DC \--+--+--+--+--/ Conjugados

Parejas Conjugadas:
- X[1] = X*[6]
- X[2] = X*[5]
- X[3] = X*[4]
- ¡NO existe bin entero para Nyquist! (N/2 = 3.5 no es un entero).
```

> [!WARNING]
> **Consecuencia en Procesamiento Digital:**  
> Cuando $N$ es impar ($N=7$), no existe una muestra correspondiente a la frecuencia exacta de Nyquist en la grilla discreta. La máxima frecuencia resoluble sin solapamiento se ubica en la componente conjugada $k=3$.

---

## Código de Laboratorio del Profesor (`Mariano.py`)

A continuación se transcribe y complementa teóricamente el código que programó el profesor Mariano en la computadora durante la clase práctica para demostrar la diferencia entre convolución circular mediante FFT y convolución lineal:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Código de Clase 7 / 8 - Prof. Mariano
Demostración de Convolución Circular mediante FFT vs. Convolución Lineal
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

# ============================================================
# 1. PARÁMETROS Y GENERACIÓN DE SEÑALES
# ============================================================
N = 16  # Cantidad de muestras del bloque
k = 2   # Frecuencia: 2 ciclos completos en N muestras (f = k/N = 2/16)

n = np.arange(N)
# Señal senoidal pura sintonizada en la grilla
x = np.sin(2 * np.pi * n * k / N)

# Respuesta al impulso: Filtro FIR promediador de 5 muestras (Boxcar)
h = np.zeros(N)
h[:5] = 1/5  # h[n] = 0.2 para n=0..4, luego ceros hasta N-1

# Kernel ajustado a longitud corta (5 muestras) para convolución lineal
h5 = np.zeros(5)
h5[:5] = 1/5

# ============================================================
# 2. CONVOLUCIÓN CIRCULAR VÍA FFT (PRODUCTO EN FRECUENCIA)
# ============================================================
# Por el Teorema de Convolución en la DFT:
# F{x[n] (o) h[n]} = X[k] . H[k]
X = np.fft.fft(x)
H = np.fft.fft(h)
y_fft = np.fft.ifft(X * H).real  # Se toma la parte real eliminando residuos numéricos

# ============================================================
# 3. CONVOLUCIÓN LINEAL (scipy.signal.convolve)
# ============================================================
# Salida de longitud L_x + L_h - 1 = 16 + 5 - 1 = 20 muestras
y_h5 = sig.convolve(x, h5, mode='full')

# ============================================================
# 4. GRAFICACIÓN Y COMPARACIÓN
# ============================================================
plt.figure(figsize=(10, 5))
plt.plot(x, ':v', label='Señal de entrada x[n]')
plt.plot(y_fft, ':x', label='Convolución Circular (FFT - 16 pts)')
plt.plot(y_h5, ':o', label='Convolución Lineal (sig.convolve - 20 pts)')

plt.title('Comparación: Convolución Circular vs. Convolución Lineal')
plt.xlabel('Muestra n')
plt.ylabel('Amplitud')
plt.legend(loc='upper right')
plt.grid(True)
plt.tight_layout()
plt.show()
```

---

### Explicación Bloque por Bloque del Código

1. **Definición de $x[n]$ y $h[n]$:** Se genera una senoidal con $k=2$ ciclos en $N=16$ muestras. El filtro $h$ posee 5 coeficientes iguales a $0.2$.
2. **Producto espectral (`np.fft.fft`):** Al multiplicar $X[k] \cdot H[k]$ en la FFT de $N=16$ puntos e invertir con `ifft`, se obtiene **consecuentemente la convolución circular** de 16 puntos. La transitoriedad de salida se pliega y suma sobre el inicio.
3. **Convolución Lineal (`sig.convolve`):** Al usar el kernel $h_5$ de 5 muestras sobre $x[n]$ de 16 muestras, la salida lineal se extiende hasta $N + M - 1 = 20$ muestras, mostrando el transitorio de apagado entre las muestras 16 y 19.

---

> **Apuntes de Clase 7 completados.**  
> Todos los conceptos teóricos, demostraciones algebraicas, esquemas del pizarrón y códigos de la Clase 7 han sido totalmente documentados.
