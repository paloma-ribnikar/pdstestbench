# Apuntes Complementados - Clase 9: Estimación Espectral, Desparramo Espectral (Spectral Leakage), Zero-Padding y Modelo Completo de ADC en dB
**Fecha de la clase:** 02/09  
**Institución:** Universidad Nacional de San Martín (UNSAM) - Campus Miguelete  
**Materia:** Análisis y Procesamiento de Señales (APS) / Métodos Numéricos  
**Docentes:** Prof. Mariano y Ayudantes David y Hernán  
**Fuentes integradas:** Apuntes manuscritos (Páginas 1, 2 y 3 del PDF), transcripción literal de audios (`transcripciones_completas_bolivia.md`), screenshots tomadas en clase y script de evidencia entregado (`Evidencia_02_09.py`).

---

> [!NOTE]
> Este documento unifica y desarrolla de manera exhaustiva todo el contenido teórico, algebraico, práctico y computacional expuesto en la **Clase 9**. Se abordan en profundidad: los criterios y exigencias de informe para las Tareas Semanales (TS), la modelización de las tres condiciones de desproporción de ruido en un ADC ($k = 0.1, 1, 10$), la calibración de la PSD por Parseval en Watts y dB, el fenómeno de **Desparramo Espectral (*Spectral Leakage*)** por no coincidencia de bin, el análisis analítico de la ventana rectangular $W_R(k)$, la técnica de **Zero-Padding** y la interpretación línea por línea del código de evidencia entregado con sus correspondientes gráficos.

---

