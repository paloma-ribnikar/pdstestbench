# Apuntes Complementados - Clase 2: Senoidales Discretas, Aliasing y Frecuencia Normalizada
**Fecha de la clase:** Segunda clase de cursada  
**Institución:** UNSAM (Universidad Nacional de San Martín)  
**Docentes:** Prof. Mariano  

---

> [!NOTE]
> Este documento profundiza en la representación de señales senoidales discretas, la frecuencia digital normalizada ($\omega_0$), el fenómeno de aliasing frecuencial y la condición matemática de periodicidad en tiempo discreto.

---

## Índice
1. [Senoidales en Tiempo Continuo vs. Tiempo Discreto](#1-senoidales-en-tiempo-continuo-vs-tiempo-discreto)
2. [Frecuencia Digital Normalizada ($\omega_0$ y $f_0$)](#2-frecuencia-digital-normalizada)
3. [El Fenómeno de Aliasing (Solapamiento)](#3-el-fenómeno-de-aliasing)
4. [Condición de Periodicidad Discreta ($N_0$)](#4-condición-de-periodicidad-discreta)
5. [Potencia Media de una Senoidal Discreta](#5-potencia-media-de-una-senoidal-discreta)

---

## 1. Senoidales en Tiempo Continuo vs. Tiempo Discreto

- **Continua:** $x(t) = A \sin(\Omega_0 t + \phi) = A \sin(2\pi f t + \phi)$.
- **Discreta:** Al evaluar en $t = n T_s = n / f_s$:
  $$x[n] = A \sin\left(2\pi \frac{f}{f_s} n + \phi\right) = A \sin(\omega_0 n + \phi)$$

---

## 2. Frecuencia Digital Normalizada

Definimos dos formas equivalentes de expresar la frecuencia digital:

1. **Frecuencia Angular Discreta $\omega_0$ [rad/muestra]:**
   $$\omega_0 = 2\pi \frac{f}{f_s} \quad [\text{rad/muestra}]$$
   Su rango fundamental se encuentra acotado en $[-\pi, \pi]$ (o $[0, 2\pi]$).
2. **Frecuencia Normalizada $f_0$ [ciclos/muestra]:**
   $$f_0 = \frac{f}{f_s} \quad [\text{ciclos/muestra}]$$
   Su rango fundamental va de $-0.5$ a $+0.5$.

---

## 3. El Fenómeno de Aliasing

A diferencia de las señales continuas, en tiempo discreto dos frecuencias analógicas que difieren en múltiplos enteros de la frecuencia de muestreo ($f_2 = f_1 + k f_s$) producen **exactamente la misma secuencia discreta**:

$$\sin\left(2\pi \frac{f + k f_s}{f_s} n\right) = \sin\left(2\pi \frac{f}{f_s} n + 2\pi k n\right) = \sin\left(2\pi \frac{f}{f_s} n\right)$$

- Todas las frecuencias analógicas superiores a Nyquist ($f > f_s / 2$) se "pliegan" dentro del intervalo fundamental $[0, f_s / 2]$.

---

## 4. Condición de Periodicidad Discreta

Una senoidal en tiempo continuo es siempre periódica. Sin embargo, **una senoidal discreta $x[n] = A \sin(\omega_0 n)$ es periódica SI Y SOLO SI el cociente $\frac{f}{f_s}$ es un número racional**:

$$\frac{f}{f_s} = \frac{k}{N_0} \implies N_0 = k \cdot \frac{f_s}{f} \quad (\text{Período fundamental en muestras})$$

donde $k$ y $N_0$ son enteros primos entre sí.

---

## 5. Potencia Media de una Senoidal Discreta

La potencia media de una senoidal pura $x[n] = A \sin(\omega_0 n + \phi)$ es independiente de la frecuencia y la fase, y depende únicamente de su amplitud pico $A$:

$$P_x = \frac{A^2}{2} \quad [\text{Watts}]$$

- Para que una senoidal tenga potencia de **$1\text{ Watt}$**, su amplitud debe fijarse en **$A = \sqrt{2} \approx 1.4142\text{ V}$**.

---

> **Documento de la Clase 2 compilado y verificado.**
