# 🧠 Machete Teórico y Práctico: Senoidal con Ruido Configurable (SNR)

Este documento es una guía conceptual y práctica paso a paso que resume todas las dudas, conceptos físicos, relaciones matemáticas y correcciones de código abordadas para simular una **senoidal con relación señal a ruido (SNR) controlada** en Python.

---

## 1. El Objetivo del Ejercicio
Generar una **señal senoidal limpia** de potencia conocida (1 Watt) y contaminarla con una **secuencia aleatoria de ruido blanco gaussiano**, de modo que la potencia del ruido sea ajustada automáticamente según el nivel de **SNR en dB** deseado por el usuario.

---

## 2. Desglose de Parámetros: ¿Qué es cada cosa?

### A. Parámetros del Entorno Digital (Conversión ADC)
- **`fs` (Frecuencia de Muestreo):** Cantidad de muestras tomadas por segundo (ej. $1000\text{ Hz}$). Determina el límite de Nyquist ($f_{\text{Nyquist}} = f_s / 2 = 500\text{ Hz}$).
- **`N` (Cantidad de Muestras):** Número total de puntos discretos generados ($N = 1000$).
- **`tt` (Vector de Tiempo - EJE X HORIZONTAL):** Tiempo discreto en segundos calculado como $t = \frac{n}{f_s}$. Son los valores del eje horizontal del gráfico: $[0.0, 0.001, 0.002, \dots]$.

### B. Parámetros de la Senoidal Útil (`xx`)
- **`vmax` (Amplitud Pico en Volts):** Altura máxima de la senoidal ($A$). Se fija en **$\sqrt{2} \approx 1.4142\text{ V}$** para que la potencia sea exactamente $1\text{ W}$.
- **`dc` (Valor Medio / Offset en Volts):** Desplazamiento vertical continuo ($\mu = 0\text{ V}$).
- **`ff` (Frecuencia de la senoidal en Hz):** Rapidez de oscilación.
- **`ph` (Fase Inicial en Radianes):** Corrimiento angular inicial.
- **`xx` (Amplitud de la Senoidal Pura - EJE Y VERTICAL):** Vector de voltajes ordenados en el tiempo.

### C. Parámetros del Ruido Aleatorio (`n_q`)
- **`loc` (Media del ruido $\mu$):** Promedio del ruido. Se fija en **$0$** para que perturbe hacia arriba y hacia abajo por igual sin agregar offset vertical.
- **`sigma_nq` ($\sigma$, Desviación Estándar del ruido):** Representa el "grosor" o amplitud típica de las fluctuaciones del ruido.
- **`n_q` (Vector de Ruido - EJE Y VERTICAL):** Vector de $N$ números aleatorios (voltios de ruido) generados con `np.random.normal()`.

---

## 3. Potencia de Señal, Potencia de Ruido y SNR

### A. Potencia de la Senoidal ($P_x = 1\text{ W}$)
La potencia media de una senoidal pura es:
$$P_x = \frac{A^2}{2}$$
Para fijar $P_x = 1\text{ W}$, despejamos la amplitud $A$:
$$1 = \frac{A^2}{2} \implies A = \sqrt{2}\text{ V} \quad (\text{variable } \texttt{vmax = np.sqrt(2)})$$

### B. Potencia del Ruido ($P_{\text{ruido}} = \sigma^2$)
Para una señal aleatoria de media cero ($\mu = 0$), su potencia media es **igual a su varianza ($\sigma^2$)**:
$$P_{\text{ruido}} = \sigma^2$$

### C. Relación Señal a Ruido (SNR en dB)
Por definición:
$$\text{SNR}_{\text{dB}} = 10 \log_{10}\left(\frac{P_x}{P_{\text{ruido}}}\right)$$

Como la potencia de la señal es fija ($P_x = 1\text{ W}$), la ecuación se simplifica a:
$$\text{SNR}_{\text{dB}} = 10 \log_{10}\left(\frac{1}{\sigma^2}\right) = -20 \log_{10}(\sigma)$$

Despejando la desviación estándar $\sigma$ para programar en Python:
$$\sigma = 10^{-\frac{\text{SNR}_{\text{dB}}}{20}} \quad (\text{código Python: } \texttt{sigma\_nq = 10**(-SNR/20)})$$

