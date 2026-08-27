# Apuntes Complementados - Clase 7: Cuantización en Conversores A/D (ADC)
**Fecha de la clase:** 26/08  
**Institución:** UNSAM (Universidad Nacional de San Martín) - Campus Miguelete  
**Docente:** Prof. Mariano  
**Fuentes integradas:** Foto del pizarrón de clase (`media_1787852697614.jpg`), anotaciones manuscritas teóricas y prácticas de la compañera, comentarios de los pasos del cuantizador y el script oficial `esqueleto_ej_cuantizacion.py`.

---

> [!NOTE]
> Este documento unifica y explica en detalle todo el desarrollo teórico y práctico de la Clase 7 sobre el **Proceso de Cuantización en un ADC**. Contiene las deducciones matemáticas del paso de cuantización $q$, la potencia de ruido $q^2/12$, la regla del $6.02 B + 1.76\text{ dB}$, el algoritmo de 4 pasos para implementar en Python y la explicación gráfica de los resultados obtenidos en el laboratorio.

---

## Índice
1. [Sección 1: Modelo Físico del Cuantizador y el ADC](#sección-1-modelo-físico-del-cuantizador-y-el-adc)
   - 1.1 Diagrama de Bloques ($x[n] \to [ + ] \to x_R[n] \to [ Q ] \to x_q[n]$)
   - 1.2 Parámetros del ADC: Rango Dinámico ($V_F$), Bits ($B$) y Paso de Cuantización ($q$)
2. [Sección 2: Algoritmo Matemático de Cuantización en Python](#sección-2-algoritmo-matemático-de-cuantización-en-python)
   - 2.1 Los 4 Pasos Clave (Normalizar $\to$ Redondear $\to$ Clip $\to$ Escalar)
   - 2.2 Expresión Matemática y Función `np.round()`
3. [Sección 3: Ruido de Cuantización ($n_q$) y Potencia Teórica](#sección-3-ruido-de-cuantización-n_q-y-potencia-teórica)
   - 3.1 Definición del Error de Cuantización ($n_q = s_Q - s_R$)
   - 3.2 Densidad de Probabilidad Uniforme en $\left[-\frac{q}{2}, +\frac{q}{2}\right]$
   - 3.3 Deducción de la Varianza / Potencia Teórica ($P_q = \frac{q^2}{12}$)
   - 3.4 Relación Señal a Ruido de Cuantización (Fórmula $6.02 B + 1.76\text{ dB}$)
4. [Sección 4: Guía de la Práctica en Python y Código Resuelto](#sección-4-guía-de-la-práctica-en-python-y-código-resuelto)
   - 4.1 Análisis de la Señal Temporal (Escalones de Tensión)
   - 4.2 Análisis en el Dominio Frecuencial (Piso de Ruido de Cuantización)
   - 4.3 Histograma de la Distribución del Ruido de Cuantización

---

## Sección 1: Modelo Físico del Cuantizador y el ADC

### 1.1 Diagrama de Bloques

En el laboratorio de la Clase 7, el profesor Mariano dibujó en el pizarrón el diagrama del proceso de digitalización mediante un conversor analógico-digital (ADC):

```
 Senoidal Útil                     Entrada ADC                Salida Digital
    s[n] --------->( + )---------> s_R[n] ------->[ Q ]-------> s_Q[n]
                    ^                              B bits
                    |                              +/- Vf
                 n[n] Ruido Analógico
```

1. **Señal de entrada analógica real ($s_R[n]$):** Formada por la senoidal útil de interés $s[n]$ más el ruido térmico/analógico ambiental $n[n]$.
2. **Bloque Cuantizador $[Q]$:** Discretiza la amplitud continua $s_R[n]$ asignándole uno de los $2^B$ niveles discretos permitidos.
3. **Salida Cuantizada ($s_Q[n]$):** Señal discreta tanto en tiempo como en amplitud (escalonada).

---

### 1.2 Parámetros del ADC

Para definir un cuantizador real o simularlo en Python, se requieren tres variables fundamentales:

1. **Rango Dinámico / Escala Completa ($V_{FS}$ o $\pm V_f$):** Es el rango total simétrico de tensión de entrada que el ADC puede medir sin saturar (ej. de $-V_f = -2\text{ V}$ a $+V_f = +2\text{ V}$, rango total $2 V_f = 4\text{ V}$).
2. **Resolución en Bits ($B$):** Cantidad de bits del conversor. El número total de niveles discretos de tensión es:
   $$\text{Niveles Total} = 2^B$$
   *(Para $B=4$ bits, se tienen $2^4 = 16$ niveles).*
3. **Paso de Cuantización ($q$):** Es la menor variación de tensión que el ADC puede detectar (la "mínima medida" en Volts):
   $$q = \frac{2 V_f}{2^B}$$

---

## Sección 2: Algoritmo Matemático de Cuantización en Python

> [!IMPORTANT]
> **El razonamiento del algoritmo (explicación de la compañera):**  
> Para cuantizar cualquier valor de tensión continuo $s_R$, se divide todo el rango en escalones $q$, se normaliza por $q$, se aplica el redondeo al entero más cercano con `np.round()`, y finalmente se vuelve a multiplicar por $q$ para retornar a Volts.

### 2.1 Los 4 Pasos Clave del Algoritmo

1. **Normalización:** Se divide la señal por la unidad de medida $q$:
   $$\text{señal\_normalizada} = \frac{s_R}{q}$$
2. **Redondeo:** Se aplica la función `np.round()` para mapear cada punto al entero más cercano:
   $$\text{nivel\_entero} = \text{round}\left(\frac{s_R}{q}\right)$$
   Esto convierte la señal en números enteros dentro del rango $[-2^{B-1}, 2^{B-1}-1]$ (ej. para 4 bits, entre $-8$ y $+7$).
3. **Saturación / Clipping (opcional si no excede el rango):** Si la señal analógica supera $\pm V_f$, se trunca con `np.clip()` para evitar el desbordamiento digital:
   $$\text{nivel\_clip} = \text{np.clip}\left(\text{nivel\_entero}, -2^{B-1}, 2^{B-1}-1\right)$$
4. **Escalado a Volts:** Se desnormaliza multiplicando por el valor físico de $q$:
   $$s_Q = \text{nivel\_clip} \cdot q$$

---

### 2.2 Código Python de la Cuantización

```python
# Fórmula directa de cuantización en Python:
srq = np.round(sr / q) * q
```

---

## Sección 3: Ruido de Cuantización ($n_q$) y Potencia Teórica

### 3.1 Definición del Error de Cuantización

El **ruido de cuantización** $n_q[n]$ es la diferencia o error instantáneo entre la señal que entra al ADC ($s_R[n]$) y la señal cuantizada resultante ($s_Q[n]$):

$$n_q[n] = s_Q[n] - s_R[n]$$

---

### 3.2 Densidad de Probabilidad Uniforme

Dado que el redondeo aproxima la señal continua al nivel más cercano, el error de cuantización $n_q$ siempre se encuentra acotado entre la mitad del paso de cuantización hacia abajo y la mitad hacia arriba:

$$-\frac{q}{2} \le n_q \le +\frac{q}{2}$$

Para señales que varían de forma amplia atravesando múltiples niveles de cuantización, este error se distribuye de manera **uniforme** con función densidad de probabilidad:

$$p(n_q) = \begin{cases} \frac{1}{q} & \text{si } -\frac{q}{2} \le n_q \le +\frac{q}{2} \\ 0 & \text{en otro caso} \end{cases}$$

---

### 3.3 Deducción de la Potencia Teórica del Ruido de Cuantización ($P_q = q^2 / 12$)

La potencia media o varianza del ruido de cuantización se calcula como la esperanza matemática de $n_q^2$:

$$P_q = \sigma_q^2 = \int_{-q/2}^{q/2} x^2 \cdot p(x) \, dx = \int_{-q/2}^{q/2} x^2 \cdot \frac{1}{q} \, dx$$

Integrando:

$$P_q = \frac{1}{q} \left[ \frac{x^3}{3} \right]_{-q/2}^{q/2} = \frac{1}{3q} \left( \left(\frac{q}{2}\right)^3 - \left(-\frac{q}{2}\right)^3 \right) = \frac{1}{3q} \left( \frac{q^3}{8} + \frac{q^3}{8} \right) = \frac{1}{3q} \left( \frac{q^3}{4} \right) = \frac{q^2}{12}$$

> [!TIP]
> **Fórmula Fundamental:**  
> La potencia del ruido de cuantización de un ADC ideal de paso $q$ es siempre:
> $$P_{n_q} = \frac{q^2}{12} \quad [\text{Watts}]$$

---

### 3.4 Relación Señal a Ruido de Cuantización (Regra del $6.02 B + 1.76\text{ dB}$)

Para una senoidal a máxima escala ($A = V_f \implies P_{\text{señal}} = \frac{V_f^2}{2}$):

$$\text{SQNR}_{\text{dB}} = 10 \log_{10}\left( \frac{P_{\text{señal}}}{P_{n_q}} \right) = 10 \log_{10}\left( \frac{V_f^2 / 2}{q^2 / 12} \right)$$

Sustituyendo $q = \frac{2 V_f}{2^B}$:

$$\text{SQNR}_{\text{dB}} = 10 \log_{10}\left( \frac{V_f^2 / 2}{\frac{4 V_f^2}{12 \cdot 2^{2B}}} \right) = 10 \log_{10}\left( 1.5 \cdot 2^{2B} \right) = 10 \log_{10}(1.5) + 20 B \log_{10}(2)$$

$$\text{SQNR}_{\text{dB}} = 6.02 \cdot B + 1.76 \quad [\text{dB}]$$

> 💡 **Significado Físico:** Cada bit ($B$) adicional que le agregamos a un conversor A/D mejora la relación señal a ruido de cuantización en **$6.02\text{ dB}$** (aproximadamente reduce a la mitad el ruido en amplitud).

---

## Sección 4: Guía de la Práctica en Python y Código Resuelto

El archivo script completado para la práctica se encuentra listo en el repositorio en:
`pdstestbench/ej_cuantizacion_resuelto.py` (o en `pdstestbench/esqueleto_ej_cuantizacion.py`).

### 4.1 Código de Simulación Completo

```python
import numpy as np
import matplotlib.pyplot as plt

# 1. Parámetros de simulación
fs = 1000.0  # Hz
N = 1000     # muestras
B = 4        # bits del ADC
Vf = 2.0     # +/- 2 V (VFS = 4 V)

# 2. Paso de cuantización
q = (2.0 * Vf) / (2**B)  # 4 / 16 = 0.25 V
pot_ruido_cuant = (q**2) / 12.0 # Watts
pot_ruido_analog = pot_ruido_cuant * 1.0

ts = 1.0 / fs
df = fs / N
tt = np.arange(N) * ts

# 3. Generar señales
analog_sig = np.sqrt(2) * np.sin(2 * np.pi * 1.0 * tt)  # 1 Watt
nn = np.random.normal(0, np.sqrt(pot_ruido_analog), N)
sr = analog_sig + nn

# 4. Proceso de Cuantización
srq = np.round(sr / q) * q
nq = srq - sr

# 5. Verificación de Varianza
print(f"Paso de cuantización q = {q:.4f} V")
print(f"Potencia teórica q^2/12 = {pot_ruido_cuant:.6f} W")
print(f"Potencia estimada en simulación = {np.var(nq):.6f} W")
```

---

### 4.2 Explicación de las 3 Figuras Generadas por el Código

#### Figura 1: Señal Temporal ($s_R$ vs $s_Q$)
- Se observa la senoidal continua original $s_R$ junto con la salida del ADC $s_Q$.
- La salida $s_Q$ muestra la **forma escalonada típica de la cuantización**, donde los valores cambian a saltos discretos de altura $q = 0.25\text{ V}$.

#### Figura 2: Espectro de Densidad de Potencia en dB
- Muestra los espectros calculados con la FFT.
- La senoidal pura de $1\text{ Hz}$ aparece como un pico destacado en $1\text{ Hz}$.
- El ruido de cuantización $n_q$ forma un **piso de ruido plano (ruido blanco)** distribuido en todas las frecuencias desde $0$ hasta Nyquist ($f_s/2 = 500\text{ Hz}$).
- La línea punteada horizontal marca la potencia media del ruido de cuantización $\overline{n_Q} = 10 \log_{10}(2 P_q)$.

#### Figura 3: Histograma del Ruido de Cuantización ($n_q / q$)
- Grafica el histograma del error $n_q$ divididos por $q$.
- Se comprueba que los valores se distribuyen de forma pareja entre $-0.5$ y $+0.5$, coincidiendo con el rectángulo rojo de la **Distribución Uniforme Teórica**.

---

> **Documento finalizado.** Explicación teórica y script de Python listos para presentar y entregar en clase.
