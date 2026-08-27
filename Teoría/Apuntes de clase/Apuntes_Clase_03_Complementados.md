# Apuntes Complementados - Clase 3: Sistemas LTI y Convolución Discreta
**Fecha de la clase:** Tercera clase de cursada  
**Institución:** UNSAM (Universidad Nacional de San Martín)  
**Docentes:** Prof. Mariano  

---

> [!NOTE]
> Este documento trata la teoría de Sistemas Lineales e Invariantes en el Tiempo (LTI), la caracterización mediante la respuesta al impulso $h[n]$, la suma de convolución discreta y sus propiedades algebraicas.

---

## Índice
1. [Sistemas LTI (Lineales e Invariantes en el Tiempo)](#1-sistemas-lti)
2. [La Respuesta al Impulso ($h[n]$)](#2-la-respuesta-al-impulso)
3. [Suma de Convolución Discreta](#3-suma-de-convolución-discreta)
4. [Propiedades de la Convolución](#4-propiedades-de-la-convolución)
5. [Causalidad y Estabilidad BIBO](#5-causalidad-y-estabilidad-bibo)

---

## 1. Sistemas LTI

Un sistema discreto $\mathcal{T}$ que mapea una entrada $x[n]$ a una salida $y[n] = \mathcal{T}\{x[n]\}$ es **LTI** si cumple:

1. **Linealidad (Principio de Superposición):**
   $$\mathcal{T}\{a x_1[n] + b x_2[n]\} = a \mathcal{T}\{x_1[n]\} + b \mathcal{T}\{x_2[n]\}$$
2. **Invariancia Temporal:**
   $$\text{Si } x[n] \to y[n], \text{ entonces } x[n - n_0] \to y[n - n_0]$$

---

## 2. La Respuesta al Impulso ($h[n]$)

La **respuesta al impulso** $h[n]$ es la salida que entrega el sistema cuando la entrada es un impulso unitario de Kronecker $\delta[n]$:

$$h[n] = \mathcal{T}\{\delta[n]\}$$

Un sistema LTI queda **completamente caracterizado** por su respuesta al impulso $h[n]$.

---

## 3. Suma de Convolución Discreta

Cualquier entrada $x[n]$ puede expresarse como una suma de impulsos escalados y desplazados: $x[n] = \sum_{k=-\infty}^{\infty} x[k] \delta[n-k]$. Por linealidad e invariancia temporal, la salida $y[n]$ es la **convolución** de $x[n]$ con $h[n]$:

$$y[n] = x[n] * h[n] = \sum_{k=-\infty}^{\infty} x[k] \cdot h[n-k]$$

---

## 4. Propiedades de la Convolución

1. **Conmutativa:** $x[n] * h[n] = h[n] * x[n] = \sum_{k=-\infty}^{\infty} h[k] x[n-k]$.
2. **Asociativa:** $(x[n] * h_1[n]) * h_2[n] = x[n] * (h_1[n] * h_2[n])$ (conexión de sistemas en cascada/serie).
3. **Distributiva:** $x[n] * (h_1[n] + h_2[n]) = x[n] * h_1[n] + x[n] * h_2[n]$ (conexión de sistemas en paralelo).

---

## 5. Causalidad y Estabilidad BIBO

- **Causalidad:** Un sistema LTI es causal si su salida no depende de valores futuros de la entrada. Esto equivale a:
  $$h[n] = 0 \quad \text{para todo } n < 0$$
- **Estabilidad BIBO (Bounded-Input Bounded-Output):** Un sistema LTI es estable BIBO si a cualquier entrada acotada le corresponde una salida acotada. Esto ocurre si y solo si la respuesta al impulso es **absolutamente sumable**:
  $$\sum_{n=-\infty}^{\infty} |h[n]| < \infty$$

---

> **Documento de la Clase 3 compilado y verificado.**
