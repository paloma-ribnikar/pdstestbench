# Apuntes de Clase 3 - Procesamiento Digital de Señales (APS)
**Fecha:** Tercera Cursada  
**Profesor:** Mariano Llamedo  
**Material de origen:** Transcripción de audios (bolivia_16, bolivia_17) + Apuntes de laboratorio (Páginas 1 a 5)

---

# Página 1: Sistemas Discretos y Propiedades LTI

### 1. Definición de Sistema Discreto
Un sistema discreto es una transformación o operador $\mathcal{T}$ que toma una secuencia de entrada $x[n]$ y produce una secuencia de salida $y[n]$:

$$y[n] = \mathcal{T}\{x[n]\}$$

---

### 2. Las Dos Propiedades Fundamentales: LTI

#### A) Linealidad (Principio de Superposición)
Un sistema es **lineal** si cumple dos condiciones simultáneas:
1. **Homogeneidad (Escalamiento):** $\mathcal{T}\{a \cdot x[n]\} = a \cdot \mathcal{T}\{x[n]\}$.
2. **Aditividad:** $\mathcal{T}\{x_1[n] + x_2[n]\} = \mathcal{T}\{x_1[n]\} + \mathcal{T}\{x_2[n]\}$.

En una sola ecuación:
$$\boxed{\mathcal{T}\{a x_1[n] + b x_2[n]\} = a \mathcal{T}\{x_1[n]\} + b \mathcal{T}\{x_2[n]\}}$$

#### B) Invariancia Temporal
Un sistema es **invariante en el tiempo** si un retardo en la entrada produce exactamente el mismo retardo en la salida:

$$\boxed{\text{Si } x[n] \to y[n], \text{ entonces } x[n - n_0] \to y[n - n_0]}$$

---

# Página 2: La Respuesta al Impulso ($h[n]$)

### 1. Definición de la Respuesta al Impulso
La **respuesta al impulso** $h[n]$ es la salida que entrega un sistema LTI cuando se le aplica a la entrada un impulso unitario de Kronecker $\delta[n]$:

$$\boxed{h[n] = \mathcal{T}\{\delta[n]\}}$$

---

### 2. Caracterización Completa de Sistemas LTI
Todo sistema LTI queda **100% caracterizado por su respuesta al impulso $h[n]$**.  
Si conocemos $h[n]$, podemos predecir con absoluta precisión cuál será la salida $y[n]$ para **cualquier entrada arbitraria $x[n]$** sin necesidad de conocer los componentes internos del sistema.

---

# Página 3: La Suma de Convolución Discreta

### 1. Deducción de la Fórmula
Cualquier secuencia discreta $x[n]$ puede descomponerse en una suma ponderada de impulsos desplazados:

$$x[n] = \sum_{k=-\infty}^{\infty} x[k] \cdot \delta[n - k]$$

Aplicando el operador LTI $\mathcal{T}$ a ambos lados y usando linealidad e invariancia temporal:

$$y[n] = \mathcal{T}\left\{ \sum_{k=-\infty}^{\infty} x[k] \delta[n - k] \right\} = \sum_{k=-\infty}^{\infty} x[k] \cdot \mathcal{T}\{\delta[n - k]\}$$

$$\boxed{y[n] = x[n] * h[n] = \sum_{k=-\infty}^{\infty} x[k] \cdot h[n - k]}$$

---

### 2. Interpretación Gráfica de la Convolución (Flip & Shift)
Para calcular cada muestra $y[n]$:
1. **Reflejo (Flip):** Invertimos la respuesta al impulso en el tiempo: $h[k] \to h[-k]$.
2. **Desplazamiento (Shift):** Desplazamos $h[-k]$ en $n$ muestras hacia la derecha: $h[n - k]$.
3. **Multiplicación:** Multiplicamos punto a punto la entrada $x[k]$ por $h[n - k]$.
4. **Suma:** Sumamos todos los productos resultantes para obtener el valor escalar $y[n]$.

---

# Página 4: Propiedades Algebraicas de la Convolución

1. **Propiedad Conmutativa:**
   $$x[n] * h[n] = h[n] * x[n] = \sum_{k=-\infty}^{\infty} h[k] \cdot x[n - k]$$
   *(El orden de los factores no altera el resultado).*

2. **Propiedad Asociativa (Sistemas en Cascada / Serie):**
   $$(x[n] * h_1[n]) * h_2[n] = x[n] * (h_1[n] * h_2[n])$$
   Dos sistemas LTI en serie equivalen a un único sistema con respuesta al impulso $h_{eq}[n] = h_1[n] * h_2[n]$.

3. **Propiedad Distributiva (Sistemas en Paralelo):**
   $$x[n] * (h_1[n] + h_2[n]) = x[n] * h_1[n] + x[n] * h_2[n]$$
   Dos sistemas LTI en paralelo equivalen a un único sistema con respuesta al impulso $h_{eq}[n] = h_1[n] + h_2[n]$.

---

# Página 5: Causalidad, Estabilidad BIBO e Implementación en Python

### 1. Causalidad en Sistemas LTI
Un sistema LTI es **causal** si su salida en el instante $n$ depende únicamente del presente y del pasado.  
**Condición necesaria y suficiente:**
$$\boxed{h[n] = 0 \quad \text{para todo } n < 0}$$

---

### 2. Estabilidad BIBO (Bounded-Input Bounded-Output)
Un sistema LTI es **estable BIBO** si a cualquier entrada acotada ($|x[n]| \le M_x < \infty$) le corresponde una salida acotada ($|y[n]| \le M_y < \infty$).  
**Condición necesaria y suficiente:** La respuesta al impulso debe ser **absolutamente sumable**:

$$\boxed{\sum_{n=-\infty}^{\infty} |h[n]| < \infty}$$

---

### 3. Convolución en Python (`np.convolve`)

```python
import numpy as np
import matplotlib.pyplot as plt

# Definir entrada x[n] (senoidal) y respuesta al impulso h[n] (filtro media móvil)
N = 100
n = np.arange(N)
x = np.sin(2 * np.pi * 0.05 * n)

# Filtro de media móvil de 5 puntos (Boxcar)
h = np.ones(5) / 5.0

# Convolución lineal usando NumPy
# mode='full' entrega la salida completa de longitud L_x + L_h - 1
y = np.convolve(x, h, mode='full')

# Graficar
plt.figure(figsize=(10, 4))
plt.plot(x, label='Entrada x[n]', color='tab:blue')
plt.plot(y, label='Salida y[n] = x*h', color='tab:orange', lw=2)
plt.title('Convolución Discreta en Python (Filtro Media Móvil)')
plt.xlabel('Muestras [n]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()
plt.show()
```