## Índice de la Clase
1. [Requisitos de Entrega para Tareas Semanales (TS) y Criterios de Evaluación](#1-requisitos-de-entrega-para-tareas-semanales-ts-y-criterios-de-evaluación)
   - 1.1 Diagnóstico de las entregas y correcciones constructivas
   - 1.2 Estructura obligatoria de informe científico/técnico
   - 1.3 Flujo de trabajo en GitHub y visualizadores (NVViewer)
2. [Modelado Completo del Conversor A/D (ADC) y Desproporción de Ruidos](#2-modelado-completo-del-conversor-ad-adc-y-desproporción-de-ruidos)
   - 2.1 Parámetros del ADC y Modelo de Señal
   - 2.2 Cuantización y Ruido Teórico $P_{n_q} = q^2/12$
   - 2.3 Análisis de los Escenarios de Escalado de Ruido Analógico ($k = 0.1, 1, 10$)
   - 2.4 Principio Inviolable: Prevalencia del Piso Mayor y la Irreversibilidad del SNR
3. [Representación Espectral y Calibración de Potencia (Teorema de Parseval)](#3-representación-espectral-y-calibración-de-potencia-teorema-de-parseval)
   - 3.1 Deducción de la Escala de Potencia Física en Watts
   - 3.2 Conversión a dB y Ajuste del Piso de Ruido Medio
   - 3.3 Visualización de Densidad Espectral de Potencia (PSD) en Python
4. [Problema de la Estimación Espectral y Desparramo Espectral (*Spectral Leakage*)](#4-problema-de-la-estimación-espectral-y-desparramo-espectral-spectral-leakage)
   - 4.1 Coherencia Espectral ($f_0$ en un Bin Exacto $k_0 = N/4$)
   - 4.2 No Coherencia ($f_0 = 250.1\text{ Hz}$) y Discontinuidad de Borde
   - 4.3 Deducción Formal de la Transformada de la Ventana Rectangular $W_R(k)$
   - 4.4 Convolución en Frecuencia $X(k) = X_v(k) \circledast W_R(k)$ y Lóbulos Secundarios
   - 4.5 Análisis de Fase y Saltos de $\pi$ Radianes
5. [Interpolación por Zero-Padding y Ventaneo (Mitigación)](#5-interpolación-por-zero-padding-y-ventaneo-mitigación)
   - 5.1 Definición y Mecanismo del Zero-Padding
   - 5.2 Resolución Espectral Física ($\Delta f$) vs. Densidad de Grilla
   - 5.3 Mitigación mediante Funciones de Ventaneo Suaves (Hann, Hamming, Blackman)
6. [Análisis Completo del Código de Evidencia Entregado (`Evidencia_02_09.py`)](#6-análisis-completo-del-código-de-evidencia-entregado-evidencia_02_09py)
   - 6.1 Módulo 1: Definición de Parámetros y Generación de Senoidal
   - 6.2 Módulo 2: Función de Ruido Gaussiano y Casos de SNR (20 dB, 0 dB, -10 dB)
   - 6.3 Módulo 3: Aplicación de la FFT, Módulo, Fase y Calibración por Parseval
   - 6.4 Módulo 4: Cuantización, Error de Redondeo, Histograma y Test Kolmogorov-Smirnov
   - 6.5 Módulo 5: Autocorrelación del Error de Cuantización
   - 6.6 Módulo 6: Comparación de Pisos de Ruido Analógico vs. Digital en dB (TS2)

---

## 1. Requisitos de Entrega para Tareas Semanales (TS) y Criterios de Evaluación

### 1.1 Diagnóstico de las entregas y correcciones constructivas
Al inicio de la clase (Audios *Bolivia 26 y 27*), los profesores Mariano y David realizaron una puesta en común sobre las primeras entregas de las Tareas Semanales (TS0 y TS1). Se enfatizó que, al estar en tercer año de la carrera de Ingeniería, los trabajos **no pueden limitarse a entregar código suelto o gráficos pegados sin contexto**.

> [!IMPORTANT]
> **Criterio Docente:** Un gráfico por sí mismo no es un resultado ni una respuesta a una consulta. Un gráfico es un elemento de soporte que **debe ser citado e interpretado explícitamente en el texto** (`"Como se observa en la Figura 1..."`).

### 1.2 Estructura obligatoria de informe científico/técnico
Para las 5 tareas semanales restantes (empezando por la TS2), todo informe entregado en el repositorio debe cumplir rigurosamente con la siguiente estructura:

```
+-------------------------------------------------------------------------+
| ESTRUCTURA EXIGIDA PARA TAREAS SEMANALES (TS)                           |
+-------------------------------------------------------------------------+
| 1. INTRODUCCIÓN TEÓRICA (1 a 2 párrafos con ecuaciones clave)          |
| 2. GRÁFICOS PROLIJOS (Títulos, Leyendas, Ejes con Magnitud y Unidades)   |
| 3. ANÁLISIS DE RESULTADOS (Citar cada gráfico y justificar conceptualmente) |
| 4. CONCLUSIONES / SÍNTESIS (Reflexión personal sobre los hallazgos)     |
+-------------------------------------------------------------------------+
```

1. **Introducción Teórica:** Resumen inicial que contextualice los conceptos físicos y matemáticos que se aplican (por ejemplo, definir la expresión de autocorrelación, la fórmula del paso de cuantización $q$, o la ecuación de la PSD en dB).
2. **Gráficos Profesionales:**
   - **Rótulo explícito en ejes:** Indicar qué variable se representa y su unidad física entre corchetes (ej. `Tiempo [s]`, `Frecuencia [Hz]`, `Amplitud [V]`, `Potencia [W]` o `Densidad de Potencia [dB]`).
   - **Leyendas informativas:** Distinguir claramente las curvas representadas (`SNR = 20 dB`, `Senoidal limpia`, `Piso digital n_0`).
   - **Escalas adecuadas:** Evitar graficar pisos numéricos irrelevantes (como $-320\text{ dB}$) que desvirtúen la escala visual del fenómeno estudiado.
3. **Análisis de Resultados:** Texto descriptivo intercalado con los gráficos que explique el comportamiento de las curvas y lo vincule con la teoría.
4. **Conclusiones y Síntesis:** Apartado final donde el alumno vuelque una reflexión crítica de lo comprendido, las dificultades operativas y las síntesis conceptuales de los experimentos.

### 1.3 Flujo de trabajo en GitHub y visualizadores (NVViewer)
- **Notas dinámicas:** La nota de la entrega está "viva"; se permite realizar *push* con correcciones o agregados al repositorio sin necesidad de cerrar el trabajo.
- **Canal de comunicación:** Se utiliza la solapa de chat/comentarios de la entrega oficial del campus para notificar re-entregas o consultas particulares a los ayudantes (David y Hernán).
- **Herramientas de visualización:** Ante caídas eventuales del visualizador de Jupyter Notebooks (`nbviewer`), el código fuente en GitHub sigue siendo plenamente accesible. Si el trabajo se realiza en `.py`, es fundamental incluir las imágenes exportadas o integrar la explicación en un archivo `README.md` o `.ipynb`.

---

## 2. Modelado Completo del Conversor A/D (ADC) y Desproporción de Ruidos

### 2.1 Parámetros del ADC y Modelo de Señal
En los apuntes manuscritos (Página 1) y en el audio *Bolivia 27*, se definió el macromodelo del canal de adquisición digital. La señal continua analógica $s(t)$ pasa por una etapa de acondicionamiento donde se le suma ruido analógico $n_A(t)$, y posteriormente es muestreada y cuantizada por un ADC de $B$ bits:

```
  Senoidal Pura s(t)                      Entrada ADC s_R[n]            Salida Digital s_Q[n]
   P_s = 1 W (Vmax = sqrt(2)) ---->( + )----------> [ ADC ] ----------------->  s_Q = Q_{B,V_fs}{s_R}
                                     ^              B bits, +/- Vfs
                                     |              q = 2 Vfs / 2^B
                             Ruido Analógico n_A[n]
                             P_{n_A} = k * P_{n_q}
```

Parámetros nominales fijados en el laboratorio:
- **Frecuencia de Muestreo:** $f_s = 1000\text{ Hz}$ ($\Delta f = 1\text{ Hz}$ para $N = 1000$ muestras).
- **Frecuencia de Nyquist:** $f_{\text{Nyq}} = \frac{f_s}{2} = 500\text{ Hz}$.
- **Amplitud Senoidal:** $V_{\text{max}} = \sqrt{2}\text{ V} \approx 1.414\text{ V}$, garantizando una potencia normalizada de $P_{\text{señal}} = \frac{V_{\text{max}}^2}{2} = 1\text{ W}$ ($0\text{ dBW}$).
- **Conversor ADC:** Resolución de $B$ bits (evaluando $B = 4, 8, 16$ bits) y escala completa simétrica $V_{fs} = \pm 1.65\text{ V}$ (rango dinámico total de $3.3\text{ V}$).
- **Paso de Cuantización ($q$):**
  $$q = \frac{2 V_{fs}}{2^B}$$
  Para $B = 8$ bits: $q = \frac{3.3}{256} \approx 0.01289\text{ V}$. Para $B = 4$ bits: $q = \frac{3.3}{16} = 0.20625\text{ V}$ (en la captura del profesor se usó $V_r = 2.0\text{ V} \implies q = 0.125\text{ V}$).

### 2.2 Cuantización y Ruido Teórico $P_{n_q} = q^2/12$
El proceso de cuantización se modela como la adición de un ruido aleatorio de cuantización $n_q[n] = s_Q[n] - s_R[n]$. Bajo la hipótesis de cuantización no saturada sobre múltiples escalones, $n_q$ se distribuye uniformemente entre $[-q/2, +q/2]$:

$$\mathbb{E}[n_q] = 0, \quad P_{n_q} = \sigma_q^2 = \int_{-q/2}^{q/2} x^2 \frac{1}{q} \, dx = \frac{q^2}{12}$$

### 2.3 Análisis de los Escenarios de Escalado de Ruido Analógico ($k = 0.1, 1, 10$)
Para evaluar cómo interactúan el ruido analógico ambiental $n_A$ y el ruido digital de cuantización $n_q$, se parametriza la potencia del ruido analógico mediante un factor de escala $k$:

$$P_{n_A} = k \cdot P_{n_q} = k \cdot \frac{q^2}{12}$$

En el dominio logarítmico (dB), una multiplicación por $k$ se convierte en un desplazamiento aditivo del piso de ruido:
$$\Delta\text{dB} = 10 \log_{10}(k)$$

```
                                 COMPARATIVA DE CASOS DE DISEÑO (k)
+---------------------------------------------------------------------------------------------------+
| Factor k | Delta dB  | Condición Relativa               | Diagnóstico del Diseño                  |
+---------------------------------------------------------------------------------------------------+
| k = 1    | 0 dB      | Piso Analógico = Piso Digital    | ÓPTIMO (Diseño apareado y eficiente)     |
| k = 0.1  | -10 dB    | Piso Analógico 10 dB abajo       | SUBDIMENSIONADO DE ADC (Gasto analógico)  |
| k = 10   | +10 dB    | Piso Analógico 10 dB arriba      | SUBDIMENSIONADO ANALÓGICO (ADC desperd.)  |
+---------------------------------------------------------------------------------------------------+
```

#### 1. Caso $k = 1$ (Diseño Óptimo / Apareado):
- $P_{n_A} = P_{n_q}$. El piso analógico y el digital se encuentran exactamente al mismo nivel en el espectro.
- **Conclusión:** Representa el equilibrio perfecto de ingeniería. No se malgastan recursos analógicos en lograr una señal ultrasilenciosa que luego será destruida por el ADC, ni se utiliza un ADC de excesivos bits para muestrear ruido analógico.

#### 2. Caso $k = 0.1$ (Sobredimensionamiento Analógico):
- $P_{n_A} = 0.1 P_{n_q}$. El piso de ruido analógico está **$10\text{ dB}$ por debajo** del piso de ruido digital.
- **Conclusión:** El ruido total del sistema está dominado completamente por el ruido de cuantización $n_q$. La etapa analógica fue diseñada con una exigencia y costo desproporcionados respecto a la pobre resolución del ADC seleccionado.

#### 3. Caso $k = 10$ (Subdimensionamiento Analógico / ADC "Demasiado Bueno"):
- $P_{n_A} = 10 P_{n_q}$. El piso de ruido analógico está **$10\text{ dB}$ por encima** del piso de ruido digital.
- **Conclusión:** El ruido total del sistema está dominado por el ruido analógico $n_A$. El ADC posee bits de más que sólo se dedican a digitalizar el ruido proveniente del sensor o acondicionador previo.

### 2.4 Principio Inviolable: Prevalencia del Piso Mayor y la Irreversibilidad del SNR

> [!CAUTION]
> **Axioma de Procesamiento de Señales:**  
> 1. Al sumar dos procesos estocásticos independientes ($s_R = s + n_A$ y $s_Q = s_R + n_q$), **la potencia total de ruido es la suma lineal de las potencias**: $P_{\text{total}} = P_{n_A} + P_{n_q}$. En escala logarítmica, el espectro resultante es dominado completamente por el piso de mayor magnitud.  
> 2. **La relación señal a ruido ($\text{SNR}$) jamás puede mejorar al atravesar un sistema o conversión.** En el caso ideal se mantiene ($k=1$); en cualquier otro caso se degrada.

---

## 3. Representación Espectral y Calibración de Potencia (Teorema de Parseval)

### 3.1 Deducción de la Escala de Potencia Física en Watts
Para que el espectro computado mediante la FFT refleje los valores de potencia física real en Watts (asumiendo resistencia de $1\,\Omega$), debe aplicarse la normalización del Teorema de Parseval.

Si $X[k] = \text{FFT}\{x[n]\}$, la magnitud bruta $|X[k]|$ acumula un factor de escala $N$. Para recuperar la amplitud pico física $V_{\text{max}}$ de una senoidal espectral unilateral (solo frecuencias positivas $0 \le k \le N/2$):

$$V_{\text{pico}}(k) = \frac{2 \cdot |X[k]|}{N}$$

Como la potencia promedio de una senoidal de amplitud $V_{\text{pico}}$ es $P = \frac{V_{\text{pico}}^2}{2}$:

$$P(k) = \frac{\left( \frac{2 \cdot |X[k]|}{N} \right)^2}{2} = \frac{2 \cdot |X[k]|^2}{N^2} \quad [\text{Watts}]$$

### 3.2 Conversión a dB y Ajuste del Piso de Ruido Medio
Para convertir la PSD a escala decibel contendiente ($dBW$):

$$\text{PSD}_{\text{dB}}(k) = 10 \log_{10} \left( P(k) + \epsilon \right)$$

donde $\epsilon = 10^{-12}$ es un factor infinitesimal de protección contra divisiones por cero o $\log(0)$.

El **Piso Medio de Ruido ($\overline{n}_{\text{dB}}$)** se calcula promediando la potencia lineal de los bins correspondientes únicamente a ruido (excluyendo la senoidal) y aplicando luego la conversión a dB:

$$\overline{n}_{\text{dB}} = 10 \log_{10} \left( \frac{1}{M} \sum_{k \in \text{ruido}} P(k) \right)$$

---

## 4. Problema de la Estimación Espectral y Desparramo Espectral (*Spectral Leakage*)

### 4.1 Coherencia Espectral ($f_0$ en un Bin Exacto $k_0 = N/4$)
En la segunda parte de la clase (Página 1 del manuscrito y Audios *Bolivia 28 y 29*), se abordó el problema central de la estimación espectral discreta.

Si se sintetiza una senoidal de frecuencia $f_0$ con frecuencia de muestreo $f_s$ y $N$ muestras, la resolución espectral de la DFT es:

$$\Delta f = \frac{f_s}{N}$$

El índice de bin espectral asociado a $f_0$ es:

$$k_0 = \frac{f_0}{\Delta f} = \frac{f_0 \cdot N}{f_s}$$

#### Ejemplo Coherente (Manuscrito Pág 1):
Si $f_s = 1000\text{ Hz}$, $N = 1000$ muestras ($\Delta f = 1\text{ Hz}$) y sintonizamos la senoidal en $f_0 = \frac{f_s}{4} = 250\text{ Hz}$:

$$k_0 = \frac{250}{1} = 250 = \frac{N}{4}$$

En este caso:
1. $k_0$ es un número entero exacto.
2. La senoidal completa exactamente 250 ciclos dentro del registro de observación.
3. Se satisface la condición de **coherencia periódica**: $x[0] = x[N]$.
4. **Resultado Espectral:** El espectro muestra un pico único y puro (delta de Dirac discreta) en $k = 250$. Todos los demás bins caen exactamente en los ceros de la función ventana. No hay fugas de energía.

```
       COHERENCIA ESPECTRAL (f_0 = 250 Hz -> bin k = 250)
 Amplitud
   ^          | (Bin 250 puro)
   |          |
   |          |
   +----------+----------+-----------> Bin k
  k=0        250        500 (Nyq)
 (Sin desparramo, ceros exactos en k != 250)
```

### 4.2 No Coherencia ($f_0 = 250.1\text{ Hz}$) y Discontinuidad de Borde
¿Qué sucede si la frecuencia de la senoidal cambia levemente a $f_0 = 250.1\text{ Hz}$?

$$k_0 = \frac{250.1}{1} = 250.1 \notin \mathbb{Z}$$

Al no ser $k_0$ un entero:
1. La señal **no completa un número entero de ciclos** en las $N$ muestras ($x[0] \neq x[N-1]$).
2. La DFT asume implícitamente que la secuencia se repite periódicamente en el tiempo. Al concatenar copias de la ventana temporal de $N$ muestras, se produce una **discontinuidad de salto abrupto** en las fronteras entre bloques.
3. Esta discontinuidad introduce componentes de alta frecuencia espurias en el espectro.

```
       DISCONTINUIDAD TEMPORAL POR NO COHERENCIA
 x[n]
   ^     /\          /\          /\ |<- Discontinuidad de salto
   |    /  \        /  \        /  \|
   +---/----\------/----\------/----+\---------> n
   0                              N-1 | N (copia periódica)
```

### 4.3 Deducción Formal de la Transformada de la Ventana Rectangular $W_R(k)$
Capturar una señal continua durante $N$ muestras equivale matemáticamente a **multiplicar la señal infinita por una ventana rectangular temporal $w_R[n]$**:

$$w_R[n] = \begin{cases} 1 & 0 \le n \le N-1 \\ 0 & \text{en otro caso} \end{cases}$$

La Transformada Discreta de Fourier de la ventana rectangular de $N$ puntos es la suma geométrica finita:

$$W_R(k) = \sum_{n=0}^{N-1} e^{-j \frac{2\pi}{N} k n} = \frac{1 - e^{-j 2\pi k}}{1 - e^{-j \frac{2\pi}{N} k}}$$

Extrayendo los semi-ángulos del numerador y denominador:

$$W_R(k) = \frac{e^{-j \pi k} \left( e^{j \pi k} - e^{-j \pi k} \right)}{e^{-j \frac{\pi k}{N}} \left( e^{j \frac{\pi k}{N}} - e^{-j \frac{\pi k}{N}} \right)} = e^{-j \frac{\pi k}{N} (N-1)} \cdot \frac{2 j \sin(\pi k)}{2 j \sin\left(\frac{\pi k}{N}\right)}$$

Utilizando la notación de la función $\text{sinc}(x) = \frac{\sin(\pi x)}{\pi x}$:

$$W_R(k) = N \cdot \frac{\text{sinc}(\pi k)}{\text{sinc}\left(\frac{\pi k}{N}\right)} \cdot e^{-j \frac{\pi k}{N} (N-1)}$$

> [!IMPORTANT]
> **Propiedades Fundamentales de $W_R(k)$:**
> - **Lóbulo principal:** Centrado en $k=0$ con ancho entre ceros igual a $2 \Delta f = \frac{2 f_s}{N}$.
> - **Cruces por cero (Nodos):** Ocurren exactamente en todos los enteros no nulos $k = \pm 1, \pm 2, \dots, \pm (N-1)$.
> - **Caída de lóbulos secundarios:** Cae a una razón de $-13\text{ dB}$ en el primer lóbulo secundario y decae a $-20\text{ dB/década}$ ($1/f$).

### 4.4 Convolución en Frecuencia $X(k) = X_v(k) \circledast W_R(k)$ y Lóbulos Secundarios
Por el Teorema de Convolución, la multiplicación en el dominio del tiempo entre la senoidal pura $x_v[n] = e^{j 2\pi f_0 n / f_s}$ y la ventana rectangular $w_R[n]$ se transforma en una **convolución circular en el dominio de la frecuencia**:

$$X(k) = X_v(k) \circledast W_R(k) = W_R(k - k_0)$$

- **Si $k_0 \in \mathbb{Z}$ (Coherente):** La sinc $W_R(k - k_0)$ se desplaza exactamente a un bin entero. Al muestrear el espectro en los enteros $k$, la grilla coincide con el máximo central en $k = k_0$ y con **todos los ceros exactos** en $k \neq k_0$.
- **Si $k_0 \notin \mathbb{Z}$ (No Coherente, ej. $k_0 = 250.1$):** La sinc se desplaza a una posición no entera. La grilla de bins enteros **ya no cae en los ceros**, sino que muestrea los flancos del lóbulo principal y la cresta de todos los **lóbulos secundarios**.

Este fenómeno se denomina **Desparramo Espectral (*Spectral Leakage*)**: la energía de la senoidal se "fuga" o "desparrama" desde su frecuencia original hacia todas las demás frecuencias del espectro, elevando artificialmente el piso numérico.

```
       ESPECTRO CON SPECTRAL LEAKAGE (f_0 = 250.1 Hz)
 Modulo [dB]
   0 dB +          |\  (Lóbulo Principal)
        |         /  \
 -20 dB +        /    \__  __  __  (Lóbulos Secundarios / Leakage)
 -40 dB +       /        \/  \/  \/  \
 -60 dB +____  /                      \__________________
        +-----+-----+-----+-----+-----+-----+-----+-----> Frecuencia [Hz]
       0           200   250   300               500 (Nyq)
```

### 4.5 Análisis de Fase y Saltos de $\pi$ Radianes
Como se demuestra en el manuscrito (Página 2) y en la gráfica de Python:
- **Comportamiento del Módulo:** Muestra la envolvente sinc típica centrada en la frecuencia de la senoidal, decayendo logarítmicamente.
- **Comportamiento de la Fase:**
  - En la región del lóbulo principal donde la función sinc es positiva, la fase permanece constante en $0\text{ rad}$.
  - Al atravesar cada cruce por cero, el argumento del sinc cambia de signo ($\text{sinc}(x) < 0$), lo que equivale analíticamente a sumar una fase de $e^{j \pi} = -1$.
  - Esto produce **saltos bruscos de $\pi$ radianes (oscilaciones continuas entre $+\pi$ y $-\pi$)** en toda la banda de lóbulos secundarios.

---

## 5. Interpolación por Zero-Padding y Ventaneo (Mitigación)

### 5.1 Definición y Mecanismo del Zero-Padding
En la Página 3 del manuscrito y en el audio *Bolivia 29*, se analizó la técnica de **Zero-Padding (Relleno con Ceros)**. Consiste en tomar el bloque original de $N$ muestras de la señal temporal y adjuntarle $M - N$ ceros al final, expandiendo la longitud total del vector a $M$ muestras (por ejemplo, $M = 10 N$).

$$x_{\text{padded}}[n] = \begin{cases} x[n] & 0 \le n \le N-1 \\ 0 & N \le n \le M-1 \end{cases}$$

### 5.2 Resolución Espectral Física ($\Delta f$) vs. Densidad de Grilla
Existe una confusión recurrente sobre los efectos del Zero-Padding:

```
+---------------------------------------------------------------------------------------------------+
| DIFERENCIACIÓN CRÍTICA: RESOLUCIÓN FÍSICA VS. DENSIDAD DE GRILLA DENSAMENTE MUESTREADA            |
+---------------------------------------------------------------------------------------------------+
| Parámetro                  | Sin Zero-Padding (N pts)      | Con Zero-Padding (M = 10 N pts)      |
+---------------------------------------------------------------------------------------------------+
| Ancho Lóbulo Principal     | 2 f_s / N                      | 2 f_s / N  (INVARIABLE)              |
| Paso entre bins (Grilla)   | \Delta f_0 = f_s / N           | \Delta f_1 = f_s / (10 N) = \Delta f_0 / 10 |
| Puntos de evaluación DFT   | N puntos distanciados          | 10 N puntos (Densamente interpolados)|
| Separación de tonos puros  | Imposible si df < f_s / N      | IMPOSIBLE (No resuelve tonos cercanos)|
+---------------------------------------------------------------------------------------------------+
```

> [!WARNING]
> **Conclusión Clave sobre Zero-Padding:**  
> **El Zero-Padding NO mejora la resolución espectral física real del sistema.** La resolución física depende EXCLUSIVAMENTE del tiempo total de observación útil $T_0 = N \cdot T_s$.  
> Lo que hace el Zero-Padding es **interpolar la DTFT continua**, evaluando la misma función sinc en una grilla de frecuencias más fina ($\Delta f_1 = \Delta f_0 / 10$). Esto permite visualizar con precisión la forma del lóbulo principal, ubicar exactamente la cima del pico y confirmar los cruces por cero, pero no reduce el desparramo espectral ni permite separar dos senoidales más cercanas que $f_s/N$.

### 5.3 Mitigación mediante Funciones de Ventaneo Suaves (Hann, Hamming, Blackman)
Para mitigar físicamente el *Spectral Leakage*, se sustituye la ventana rectangular implícita por una ventana suavizada $w[n]$ que caiga progresivamente a cero en los extremos ($n = 0$ y $n = N-1$):

1. **Ventana Hann:** $w[n] = 0.5 \left( 1 - \cos\left(\frac{2\pi n}{N-1}\right) \right)$. Atenúa los lóbulos secundarios a $-32\text{ dB}$ (a costa de ensanchar el lóbulo principal al doble).
2. **Ventana Blackman:** Atenúa lóbulos secundarios a $-58\text{ dB}$.
3. **Ventana Flattop:** Diseñada para mediciones de amplitud exacta sin error de picos.

---

## 6. Análisis Completo del Código de Evidencia Entregado (`Evidencia_02_09.py`)

A continuación se presenta y desglosa minuciosamente el script en Python entregado como evidencia de trabajo de la Clase 9.

### 6.1 Módulo 1: Definición de Parámetros y Generación de Senoidal
```python
import numpy as np
import matplotlib.pyplot as plt

plt.close('all') # Cierra ventanas previas

# Parametros fijos del ADC
fs = 1000  # Frecuencia de muestreo (Hz) -> F_Nyquist = 500 Hz
N = 1000   # Cantidad de muestras -> Delta_f = 1 Hz

# Parametros de la senoidal
vmax = np.sqrt(2)  # Amplitud pico para lograr Potencia = 1 Watt (1.414 V)
dc = 0             # Valor medio / Offset
ff = 3             # Frecuencia de la senoidal (Hz)
ph = 0             # Fase inicial (rad)

# Parametros del cuantizador ADC
B = 8              # Cantidad de bits
Vfs = 1.65         # Rango simetrico de +/- 1.65 V (3.3 V de excursion)
qq = 2 * Vfs / (2**B) # Paso de cuantizacion (q = 3.3 / 256 = 0.01289 V)
```
- **Explicación:** Se fijan las constantes físicas del ADC. La elección de $N = 1000$ y $f_s = 1000$ asegura un paso entre bins exacto de $\Delta f = 1\text{ Hz}$. La amplitud $V_{\text{max}} = \sqrt{2}$ fija una potencia de $P = \frac{(\sqrt{2})^2}{2} = 1\text{ W}$.

### 6.2 Módulo 2: Función de Ruido Gaussiano y Casos de SNR (20 dB, 0 dB, -10 dB)
```python
def mi_funcion_sen(vmax=np.sqrt(2), dc=0, ff=1, ph=0, nn=N, fs=fs):
    tt = np.arange(nn) / fs # Vector de tiempo discreto t = n * Ts
    xx = vmax * np.sin(2 * np.pi * ff * tt + ph) + dc
    return tt, xx

def generar_ruido(SNR=0, loc=dc, size=N):
    # Calculo de desvio estandar para una potencia de senoidal de 1 W:
    # SNR = 10 * log10(P_s / P_n) = 20 * log10(V_s / sigma) => sigma = 10^(-SNR/20)
    sigma_nq = 10**(-SNR / 20)
    n_q = np.random.normal(loc=loc, scale=sigma_nq, size=size)
    return n_q
```
- **Explicación:** `generar_ruido` calcula la desviación estándar del ruido analógico $\sigma_A$ en función de la relación señal a ruido en decibeles deseada. Para $\text{SNR} = 20\text{ dB}$, $\sigma = 0.1$; para $\text{SNR} = 0\text{ dB}$, $\sigma = 1.0$; para $\text{SNR} = -10\text{ dB}$, $\sigma = 3.162$.

### 6.3 Módulo 3: Aplicación de la FFT, Módulo, Fase y Calibración por Parseval
```python
tt, xx = mi_funcion_sen(vmax=vmax, dc=0, ff=ff, ph=0, nn=N, fs=fs)
ff_vector = np.fft.fftfreq(N, d=1/fs)
salida = np.fft.fft(xx)

salida_abs = np.absolute(salida)
salida_fase = np.angle(salida)

# CALIBRACIÓN DE POTENCIA ESPECTRAL EN WATTS (PARSEVAL)
# 1. salida_abs[:N//2] -> Se toma solo la mitad positiva del espectro (hasta Nyquist).
# 2. / N               -> Se divide por N para corregir la escala acumulada de la FFT.
# 3. 2 * ...           -> Multiplica por 2 para recuperar la amplitud pico unilateral.
# 4. ** 2              -> Eleva al cuadrado para convertir Amplitud en Potencia.
# 5. / 2               -> Divide por 2 (P = Vmax^2 / 2).
salida_potencia = ((2 * salida_abs[:N//2]) / N)**2 / 2
```
- **Explicación:** Algoritmo riguroso de calibración de potencia en binario. Garantiza que la suma del vector `salida_potencia` concuerde exactamente con la potencia temporal `np.mean(xx**2)`.

### 6.4 Módulo 4: Cuantización, Error de Redondeo, Histograma y Test Kolmogorov-Smirnov
```python
# Cuantizacion por redondeo al escalon q mas cercano
xx_q = np.round(xx / qq) * qq
nq = xx_q - xx # Error instantaneo de cuantizacion

# Normalizacion del error en unidades de paso q (-0.5 a +0.5)
nq_normalizado = nq / qq

media_nq = np.mean(nq_normalizado)
varianza_nq = np.var(nq_normalizado)

print('Media del ruido de cuantizacion =', media_nq)
print('Varianza del ruido de cuantizacion =', varianza_nq)
# Varianza teorica esperada para distribucion uniforme U(-0.5, 0.5): 1/12 = 0.08333...

# Sugerencia del profesor: Test de Kolmogorov-Smirnov (KS)
from scipy import stats
res_ks = stats.kstest(nq_normalizado, 'uniform', args=(-0.5, 1.0))
print('Estadistico KS =', res_ks.statistic, 'p-valor =', res_ks.pvalue)
```
- **Explicación:** Se cuantiza la señal y se extrae la secuencia de error $n_q$. Al calcular la varianza experimental de `nq_normalizado`, esta converge a $\frac{1}{12} \approx 0.08333$. El test KS de `scipy.stats` permite evaluar formalmente la hipótesis nula de uniformidad ($p\text{-valor} > 0.05$).

### 6.5 Módulo 5: Autocorrelación del Error de Cuantización
```python
# Autocorrelacion lineal completa del ruido de cuantizacion
autocorr = np.correlate(nq_normalizado, nq_normalizado, mode='full')
autocorr = autocorr / np.max(autocorr) # Normalizacion a pico unitario en retardo zero

retardos = np.arange(-(N-1), N)

plt.figure()
plt.plot(retardos, autocorr)
plt.xlim(-50, 50)
plt.xlabel('Retardo [muestras]')
plt.ylabel('Autocorrelacion Normalizada')
plt.title('Autocorrelacion del Ruido de Cuantizacion')
plt.grid(True)
plt.show()
```
- **Explicación:** Evalúa si el error de cuantización $n_q[n]$ se comporta como un **ruido blanco incorrelacionado**. La gráfica resultante muestra un impulso delta aislado en retardo 0 ($R_{n_q}[0] = 1$) y valores despreciables cercanos a 0 para todo retardo $\tau \neq 0$, demostrando empíricamente que la secuencia es incorrelacionada consigo misma.

### 6.6 Módulo 6: Comparación de Pisos de Ruido Analógico vs. Digital en dB (TS2)
```python
# Señal analógica ruidosa s_R pasa por el cuantizador ADC
xx_ruidosa_q = np.round(xx_ruidosa / qq) * qq

# PSD de la señal limpia y ruidosa en dB
psd_limpia_dB = 10 * np.log10(salida_potencia + 1e-12)
psd_ruidosa_dB = 10 * np.log10(salida_ruidosa_potencia + 1e-12)

# PSD de la salida digital s_Q (ADC out)
salida_q_abs = np.abs(np.fft.fft(xx_ruidosa_q)[:N//2])
psd_cuantizada_dB = 10 * np.log10(((2 * salida_q_abs) / N)**2 / 2 + 1e-12)

# PISO DE RUIDO ANALÓGICO (n_A)
psd_n_q = ((2 * np.abs(np.fft.fft(n_q)[:N//2])) / N)**2 / 2
piso_analog_dB = 10 * np.log10(np.mean(psd_n_q) + 1e-12)

# PISO DE RUIDO DIGITAL DE CUANTIZACIÓN (n_0)
ruido_cuantiz_digital = xx_ruidosa_q - xx_ruidosa
psd_n_digital = ((2 * np.abs(np.fft.fft(ruido_cuantiz_digital)[:N//2])) / N)**2 / 2
piso_digital_dB = 10 * np.log10(np.mean(psd_n_digital) + 1e-12)

# Grafico final comparativo de la TS2
plt.figure(figsize=(12, 6))
plt.plot(ff_vector[:N//2], psd_cuantizada_dB, label=r'$s_Q = Q_{B, V_R}\{s_R\}$ (ADC out)', color='#1f77b4', linewidth=1.5)
plt.plot(ff_vector[:N//2], psd_ruidosa_dB, label=r'$s_R = s + n$ (ADC in)', color='#2ca02c', linestyle=':', linewidth=1.2)
plt.axhline(piso_analog_dB, color='#d62728', linestyle='--', label=rf'$\overline{{n}} = {piso_analog_dB:.1f}$ dB (piso analog.)')
plt.axhline(piso_digital_dB, color='#17becf', linestyle='--', label=rf'$\overline{{n_0}} = {piso_digital_dB:.1f}$ dB (piso digital)')

plt.title(f'Señal muestreada por un ADC de {B} bits - $\pm V_{{fs}} = {Vfs}$ V - q = {qq:.3f} V')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Densidad de Potencia [dB]')
plt.xlim(0, fs/2)
plt.legend(loc='upper right')
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()
```
- **Explicación:** Este bloque sintetiza visualmente la comparativa entre la señal muestreada $s_Q$, la señal ruidosa de entrada $s_R$, el piso analógico medio $\overline{n}$ y el piso digital de cuantización $\overline{n_0}$. Permite validar de un vistazo la condición de escalado $k$ configurada y comprobar el cumplimiento del marco teórico de la TS2.

---
