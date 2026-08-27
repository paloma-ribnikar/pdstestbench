# Apuntes Complementados - Clase 4: Transformada de Fourier de Tiempo Discreto (DTFT) y Respuesta en Frecuencia
**Fecha de la clase:** Cuarta clase de cursada  
**Institución:** UNSAM (Universidad Nacional de San Martín)  
**Docentes:** Prof. Mariano  

---

> [!NOTE]
> Este documento desarrolla la Transformada de Fourier de Tiempo Discreto (DTFT), la respuesta en frecuencia $H(e^{j\omega})$ de un sistema LTI, el efecto del retardo temporal sobre la fase y el filtrado en el dominio de la frecuencia.

---

## Índice
1. [Definición Formal de la DTFT e Inversa (IDTFT)](#1-definición-formal-de-la-dtft)
2. [Periodicidad en Frecuencia $\omega \in [-\pi, \pi]$](#2-periodicidad-en-frecuencia)
3. [Respuesta en Frecuencia del Sistema LTI $H(e^{j\omega})$](#3-respuesta-en-frecuencia)
4. [Propiedades de la DTFT](#4-propiedades-de-la-dtft)
5. [El Filtro de Media Móvil (Boxcar) en Frecuencia](#5-el-filtro-de-media-móvil-boxcar)

---

## 1. Definición Formal de la DTFT

Dada una secuencia discreta $x[n]$, su **Transformada de Fourier de Tiempo Discreto (DTFT)** es la función continua de la frecuencia angular $\omega$:

$$X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] \cdot e^{-j \omega n}$$

La **Transformada Inversa (IDTFT)** recupera la secuencia discreta integrada sobre un período de $2\pi$:

$$x[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\omega}) \cdot e^{j \omega n} \, d\omega$$

---

## 2. Periodicidad en Frecuencia

Dado que $e^{-j(\omega + 2\pi)n} = e^{-j\omega n}$, toda DTFT de una secuencia discreta en el tiempo es **continua en el dominio espectral y periódica con período $2\pi$**:

$$X(e^{j(\omega + 2k\pi)}) = X(e^{j\omega}), \quad k \in \mathbb{Z}$$

El intervalo fundamental habitual de análisis es $\omega \in [-\pi, \pi]$ (o $[0, 2\pi]$).

---

## 3. Respuesta en Frecuencia del Sistema LTI

En el dominio de la frecuencia, la convolución temporal $y[n] = x[n] * h[n]$ se simplifica a una **multiplicación punto a punto**:

$$Y(e^{j\omega}) = X(e^{j\omega}) \cdot H(e^{j\omega})$$

donde $H(e^{j\omega}) = \text{DTFT}\{h[n]\} = \sum_{n=-\infty}^{\infty} h[n] e^{-j\omega n}$ es la **Respuesta en Frecuencia** del sistema.

- **Módulo $|H(e^{j\omega})|$:** Modifica la amplitud de cada componente frecuencial.
- **Fase $\arg(H(e^{j\omega}))$:** Desfasa cada componente frecuencial.

---

## 4. Propiedades de la DTFT

1. **Linealidad:** $a x_1[n] + b x_2[n] \overset{\mathcal{F}}{\longleftrightarrow} a X_1(e^{j\omega}) + b X_2(e^{j\omega})$.
2. **Desplazamiento Temporal (Retardo):**
   $$x[n - n_0] \overset{\mathcal{F}}{\longleftrightarrow} X(e^{j\omega}) \cdot e^{-j \omega n_0}$$
   > **Nota clave:** Un retardo temporal $n_0$ **sólo altera la fase lineal** del espectro ($\Delta \phi = -\omega n_0$). **El módulo $|X(e^{j\omega})|$ permanece inalterado.**
3. **Simetría Conjugada para Señales Reales:** Si $x[n] \in \mathbb{R} \implies X(e^{-j\omega}) = X^*(e^{j\omega})$.

---

## 5. El Filtro de Media Móvil (Boxcar) en Frecuencia

Para un filtro de media móvil de $N_0$ muestras centrado $h_0[n] = \frac{1}{N_0}$ para $0 \le n \le N_0-1$, su transformada es una **sinc periódica (núcleo de Dirichlet)**:

$$H_0(e^{j\omega}) = \frac{1}{N_0} \frac{\sin\left(\frac{N_0 \omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)} e^{-j \omega \frac{N_0 - 1}{2}}$$

Si el filtro se demora $1$ muestra ($h[n] = h_0[n-1]$), por la propiedad de desplazamiento:

$$H(e^{j\omega}) = H_0(e^{j\omega}) e^{-j\omega} = \frac{1}{N_0} \frac{\sin\left(\frac{N_0 \omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)} e^{-j \omega \frac{N_0 + 1}{2}}$$

---

> **Documento de la Clase 4 compilado y verificado.**
