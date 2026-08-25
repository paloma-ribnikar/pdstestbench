# Apuntes Complementados - Clase 6: Análisis y Procesamiento de Señales (APS)
**Fecha de la clase:** 20/08  
**Institución:** UNSAM (Universidad Nacional de San Martín) - Campus Miguelete  
**Docentes:** Prof. Mariano y Ayudante David  
**Fuentes integradas:** Apuntes manuscritos propios (páginas 1 a 4), transcripciones de audios de clase (*Miguelete 28, 29 y 30*).

---

> [!NOTE]
> Este documento toma como columna vertebral la estructura y cronología de los apuntes manuscritos de la Clase 6. Se completan y aclaran todas las demostraciones algebraicas, gráficos, propiedades de la DFT, el algoritmo FFT con direccionamiento *Bit Reversal*, y la verificación numérica en Python realizada en el laboratorio.

---

## Índice de la Clase
1. [Página 1: Propiedades de la Transformada y Convolución Circular](#página-1-propiedades-de-la-transformada-y-convolución-circular)
   - 1.1 Inversión Temporal y Conjugación
   - 1.2 Convolución Circular vs. Convolución Lineal
   - 1.3 Análisis Gráfico y Equivalencia entre Convoluciones
2. [Página 2: Ejercicio Analítico de la DFT, Grilla Frecuencial y Principio de la FFT](#página-2-ejercicio-analítico-de-la-dft-grilla-frecuencial-y-principio-de-la-fft)
   - 2.1 Planteo y Desarrollo Algebraico para $x[n] = \cos(\pi n / 2)$ con $N=8$
   - 2.2 Resolución Espectral ($\Delta f$), Circunferencia Unitaria y Sintonización en la Grilla
   - 2.3 Introducción a la FFT (Algoritmo de Cooley-Tukey y Twiddle Factors)
3. [Página 3: Diagrama de Mariposa, Bit Reversal y Simetrías de la DFT](#página-3-diagrama-de-mariposa-bit-reversal-y-simetrías-de-la-dft)
   - 3.1 Estructura del Diagrama de Mariposa (Radix-2 DIT)
   - 3.2 Direccionamiento de Memoria *Bit Reversal*
   - 3.3 Propiedades de Simetría Compleja para Señales Reales
4. [Página 4: Verificación Numérica en Python (`numpy.fft.fft`) y Espectro de Ruido](#página-4-verificación-numérica-en-python-numpyfftfft-y-espectro-de-ruido)
   - 4.1 Experiencia en el Laboratorio: Lectura de la Matriz Compleja ($J500$)
   - 4.2 Ubicación de Bins Directos e Imágenes ($k$ y $N-k$)
   - 4.3 Espectro Plano del Ruido Blanco

---

## Página 1: Propiedades de la Transformada y Convolución Circular

### 1.1 Inversión Temporal y Conjugación

Al trabajar en el dominio discreto con la **Transformada de Fourier de Tiempo Discreto (DTFT)** y la **Transformada Discreta de Fourier (DFT)**, se cumplen las siguientes relaciones básicas:

1. **Transformada directa:**
   $$x[n] \overset{\mathcal{F}}{\longleftrightarrow} X[k]$$

2. **Inversión temporal:**
   $$x[-n] \overset{\mathcal{F}}{\longleftrightarrow} X^*[k] \quad (\text{Espectro conjugado})$$

3. **Producto en el tiempo $\longleftrightarrow$ Convolución en frecuencia:**
   $$x[n] \cdot y[n] \overset{\mathcal{F}}{\longleftrightarrow} X[k] \circledast Y[k]$$

---

### 1.2 Convolución Circular vs. Convolución Lineal

> [!IMPORTANT]
> **¿Por qué aparece la Convolución Circular?**  
> En la DFT, tanto el dominio del tiempo como el de la frecuencia están **discretizados y son periódicos** de período $N$. Debido a esta periodicidad inherente en ambos dominios, un desplazamiento temporal estándar $n - k$ se convierte automáticamente en un **desplazamiento circular (módulo $N$)**.

La expresión de la **Convolución Circular** se define como:

$$y[n] = x[n] \circledast h[n] = \sum_{k=0}^{N-1} x[k] \cdot h[(n - k)_N]$$

donde el subíndice $(n - k)_N$ representa la operación módulo $N$:

$$h[(n-k)_N] = h[(n - k) \pmod N]$$

#### Condiciones de Contorno Periódicas:
$$h[0] = h[N]$$
$$h[-1] = h[N-1]$$

---

### 1.3 Análisis Gráfico y Equivalencia entre Convoluciones

En los apuntes manuscritos se ilustra la diferencia entre ambos tipos de convolución para una señal de duración finita de $N=4$ muestras:

```
CONVOLUCIÓN LINEAL (Longitud salida L_y = L_x + L_h - 1):
      +-----------------+-----------------+-----------------+
      | Transitorio de  |    Régimen      | Transitorio de  |
      | Entrado/Prendido|   Permanente    | Apagado/Salida  |
      +-----------------+-----------------+-----------------+
     0                 L_h               L_x               L_y

CONVOLUCIÓN CIRCULAR (Longitud salida fija N):
      +-----------------------------------------------------+
      |   Bloque B1 + Solapamiento de Cola B2 (Aliasing)    |
      +-----------------------------------------------------+
     0                                                     N-1
```

1. **Convolución Lineal:** La salida se expande en el tiempo. Consta de tres zonas bien diferenciadas:
   - *Transitorio prendido:* La señal entra al filtro.
   - *Régimen permanente:* La señal cubre totalmente el ancho del filtro.
   - *Transitorio apagado:* La señal sale del filtro.
2. **Convolución Circular:** La salida queda "atrapada" dentro de un bloque de tamaño $N$. Si el tamaño $N$ de la DFT es menor que $L_x + L_h - 1$, la cola del transitorio de apagado (bloque B2) se pliega y se suma circularmente sobre el inicio de la señal (bloque B1). Esto produce **solapamiento temporal (aliasing)**.

> [!TIP]
> **Equivalencia entre ambas convoluciones:**  
> Para lograr que la Convolución Circular dé **exactamente el mismo resultado** que la Convolución Lineal, se debe aplicar **Zero-Padding** (rellenar con ceros las señales) hasta que la cantidad total de puntos $N$ sea:
> $$N \ge L_x + L_h - 1$$

---

## Página 2: Ejercicio Analítico de la DFT, Grilla Frecuencial y Principio de la FFT

### 2.1 Planteo y Desarrollo Algebraico para $x[n] = \cos(\pi n / 2)$ con $N=8$

En el pizarrón, el ayudante David planteó el cálculo analítico directo de la DFT de $N=8$ puntos de una senoidal discreta:

$$x[n] = \cos\left(2\pi f n\right) = \cos\left(\frac{\pi}{2} n\right) \quad \text{con } f = \frac{1}{4}, \; N = 8$$

La definición formal de la DFT es:

$$X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j \frac{2\pi}{N} k n}, \quad k = 0, 1, \dots, N-1$$

Sustituyendo $N = 8$ y expresando el coseno según la identidad de Euler $\cos(\theta) = \frac{1}{2}\left(e^{j\theta} + e^{-j\theta}\right)$:

$$X[k] = \sum_{n=0}^{7} \frac{1}{2} \left( e^{j \frac{\pi}{2} n} + e^{-j \frac{\pi}{2} n} \right) e^{-j \frac{2\pi}{8} k n}$$

Simplificando los exponentes:

$$X[k] = \frac{1}{2} \sum_{n=0}^{7} \left( e^{j \frac{\pi}{4} (2 - k) n} + e^{-j \frac{\pi}{4} (2 + k) n} \right)$$

 Aplicando la propiedad de ortogonalidad del kernel exponencial discreto:

$$\sum_{n=0}^{N-1} e^{j \frac{2\pi}{N} m n} = N \cdot \delta(m \pmod N)$$

Para $N=8$:
1. El primer término suma $8$ únicamente cuando $(2 - k) \equiv 0 \pmod 8 \implies k = 2$.
2. El segundo término suma $8$ únicamente cuando $(2 + k) \equiv 0 \pmod 8 \implies k = -2 \equiv 6 \pmod 8$.

Por lo tanto:

$$X[k] = \frac{1}{2} \cdot 8 \cdot \delta((k - 2)_8) + \frac{1}{2} \cdot 8 \cdot \delta((k - 6)_8) = 4 \delta[k - 2] + 4 \delta[k - 6]$$

#### Espectro resultante de la DFT ($N=8$):
```
      X[k]
        ^
      4 |       | (k=2)                   | (k=6)
        |       |                         |
     ---+-------+----+----+----+----+-----+----+-----> k
        0       2    3    4    5    6     7
```
Aparecen **dos deltas impulsivas de magnitud $N/2 = 4$** ubicadas exactamente en las frecuencias discretas $k = 2$ y $k = 6$.

---

### 2.2 Resolución Espectral ($\Delta f$), Circunferencia Unitaria y Sintonización en la Grilla

El dominio discreto de la frecuencia $k$ equivale a dividir la **circunferencia trigonométrica de radio unitario** en $N$ partes iguales:

```
                Dom k (N=8)
                   k=2 (90°)
                    |  
         k=3 \      |      / k=1
              \     |     /
   k=4 (180°) -------+------- k=0 (0°)
              /     |     \
         k=5 /      |      \ k=7
                    |  
                   k=6 (270°)
```

La **Resolución Espectral ($\Delta f$)** (distancia entre dos bins consecutivos de frecuencia) se define como:

$$\Delta f = \frac{f_s}{N} \quad [\text{Hz/bin}] \qquad \text{o en frecuencia angular: } \Delta \omega = \frac{2\pi}{N} \quad [\text{rad/muestra}]$$

En el ejercicio, $\Delta \omega = \frac{2\pi}{8} = \frac{\pi}{4}$. Reescribiendo el coseno en función de la resolución:

$$x[n] = \cos(2 \cdot \Delta \omega \cdot n) = \cos\left(2 \cdot \frac{\pi}{4} \cdot n\right)$$

> [!TIP]
> **El concepto de "Sintonizar en la Grilla" (Prof. Mariano):**  
> Si la frecuencia de la senoidal de entrada es un **múltiplo entero exacto de la resolución espectral** ($f_0 = k_0 \cdot \Delta f$), la energía de la senoidal cae perfectamente en un "bin" $k_0$ y el espectro es una **delta de Dirac pura**.  
> Si la frecuencia no cae en un número entero de la grilla, la energía se "derrama" hacia los bins vecinos, produciendo el fenómeno conocido como **Fuga Espectral (Spectral Leakage)**.

---

### 2.3 Introducción a la FFT (Algoritmo de Cooley-Tukey y Twiddle Factors)

Calcular la DFT de forma directa requiere realizar $N$ multiplicaciones complejas para cada uno de los $N$ bins:

$$\text{Complejidad Computacional Directa DFT} \implies \mathcal{O}(N^2)$$

Para $N=1000$ muestras, se requerirían $1.000.000$ de operaciones.

Para optimizar esto, se utiliza el **Factor de Giro (Twiddle Factor)** $W_N$:

$$W_N = e^{-j \frac{2\pi}{N}} \implies W_N^{k n} = e^{-j \frac{2\pi}{N} k n}$$

La clave del algoritmo de **Transformada Rápida de Fourier (FFT)** (Cooley-Tukey) consiste en separar la sumatoria original de $N$ puntos en **dos DFTs más pequeñas de $N/2$ puntos** (muestras pares e impares):

$$X[k] = \sum_{n=0}^{N/2 - 1} x[2n] W_{N/2}^{k n} + W_N^k \sum_{n=0}^{N/2 - 1} x[2n+1] W_{N/2}^{k n}$$

$$X[k] = \text{DFT}_{N/2}(x_{\text{pares}}) + W_N^k \cdot \text{DFT}_{N/2}(x_{\text{impares}})$$

Esta propiedad recursiva reduce drásticamente la complejidad computacional a:

$$\text{Complejidad Computacional FFT} \implies \mathcal{O}(N \log_2 N)$$

---

## Página 3: Diagrama de Mariposa, Bit Reversal y Simetrías de la DFT

### 3.1 Estructura del Diagrama de Mariposa (Radix-2 DIT)

En el algoritmo de diezmado en el tiempo (DIT), las operaciones elementales de suma y multiplicación por el Twiddle Factor $W_N^k$ se representan geométricamente mediante el **Diagrama de Mariposa (Butterfly Diagram)**:

```
  x_p ---o------------------(+)---> X[k] (Parte Superior)
          \                /
           \              /  W_N^k
            \            /
  x_i -------o---[W_N^k]----(-)---> X[k + N/2] (Parte Inferior)
```

- Cada nodo suma combina las salidas de dos transformadas parciales de tamaño $N/2$.
- El término $W_N^k$ pondera la contribución de la rama impar.

---

### 3.2 Direccionamiento de Memoria *Bit Reversal*

Para alimentar la estructura de mariposas en paralelo, las muestras de entrada $x[n]$ no se ingresan en orden secuencial $(0, 1, 2, 3, \dots)$, sino reordenadas separando pares e impares sucesivamente.

Como explicaron el ayudante David y el profesor Mariano en la clase, los procesadores de señal (DSP) y arquitecturas de hardware implementan este reordenamiento invirtiendo el orden de los bits del índice en binario (**Bit Reversal**):

#### Tabla de Reordenamiento Bit Reversal ($N=8$):
| Índice Normal ($n$) | Binario (3 bits) | Binario Invertido | Índice Reordenado | Entrada Reordenada |
| :---: | :---: | :---: | :---: | :---: |
| **0** | `000` | `000` | **0** | $x[0]$ |
| **1** | `001` | `100` | **4** | $x[4]$ |
| **2** | `010` | `010` | **2** | $x[2]$ |
| **3** | `011` | `110` | **6** | $x[6]$ |
| **4** | `100` | `001` | **1** | $x[1]$ |
| **5** | `101` | `101` | **5** | $x[5]$ |
| **6** | `110` | `011` | **3** | $x[3]$ |
| **7** | `111` | `111` | **7** | $x[7]$ |

> **Secuencia resultante en memoria:** `[0, 4, 2, 6, 1, 5, 3, 7]`

---

### 3.3 Propiedades de Simetría Compleja para Señales Reales

Si la señal de entrada $x[n]$ es una señal **real** (sin parte imaginaria), su DFT cumple la propiedad de **Simetría Conjugada (Hermitiana)**:

$$X[k] = X^*[N - k]$$

De esta propiedad fundamental se derivan las siguientes relaciones:

1. **Módulo (Simetría PAR alrededor de $N/2$):**
   $$|X[N - k]| = |X[k]|$$
2. **Fase (Simetría IMPAR alrededor de $N/2$):**
   $$\arg(X[N - k]) = -\arg(X[k])$$
3. **Puntos de Simetría Especiaes:**
   - Bin $k = 0$ (Componente de Continua / DC): Es strictly **real** y representa la suma total de las muestras.
   - Bin $k = N/2$ (Frecuencia de Nyquist $f_s/2$): Es strictly **real**.

---

## Página 4: Verificación Numérica en Python (`numpy.fft.fft`) y Espectro de Ruido

### 4.1 Experiencia en el Laboratorio: Lectura de la Matriz Compleja ($J500$)

Durante la clase práctica en el laboratorio, el profesor Mariano guio a los alumnos a analizar los resultados numéricos de ejecutar la FFT sobre una senoidal pura de $1\text{ W}$ utilizando el entorno **Spyder / Jupyter Notebook**:

```python
import numpy as np

# Configuración del experimento
fs = 1000   # Frecuencia de muestreo (1000 Hz)
N = 1000    # 1000 muestras => Delta_f = fs / N = 1 Hz/bin
t = np.arange(N) / fs

# Senoidal pura de f = 4 Hz (Amplitud = 1 V)
# x[n] = sin(2*pi*4*t) = (e^(j 2pi 4 t) - e^(-j 2pi 4 t)) / (2j)
x = np.sin(2 * np.pi * 4 * t)

# Cálculo de la FFT de 1000 puntos
X_fft = np.fft.fft(x)
```

Al inspeccionar el vector complejo `X_fft` de 1000 elementos en el **Inspector de Variables de Spyder**:

- En el bin $k = 4$ (correspondiente a la frecuencia $f = 4\text{ Hz}$):
  $$\text{Parte Real} \approx 10^{-16} \approx 0$$
  $$\text{Parte Imaginaria} = -500.0 \quad \implies X[4] = -500j = -j \frac{N}{2}$$
  $$\text{Módulo } |X[4]| = 500 = \frac{N}{2}$$

> [!IMPORTANT]
> **¿Por qué da $-500j$?**  
> Una senoidal pura $\sin(\omega_0 n)$ expresada en exponenciales complejas es:
> $$\sin(\omega_0 n) = \frac{e^{j\omega_0 n} - e^{-j\omega_0 n}}{2j} = -\frac{j}{2} e^{j\omega_0 n} + \frac{j}{2} e^{-j\omega_0 n}$$
> Al aplicar la DFT de $N=1000$ puntos, cada exponencial se multiplica por $N$, dando como resultado en el bin directo $k=4$:
> $$X[4] = N \cdot \left(-\frac{j}{2}\right) = 1000 \cdot (-0.5j) = -500j$$

---

### 4.2 Ubicación de Bins Directos e Imágenes ($k$ y $N-k$)

Debido a la simetría compleja para señales reales, los $N=1000$ bins de la FFT se distribuyen de la siguiente manera:

```
Bin 0 (DC)      Bin k=4 (4 Hz)                    Bin N-k = 996 (996 Hz)     Bin 999
   |                 |                                      |                     |
  [0]  . . . . .  [-500j]  . . . . . . . . . . . . . .  [+500j]  . . . . . . .  [999]
                     ^                                      ^
               Componente Positiva                   Componente Imagen
                  (f = 4 Hz)                    (f = fs - 4 = 996 Hz)
```

- **Frecuencia positiva ($f = 4\text{ Hz}$):** Ubicada en el bin $k = 4$. Valor $= -500j$.
- **Frecuencia imagen conjugada ($f = -4\text{ Hz} \equiv 996\text{ Hz}$):** Ubicada en el bin $N - k = 1000 - 4 = 996$. Valor $= +500j$.

---

### 4.3 Espectro Plano del Ruido Blanco

En la última parte de la clase (audio *Miguelete 30*), el profesor Mariano explicó qué sucede al calcular la FFT de una secuencia de **ruido blanco incorrelado** $n_q[n]$:

- Dado que el ruido blanco no posee ninguna frecuencia preferencial (sus muestras son independientes en el tiempo y su autocorrelación es una delta $r_{n_q n_q}[l] = \sigma^2 \delta[l]$), su transformada de Fourier distribuye la energía equitativamente entre todas las frecuencias.
- El módulo de la FFT de un ruido blanco da como resultado un **espectro plano (o aproximadamente plano)** con un valor medio de amplitud proporcional a:

$$\mathbb{E}[|N_q[k]|] \approx \sigma \cdot \sqrt{N}$$

---

> **Documento finalizado.** Todos los conceptos de los apuntes manuscritos y audios de la Clase 6 integrados y verificados.
