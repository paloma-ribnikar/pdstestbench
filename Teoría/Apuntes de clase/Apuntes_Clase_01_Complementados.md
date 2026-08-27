# Apuntes Complementados - Clase 1: Introducción al Procesamiento Digital de Señales (APS)
**Fecha de la clase:** Inicio de cursada  
**Institución:** UNSAM (Universidad Nacional de San Martín)  
**Docentes:** Prof. Mariano y Ayudantes  

---

> [!NOTE]
> Este documento resume los conceptos introductorios del Procesamiento Digital de Señales (PDS/APS), abarcando la clasificación de señales continuas vs. discretas, la conversión A/D, el Teorema de Nyquist-Shannon y las nociones de energía y potencia.

---

## Índice
1. [Conceptos Fundamentales de Señales Continuas y Discretas](#1-conceptos-fundamentales)
2. [Conversión Analógico-Digital y Parámetros de Muestreo](#2-conversión-analógico-digital)
3. [Teorema de Muestreo de Nyquist-Shannon](#3-teorema-de-nyquist-shannon)
4. [Reconstrucción e Interpolación Ideal](#4-reconstrucción-e-interpolación-ideal)
5. [Clasificación de Señales: Energía vs. Potencia](#5-clasificación-de-señales)

---

## 1. Conceptos Fundamentales

- **Señal analógica / continua $x(t)$**: Definida para todo instante de tiempo continuo $t \in \mathbb{R}$.
- **Señal discreta $x[n]$**: Secuencia de valores ordenados definida en instantes enteros $n \in \mathbb{Z}$.
- **Muestreo uniforme**: Se toma la amplitud de la señal continua a intervalos constantes $T_s$:
  $$x[n] = x(n T_s) = x\left(\frac{n}{f_s}\right)$$
  donde $T_s$ es el **Período de Muestreo** y $f_s = \frac{1}{T_s}$ es la **Frecuencia de Muestreo**.

---

## 2. Conversión Analógico-Digital

Un conversor A/D (ADC) consta de dos procesos fundamentales:
1. **Muestreo (Sampling):** Discretiza el tiempo continuo $t \to n T_s$.
2. **Cuantización (Quantization):** Discretiza la amplitud en niveles finitos $2^B$.

---

## 3. Teorema de Nyquist-Shannon

Para poder reconstruir exactamente una señal continua de banda limitada $B$ a partir de sus muestras discretas, la frecuencia de muestreo $f_s$ debe cumplir:

$$f_s \ge 2 f_{\max}$$

- **Frecuencia de Nyquist:** $f_{\text{Nyquist}} = \frac{f_s}{2}$. Es la máxima frecuencia analógica que se puede representar sin solapamiento (aliasing).
- **Aliasing (Solapamiento Frecuencial):** Ocurre cuando $f_s < 2 f_{\max}$. Las frecuencias superiores a $f_s/2$ se pliegan y aparecen erróneamente como frecuencias más bajas.

---

## 4. Reconstrucción e Interpolación Ideal

La reconstrucción de la señal continua $x(t)$ a partir de la secuencia discreta $x[n]$ mediante un filtro interpolador ideal (sinc) viene dada por la fórmula de Whittaker-Shannon:

$$x(t) = \sum_{n=-\infty}^{\infty} x[n] \cdot \text{sinc}\left(\frac{t - n T_s}{T_s}\right)$$

donde $\text{sinc}(u) = \frac{\sin(\pi u)}{\pi u}$.

---

## 5. Clasificación de Señales

### A. Señales de Energía
Una señal $x[n]$ es de energía si su energía total $E_x$ es finita:
$$E_x = \sum_{n=-\infty}^{\infty} |x[n]|^2 < \infty$$

### B. Señales de Potencia
Una señal $x[n]$ es de potencia si su potencia media $P_x$ es finita y mayor a cero:
$$P_x = \lim_{N \to \infty} \frac{1}{2N+1} \sum_{n=-N}^{N} |x[n]|^2 < \infty$$
Las senoidales infinitas y señales periódicas son señales de potencia.

---

> **Documento de la Clase 1 compilado y verificado.**