#### Comportamiento físico según SNR:
- **$\text{SNR} = 20\text{ dB}$:** $\sigma = 0.1$. Potencia de señal $100$ veces mayor que la del ruido (señal muy limpia).
- **$\text{SNR} = 0\text{ dB}$:** $\sigma = 1.0$. Potencia de señal igual a potencia de ruido ($P_x = P_{\text{ruido}} = 1$). Senoidal distorsionada.
- **$\text{SNR} = -1\text{ dB}$:** $\sigma \approx 1.122$. El ruido supera a la potencia de la señal.

---

## 4. Ejes Cartesianos vs Notación Matemática: La Gran Confusión

| Concepto | Notación Matemática | En el Gráfico Matplotlib | Significado Físico |
| :--- | :--- | :--- | :--- |
| **Tiempo** | $t$ o $n$ | **Eje X (Horizontal)** | Instante temporal en segundos ($0.01\text{ s}, 0.02\text{ s}$) |
| **Senoidal Pura** | $x[n]$ | **Eje Y (Vertical)** | Voltaje de la señal de interés ($+1.41\text{ V}$) |
| **Ruido** | $n_q[n]$ | **Eje Y (Vertical)** | Voltaje aleatorio de perturbación ($-0.10\text{ V}$) |
| **Señal Compuesta** | $x'[n] = x[n] + n_q[n]$ | **Eje Y (Vertical)** | Voltaje total medido ($+1.31\text{ V}$) |

> 💡 **¿Por qué la señal compuesta es una suma simple `xx + n_q`?**  
> El tiempo $t$ (Eje X) corre igual para todos. En cada instante $t$, el voltaje medido por un sensor o circuito es la suma física directa de la tensión útil más la tensión del ruido. En NumPy, `xx + n_q` suma automáticamente voltio a voltio cada elemento del vector.

---

## 5. Errores Comunes de Python a Evitar

1. **Potencia en Python (`**` vs `^`):**
   - ❌ `10^(-SNR/20)` $\to$ El símbolo `^` hace la operación de bits XOR (da error de tipo `TypeError`).
   - ✅ `10**(-SNR/20)` $\to$ `**` es la potencia real.

2. **Parámetros por Defecto en Funciones:**
   - ❌ `def generar_ruido(loc = loc)` $\to$ Da `NameError` si la variable `loc` no fue creada afuera previamente.
   - ✅ `def generar_ruido(SNR=0, loc=0, size=N):` $\to$ Usar valores explícitos como defaults.

3. **Uso de Variables Dentro de Funciones:**
   - Adentro del cuerpo de la función, usar las variables pasadas por parámetro:
     `n_q = np.random.normal(loc=loc, scale=sigma_nq, size=size)`

4. **Sintaxis de Comentarios Multilínea:**
   - Usar exactamente 3 comillas simples `''' comentario '''` (atención de no poner 4 comillas `''''`).

---

## 6. Estructura Limpia del Código Final

```python
import numpy as np
import matplotlib.pyplot as plt

# --- DEFINICIONES ---
fs = 1000   # Hz
N = 1000    # muestras
vmax = np.sqrt(2) # Volts (para Px = 1 W)
dc = 0
ph = 0

# --- FUNCIONES ---
def mi_funcion_sen(vmax=np.sqrt(2), dc=0, ff=1, ph=0, nn=N, fs=fs):
    tt = np.arange(nn) / fs
    xx = vmax * np.sin(2 * np.pi * ff * tt + ph) + dc
    return tt, xx

def generar_ruido(SNR=0, loc=0, size=N):
    sigma_nq = 10**(-SNR/20)
    n_q = np.random.normal(loc=loc, scale=sigma_nq, size=size)
    return n_q

# --- SCRIPT ---
# 1. Senoidal limpia de 1 W (f = 1 Hz)
tt, xx = mi_funcion_sen(vmax=vmax, dc=dc, ff=1, ph=ph, nn=N, fs=fs)

# 2. Ruido ajustado a SNR = 20 dB
n_q = generar_ruido(SNR=20, loc=dc, size=N)

# 3. Señal Compuesta (suma en el eje Y)
xx_ruidosa = xx + n_q

# 4. Gráfico
plt.figure(figsize=(10, 4))
plt.plot(tt, xx_ruidosa, label='Senoidal con Ruido (SNR = 20 dB)', color='#FF007F')
plt.title('Señal Senoidal de 1W con Ruido')
plt.xlabel('Tiempo [Segundos]')
plt.ylabel('Amplitud [Volts]')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()
```
