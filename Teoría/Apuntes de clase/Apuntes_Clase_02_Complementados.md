# Apuntes de Clase 2 - Procesamiento Digital de Señales (APS)
**Fecha:** Segunda Cursada  
**Profesor:** Mariano Llamedo  
**Material de origen:** Transcripción de audios + Apuntes de laboratorio (Páginas 1 a 5)

---

# Página 1: Senoidales Continuas vs. Discretas y Muestreo

### 1. La Señal Senoidal en Tiempo Continuo
Una senoidal pura en tiempo continuo se define por su amplitud $A$, su frecuencia analógica $f$ (Hz) o frecuencia angular $\Omega = 2\pi f$ (rad/s), y su fase inicial $\phi$ (rad):

$$x(t) = A \sin(\Omega t + \phi) = A \sin(2\pi f t + \phi)$$

---

### 2. Discretización de la Senoidal
Al muestrear uniformemente con período $T_s = 1/f_s$:

$$x[n] = x(n T_s) = A \sin\left(2\pi f n T_s + \phi\right) = \boxed{A \sin\left(2\pi \frac{f}{f_s} n + \phi\right) = A \sin(\omega_0 n + \phi)}$$

---

# Página 2: Frecuencia Digital Normalizada y Banda Digital

### 1. Frecuencia Angular Discreta ($\omega_0$) y Frecuencia Normalizada ($f_0$)

Definimos las variables frecuenciales en el mundo discreto:

1. **Frecuencia Angular Discreta $\omega_0$ [rad/muestra]:**
   $$\boxed{\omega_0 = 2\pi \frac{f}{f_s}} \quad [\text{rad/muestra}]$$
   Su rango fundamental (sin ambigüedad) está acotado en el intervalo $[-\pi, \pi]$ (o $[0, 2\pi]$).

2. **Frecuencia Normalizada $f_0$ [ciclos/muestra]:**
   $$\boxed{f_0 = \frac{f}{f_s}} \quad [\text{ciclos/muestra}]$$
   Su rango fundamental se extiende en $[-0.5, +0.5]$.

---

### 2. La Banda Digital Primaria
El intervalo de frecuencias analógicas $[ -f_s/2, +f_s/2 ]$ se mapea directamente al intervalo angular discreto $[ -\pi, +\pi ]$.
* La frecuencia de continua (DC) $f = 0 \text{ Hz} \implies \omega_0 = 0 \text{ rad/muestra}$.
* La frecuencia de Nyquist $f = f_s/2 \text{ Hz} \implies \omega_0 = \pi \text{ rad/muestra}$.

---

# Página 3: Demostración Matemática del Aliasing Senoidal

### 1. Demostración Algebraica
Consideremos dos senoidales analógicas distintas $x_1(t)$ de frecuencia $f$ y $x_2(t)$ de frecuencia desplazada $f' = f + k f_s$ (donde $k \in \mathbb{Z}$):

$$x_2[n] = \sin\left(2\pi \frac{f + k f_s}{f_s} n\right) = \sin\left(2\pi \frac{f}{f_s} n + 2\pi k n\right)$$

Como $k \cdot n$ es siempre un número entero, $2\pi k n$ representa un múltiplo entero de $2\pi$ radianes:

$$\sin(\theta + 2\pi \cdot \text{entero}) = \sin(\theta)$$

Por lo tanto:

$$\boxed{x_2[n] = \sin\left(2\pi \frac{f}{f_s} n\right) = x_1[n]}$$

> [!IMPORTANT]
> **Conclusión del Aliasing:**  
> En tiempo discreto, **infinitas frecuencias analógicas distintas** producen la **misma secuencia discreta exacta**. No es posible distinguirlas a menos que apliquemos previamente un filtro anti-aliasing.

---

# Página 4: Condición de Periodicidad en Tiempo Discreto

### 1. ¿Por qué una senoidal discreta no siempre es periódica?
En tiempo continuo, $\sin(\Omega t)$ siempre es periódica. Sin embargo, en tiempo discreto, requerimos que exista un entero $N_0 > 0$ tal que:

$$x[n + N_0] = x[n] \implies \sin(\omega_0 (n + N_0)) = \sin(\omega_0 n)$$

Para que esto se cumpla, el término $\omega_0 N_0$ debe ser un múltiplo entero de $2\pi$:

$$\omega_0 N_0 = 2\pi k \implies 2\pi \frac{f}{f_s} N_0 = 2\pi k \implies \boxed{\frac{f}{f_s} = \frac{k}{N_0}}$$

> [!NOTE]
> **Regla de Periodicidad Discreta:**  
> Una senoidal discreta es periódica **SI Y SOLO SI la relación $\frac{f}{f_s}$ es un número racional**.  
> El **Período Fundamental ($N_0$ muestras)** es el menor entero positivo que resulta de simplificar la fracción $\frac{f_s}{f}$.

---

# Página 5: Potencia Media y Simulación en Python

### 1. Potencia Media de una Senoidal Discreta ($P_x = A^2 / 2$)
La potencia media muestral de una senoidal $x[n] = A \sin(\omega_0 n + \phi)$ viene dada por:

$$P_x = \frac{1}{N_0} \sum_{n=0}^{N_0-1} |x[n]|^2 = \boxed{\frac{A^2}{2}}$$

* Para fijar una senoidal de potencia unitaria **$P_x = 1 \text{ Watt}$**:
  $$1 = \frac{A^2}{2} \implies A = \sqrt{2} \approx 1.41421356 \text{ Volts}$$

---

### 2. Script de Simulación en Python (Experimentación de la Clase)

```python
import numpy as np
import matplotlib.pyplot as plt

# Parámetros del experimento
fs = 1000.0   # Frecuencia de muestreo (1000 Hz)
N = 1000      # Cantidad de muestras
f1 = 1.0      # Frecuencia 1 Hz (dentro de la banda digital)
f2 = 1001.0   # Frecuencia 1001 Hz (fuera de Nyquist => Aliasing)

n = np.arange(N)
tt = n / fs

# Senoidales de 1 Watt (A = sqrt(2))
A = np.sqrt(2)
x1 = A * np.sin(2 * np.pi * f1 * tt)
x2 = A * np.sin(2 * np.pi * f2 * tt)

# Graficar para demostrar que x1 y x2 son idénticas en discreto
plt.figure(figsize=(10, 4))
plt.plot(tt[:100], x1[:100], label='f1 = 1 Hz', color='tab:blue', lw=2)
plt.plot(tt[:100], x2[:100], label='f2 = 1001 Hz (Aliased)', linestyle='--', color='tab:red')
plt.title('Demostración Práctica de Aliasing en Python')
plt.xlabel('Tiempo [segundos]')
plt.ylabel('Amplitud [Volts]')
plt.grid(True)
plt.legend()
plt.show()
```
