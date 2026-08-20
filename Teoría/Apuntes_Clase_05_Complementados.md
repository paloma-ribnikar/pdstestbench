# Apuntes Complementados - Clase 5: Análisis y Procesamiento de Señales (APS)
**Fecha de la clase:** 19/08 / 20/08  
**Institución:** UNSAM (Universidad Nacional de San Martín)  
**Fuentes integradas:** Apuntes manuscritos propios, PDF de apuntes teóricos en computadora, y transcripciones completas de los audios de la clase (*UNSAM Campus Miguelete 27* y *Universidad de San Martín 5*).

---

> [!NOTE]
> Este documento unifica y profundiza todos los temas tratados en la Clase 5. Se integraron las explicaciones verbales del profesor Mariano y del ayudante Hernán, las demostraciones algebraicas y frecuenciales, la teoría de correlación/incorrelación, y la guía paso a paso del ejercicio práctico de Python propuesto en el laboratorio.

---

## Índice
1. [Sección 1: Ejercicio de Convolución Discreta y Filtrado FIR (Boxcar)](#sección-1-ejercicio-de-convolución-discreta-y-filtrado-fir-boxcar)
   - 1.1 Planteo del Sistema LTI y Respuesta al Impulso ($h[n]$)
   - 1.2 Resolución Analítica en el Dominio del Tiempo
   - 1.3 Análisis Espectral en el Dominio de la Frecuencia (DTFT y Propiedades)
2. [Sección 2: Ejercicio Práctico de Laboratorio (Prof. Mariano)](#sección-2-ejercicio-práctico-de-laboratorio-prof-mariano)
   - 2.1 Consignas y Objetivos Claros del Ejercicio
   - 2.2 Deducción Matemática del Ajuste de SNR y Potencia
   - 2.3 Solución Completa e Implementación en Python
3. [Sección 3: Teoría de Correlación e Incorrelación (Profundización Teórica)](#sección-3-teoría-de-correlación-e-incorrelación-profundización-teórica)
   - 3.1 Concepto de Correlación y Autocorrelación ($r_{xx}[l]$)
   - 3.2 Evaluación en $l=0$: Energía y Potencia Muestral
   - 3.3 Evaluación para $l \neq 0$: Comparación de Signos
   - 3.4 Incorrelación Estocástica y Ruido Blanco ($\delta[l]$)
4. [Sección 4: Aspectos Administrativos y Entregas (TC0 vs TS1)](#sección-4-aspectos-administrativos-y-entregas-tc0-vs-ts1)

---

## Sección 1: Ejercicio de Convolución Discreta y Filtrado FIR (Boxcar)

### 1.1 Planteo del Sistema LTI y Respuesta al Impulso ($h[n]$)

Se analiza un **Sistema Lineal e Invariante en el Tiempo (LTI)** discreto. Todo sistema LTI está completamente caracterizado por su respuesta al impulso $h[n]$. La relación entre la entrada $x[n]$ y la salida $y[n]$ viene dada por la relación de convolución:

$$y[n] = x[n] * h[n] = \sum_{k=-\infty}^{\infty} x[k] \cdot h[n-k]$$

```
          +-----------+
x[n] ---->|   LTI     |----> y[n] = x[n] * h[n]
          |   h[n]    |
          +-----------+
```

El filtro utilizado en la práctica es un **filtro de media móvil (Boxcar / ventana rectangular)** de 5 muestras, definido como:

$$h[n] = \begin{cases} \frac{1}{5} & \text{si } 1 \le n \le 5 \\ 0 & \text{en otro caso} \end{cases}$$

> [!IMPORTANT]
> **¿Por qué el factor de escala es $\frac{1}{5}$?**  
> El profesor Mariano y Hernán enfatizaron que la amplitud se fija en $\frac{1}{5}$ para garantizar **ganancia unitaria en continua ($\omega = 0$)**. De lo contrario, si la caja tuviera amplitud 1, sumaría 5 muestras constantes y amplificaría por 5 la componente de continua del sistema:
> $$H(e^{j0}) = \sum_{n=1}^{5} h[n] = 5 \cdot \frac{1}{5} = 1$$

---

### 1.2 Resolución Analítica en el Dominio del Tiempo

Dadas las siguientes señales de entrada senoidales:
1. $x_1[n] = \sin\left(\frac{2\pi}{7} n\right)$
2. $x_2[n] = \sin\left(\frac{6\pi}{7} n\right)$
3. $x_3[n] = x_1[n] + x_2[n]$

Analizamos $y_1[n] = x_1[n] * h[n]$. Utilizando la propiedad conmutativa de la convolución ($x * h = h * x$):

$$y_1[n] = \sum_{k=1}^{5} h[k] \cdot x_1[n-k] = \frac{1}{5} \sum_{k=1}^{5} \sin\left(\frac{2\pi}{7}(n - k)\right)$$

Aplicando la identidad trigonométrica de la diferencia de ángulos:
$$\sin(a - b) = \sin(a)\cos(b) - \cos(a)\sin(b)$$

Sustituyendo $a = \frac{2\pi}{7}n$ y $b = \frac{2\pi}{7}k$:

$$y_1[n] = \frac{1}{5} \left[ \sum_{k=1}^{5} \left( \sin\left(\frac{2\pi}{7}n\right)\cos\left(\frac{2\pi}{7}k\right) - \cos\left(\frac{2\pi}{7}n\right)\sin\left(\frac{2\pi}{7}k\right) \right) \right]$$

Por linealidad de la sumatoria, los términos dependientes de $n$ salen como factores comunes:

$$y_1[n] = \frac{1}{5} \left[ \sin\left(\frac{2\pi}{7}n\right) \underbrace{\left(\sum_{k=1}^{5} \cos\left(\frac{2\pi}{7}k\right)\right)}_{a} - \cos\left(\frac{2\pi}{7}n\right) \underbrace{\left(\sum_{k=1}^{5} \sin\left(\frac{2\pi}{7}k\right)\right)}_{b} \right]$$

$$y_1[n] = \frac{1}{5} \left[ a \cdot \sin\left(\frac{2\pi}{7}n\right) + b \cdot \cos\left(\frac{2\pi}{7}n\right) \right]$$

Combinando la combinación lineal de seno y coseno en una sola senoidal desfasada:

$$y_1[n] = A \cdot \sin\left(\frac{2\pi}{7}n + \phi\right)$$

> [!TIP]
> **Propiedad fundamental de los Sistemas LTI:**  
> Al aplicar una senoidal a la entrada de un sistema LTI, la salida es **obligatoriamente otra senoidal de la misma frecuencia exacta** ($\omega_0 = 2\pi/7$). El sistema LTI **únicamente modifica la amplitud ($A$) y la fase ($\phi$)** de la señal.

---

### 1.3 Análisis Espectral en el Dominio de la Frecuencia (DTFT y Propiedades)

#### 1. Transformada de Fourier de Tiempo Discreto (DTFT) de la Entrada $x_1[n]$
La transformada de Fourier de una senoidal discreta está formada por un par de deltas de Dirac periódicas de período $2\pi$:

$$X_1(\omega) = \sum_{k=-\infty}^{\infty} \frac{1}{2j} \left[ \delta\left(\omega - \frac{2\pi}{7} + 2k\pi\right) - \delta\left(\omega + \frac{2\pi}{7} + 2k\pi\right) \right]$$

> **Nota sobre periodicidad:** Toda DTFT de una secuencia discreta en el tiempo es continua en el dominio frecuencial y periódica con período $2\pi$ (o $f_s$ si no está normalizada).

#### 2. Respuesta en Frecuencia del Filtro Boxcar $H(\omega)$
Un pulso rectangular (caja) de $N_0 = 5$ puntos centrado en el origen (de $n=0$ a $n=4$) posee una transformada de Fourier en forma de **sinc periódica (núcleo de Dirichlet)**:

$$H_0(\omega) = \frac{1}{5} \frac{\sin\left(\frac{5\omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)} e^{-j \omega \frac{5-1}{2}} = \frac{1}{5} \frac{\sin\left(\frac{5\omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)} e^{-j 2\omega}$$

Dado que el filtro de la práctica $h[n]$ comienza en $n=1$ y finaliza en $n=5$, es una versión demorada en 1 muestra del filtro ideal $h_0[n]$:

$$h[n] = h_0[n - 1]$$

Aplicando la **Propiedad de Desplazamiento Temporal**:
$$x[n - n_0] \overset{\mathcal{F}}{\longleftrightarrow} X(\omega) \cdot e^{-j \omega n_0}$$

> [!NOTE]
> **Efecto del retardo en el dominio frecuencial:**  
> Un retardo temporal $n_0$ **solo afecta a la fase lineal** del sistema ($\Delta \phi = -\omega n_0$). **El módulo $|H(\omega)|$ no sufre modificación alguna.**

Multiplicando por la fase de retardo $e^{-j\omega \cdot 1}$:

$$H(\omega) = H_0(\omega) \cdot e^{-j\omega} = \left( \frac{1}{5} \frac{\sin\left(\frac{5\omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)} e^{-j 2\omega} \right) e^{-j\omega} = \frac{1}{5} \frac{\sin\left(\frac{5\omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)} e^{-j 3\omega}$$

#### 3. Salida en Frecuencia y Propiedad de Seleccionado del Impulso (Sifting Property)
En la frecuencia, la convolución se transforma en una multiplicación:

$$Y_1(\omega) = X_1(\omega) \cdot H(\omega)$$

Al multiplicar la delta de Dirac $\delta(\omega - \omega_0)$ por $H(\omega)$, por la propiedad de selección:
$$\delta(\omega - \omega_0) \cdot H(\omega) = H(\omega_0) \cdot \delta(\omega - \omega_0)$$

Al evaluar en $\omega_0 = \frac{2\pi}{7}$:
- El **módulo $|H(2\pi/7)|$** multiplica a la amplitud original.
- La **fase $\arg(H(2\pi/7)) = -3 \cdot \frac{2\pi}{7} = -\frac{6\pi}{7}$** se suma a la fase original de la senoidal.

---

## Sección 2: Ejercicio Práctico de Laboratorio (Prof. Mariano)

### 2.1 Consignas y Objetivos Claros del Ejercicio

> [!IMPORTANT]
> **Contexto de la clase práctica:**  
> El profesor Mariano planteó este ejercicio oralmente en el laboratorio para ser resuelto en Python durante la clase. Muchos alumnos se sintieron desorientados al principio por la falta de un enunciado escrito formal. A continuación se resumen de forma ordenada y sistemática todas las consignas requeridas.

#### Objetivo General
Implementar un generador de señales senoidales en Python (Jupyter Notebook) que admita un valor deseado de **Relación Señal a Ruido (SNR en dB)** y entregue la senoidal contaminada con ruido blanco gaussiano ajustado a esa especificación.

#### Consignas Detalladas
1. **Generar una senoidal pura de 1 Watt de potencia ($P_x = 1\text{ W}$)**:
   - Determinar analíticamente la amplitud $A$ requerida para que la potencia media muestral de la senoidal sea exactamente $1\text{ W}$.
2. **Generar un vector de ruido incorrelado (gaussiano)**:
   - Crear una secuencia aleatoria $n_q[n]$ con media cero $\mu = 0$ y varianza $\sigma_{n_q}^2$.
3. **Calcular y ajustar la potencia del ruido según el SNR en dB especificado**:
   - Deducir la fórmula para calcular la desviación estándar $\sigma_{n_q}$ a partir de $\text{SNR}_{\text{dB}}$.
4. **Obtener la señal compuesta**: $x'[n] = x[n] + n_q[n]$.
5. **Verificar el comportamiento para 3 escenarios clave**:
   - $\text{SNR} = 20\text{ dB}$ (señal muy limpia, ruido casi imperceptible).
   - $\text{SNR} = 0\text{ dB}$ (potencia de señal igual a potencia de ruido, senoidal visible pero ruidosa).
   - $\text{SNR} = -1\text{ dB}$ (potencia de ruido mayor a la de la señal, la estructura senoidal comienza a perderse).
6. **Comprobación numérica**:
   - Estimar numéricamente la varianza del ruido generado utilizando `np.var()` y verificar que coincida con el valor teórico calculado.

---

### 2.2 Deducción Matemática del Ajuste de SNR y Potencia

#### Amplitud de la Senoidal de 1 Watt
La potencia media de una senoidal discreta $x[n] = A \cdot \sin(\omega_0 n + \phi)$ es:

$$P_x = \frac{A^2}{2}$$

Si el profesor exige $P_x = 1\text{ W}$:

$$1 = \frac{A^2}{2} \implies A^2 = 2 \implies A = \sqrt{2} \approx 1.41421356\text{ V}$$

#### Varianza del Ruido según SNR en dB
Por definición, la relación señal a ruido en escala lineal es:

$$\text{SNR}_{\text{lineal}} = \frac{P_x}{P_{ruido}} = \frac{E_x}{E_{ruido}}$$

Dado que el ruido posee media nula ($\mu = 0$), su potencia media es igual a su varianza: $P_{ruido} = \sigma_{n_q}^2$.  
Expresando el SNR en decibeles ($\text{dB}$):

$$\text{SNR}_{\text{dB}} = 10 \log_{10}\left(\frac{P_x}{P_{ruido}}\right) = 10 \log_{10}(P_x) - 10 \log_{10}(P_{ruido})$$

Como $P_x = 1\text{ W}$, se cumple que $10 \log_{10}(1) = 0$:

$$\text{SNR}_{\text{dB}} = -10 \log_{10}(\sigma_{n_q}^2) = -20 \log_{10}(\sigma_{n_q})$$

Despejando $\sigma_{n_q}$ (desviación estándar del ruido):

$$\log_{10}(\sigma_{n_q}) = -\frac{\text{SNR}_{\text{dB}}}{20} \implies \sigma_{n_q} = 10^{-\frac{\text{SNR}_{\text{dB}}}{20}}$$

#### Análisis de Casos Particulares
| SNR ($\text{dB}$) | Ratio $\frac{P_x}{P_{ruido}}$ | Varianza $\sigma^2$ | Desviación Estándar $\sigma$ | Apariencia Visual |
| :---: | :---: | :---: | :---: | :--- |
| **$20\text{ dB}$** | $100$ | $0.01$ | $0.1$ | Senoidal limpia con ligera fluctuación. |
| **$0\text{ dB}$** | $1$ | $1.00$ | $1.0$ | $P_x = P_{ruido}$. Senoidal claramente distorsionada. |
| **$-1\text{ dB}$** | $0.794$ | $1.259$ | $1.122$ | El ruido supera a la potencia de la señal. |

---

### 2.3 Solución Completa e Implementación en Python

A continuación se presenta el código listo para ejecutar en Jupyter Notebook que resuelve íntegramente el ejercicio propuesto por el profesor Mariano:

```python
import numpy as np
import matplotlib.pyplot as plt

def generar_senoidal_con_snr(snr_db, f0=0.05, N=1000):
    """
    Genera una senoidal de 1 Watt de potencia con ruido blanco gaussiano
    ajustado al SNR (en dB) deseado.
    
    Parámetros:
      snr_db : float - Relación Señal a Ruido deseada en dB
      f0     : float - Frecuencia digital normalizada (ciclos/muestra)
      N      : int   - Cantidad de muestras a generar
    """
    # 1. Senoidal de 1 W (Amplitud = sqrt(2))
    A = np.sqrt(2)
    n = np.arange(N)
    x = A * np.sin(2 * np.pi * f0 * n)
    
    # Potencia teórica de la señal: P_x = A^2 / 2 = 1.0
    Px_teorica = 1.0
    
    # 2. Desviación estándar del ruido para lograr el SNR especificado
    # SNR_dB = -20 * log10(sigma)  =>  sigma = 10^(-SNR_dB / 20)
    sigma_ruido = 10**(-snr_db / 20.0)
    
    # 3. Generar ruido blanco gaussiano N(0, sigma^2)
    ruido = np.random.normal(loc=0.0, scale=sigma_ruido, size=N)
    
    # 4. Suma de señal + ruido
    x_ruidosa = x + ruido
    
    # 5. Verificación numérica de varianzas/potencias muestrales
    Px_est = np.var(x)
    Pruido_est = np.var(ruido)
    snr_db_est = 10 * np.log10(Px_est / Pruido_est)
    
    print(f"=== PRUEBA SNR = {snr_db} dB ===")
    print(f" Potencia teórica de señal: {Px_teorica:.4f} W | Est: {Px_est:.4f} W")
    print(f" Varianza teórica de ruido: {sigma_ruido**2:.4f} | Est: {Pruido_est:.4f}")
    print(f" SNR estimado obtenido    : {snr_db_est:.2f} dB\n")
    
    return n, x, ruido, x_ruidosa

# --- Ejecución y Gráficos para los casos pedidos por el Profesor ---
snr_valores = [20, 0, -1]
fig, axes = plt.subplots(len(snr_valores), 1, figsize=(10, 8), sharex=True)

for i, snr in enumerate(snr_valores):
    n, x, ruido, x_ruidosa = generar_senoidal_con_snr(snr)
    
    axes[i].plot(n[:200], x_ruidosa[:200], label=f'Señal con Ruido (SNR = {snr} dB)', alpha=0.7, color='tab:orange')
    axes[i].plot(n[:200], x[:200], label='Senoidal Pura (1 W)', linestyle='--', color='tab:blue', linewidth=2)
    axes[i].set_ylabel('Amplitud [V]')
    axes[i].set_title(f'Senoidal con SNR = {snr} dB (Amplitud $A = \\sqrt{{2}}$ V)')
    axes[i].grid(True)
    axes[i].legend(loc='upper right')

axes[-1].set_xlabel('Muestras [n]')
plt.tight_layout()
plt.show()
```

---

## Sección 3: Teoría de Correlación e Incorrelación (Profundización Teórica)

> [!TIP]
> Esta sección responde al pedido explícito de otorgar máxima importancia y detalle a la parte teórica de correlación explicada por Mariano e integrada en los apuntes de la compañera.

### 3.1 Concepto de Correlación y Autocorrelación ($r_{xx}[l]$)

La **correlación** cuantifica el grado de **similitud lineal** entre dos secuencias numéricas. Cuando se compara una señal consigo misma desfasada en $l$ muestras, se denomina **autocorrelación**.

La función de autocorrelación discreta de una secuencia $x[n]$ se define formalmente como:

$$r_{xx}[l] = \sum_{n=-\infty}^{\infty} x[n] \cdot x[n+l]$$

#### Relación estrecha con la Convolución
La autocorrelación es equivalente a convolucionar la señal $x[n]$ con su propia versión invertida en el tiempo $x[-n]$:

$$r_{xx}[l] = x[l] * x[-l]$$

---

### 3.2 Evaluación en $l=0$: Energía y Potencia Muestral

Cuando el retardo es nulo ($l = 0$):

$$r_{xx}[0] = \sum_{n=-\infty}^{\infty} x[n] \cdot x[n] = \sum_{n=-\infty}^{\infty} x^2[n] = E_x$$

- En $l = 0$, la autocorrelación representa exactamente la **Energía Total Muestral ($E_x$)** de la señal.
- Si la sumatoria se promedia sobre $N$ muestras, $r_{xx}[0]$ nos brinda la **estimación de la Potencia Media Muestral ($P_x$)**.
- En $l = 0$, la señal coincide idénticamente muestra a muestra consigo misma, por lo cual $r_{xx}[0]$ es **siempre el valor máximo global** de la función de autocorrelación.

---

### 3.3 Evaluación para $l \neq 0$: Comparación de Signos

Para desplazamientos $l \neq 0$, la autocorrelación efectúa una **comparación lineal muestra a muestra del signo y magnitud**:

1. **Signos Iguales (Coherencia):** Si la muestra $x[n]$ y la muestra corrida $x[n+l]$ tienen en su mayoría el mismo signo (positivo con positivo, o negativo con negativo), sus productos resultan positivos y la autocorrelación $r_{xx}[l]$ **crece** y mantiene valores elevados.
2. **Signos Contrarios o Aleatorios:** Si los signos alternan o no guardan relación, los productos positivos se cancelan algebraicamente con los productos negativos, provocando que $r_{xx}[l]$ **tienda a cero ($r \to 0$)**.

---

### 3.4 Incorrelación Estocástica y Ruido Blanco ($\delta[l]$)

#### Definición de Incorrelación
Se dice que una secuencia de ruido $n_q[n]$ (por ejemplo, el ruido de cuantización o el ruido térmico) es **incorrelada** si el valor de la muestra en un instante actual $n$ **no guarda ninguna relación lineal** con los instantes pasados ($n-1, n-2, \dots$) ni futuros ($n+1, n+2, \dots$).

> [!CAUTION]
> **Implicancia Determinística vs Estocástica:**  
> Conocer el valor exacto del error en la muestra $n-1$ **no proporciona absolutamente ninguna información** para predecir si la siguiente muestra $n$ será positiva, negativa, grande o pequeña. No existe un modelo determinístico ni relación lineal entre muestras consecutivas.

#### Forma de la Autocorrelación del Ruido Incorrelado
Dado que para cualquier desplazamiento $l \neq 0$ los signos y valores son completamente independientes y se cancelan en el promedio, la autocorrelación de una secuencia de ruido incorrelado $n_q[n]$ con varianza $\sigma_{n_q}^2$ toma la forma de una **Delta de Kronecker (impulso)**:

$$r_{n_q n_q}[l] = \sigma_{n_q}^2 \cdot \delta[l] = \begin{cases} P_{n_q} = \sigma_{n_q}^2 & \text{si } l = 0 \\ 0 & \text{si } l \neq 0 \end{cases}$$

```
   r_nqnq[l]
       ^
       |       *  (en l=0 vale sigma^2)
       |       |
  -----+-------+-------+-------> l
      -2  -1   0   1   2
```

Esta propiedad confirma que el ruido incorrelado **solo se asemeja a sí mismo en retardo cero ($l=0$)**, desvinculándose totalmente para cualquier retardo $l \neq 0$.

---

## Sección 4: Aspectos Administrativos y Entregas (TC0 vs TS1)

Durante la clase, el profesor Mariano y los ayudantes despejaron dudas administrativas clave sobre el cursado:

### 1. Diferencia entre Tarea Complementaria 0 (TC0) y Tarea Semanal 1 (TS1)
- **TC0 (Tarea de Entorno):** Es la actividad inicial de prueba técnica disponible en el campus. Consiste simplemente en descargar un archivo base de Jupyter Notebook, modificar el nombre, ejecutarlo y subirlo al repositorio de GitHub para confirmar que el entorno de trabajo está correctamente configurado. **No requiere desarrollo matemático ni cálculos complejos.**
- **TS1 (Tarea Semanal 1):** Es la primera tarea práctica formal con evaluación de contenidos. Requiere generar señales senoidales, trabajar con deltas de Dirac, aplicar filtrado y resolver las consignas teórico-prácticas planteadas en el campus.

### 2. Entrega de Enlaces: GitHub vs NBViewer
- **NBViewer:** Es una herramienta web para renderizar notebooks de GitHub. Suele presentar caídas o errores de servidor frecuentes.
- **Criterio de Entrega:** No es obligatorio que el enlace de NBViewer funcione. Se recomienda incluir **ambos enlaces** (el enlace directo al repositorio de GitHub y el enlace de NBViewer). El enlace a GitHub es el primario y más confiable.

### 3. Guías de Trabajos Prácticos
- Las guías de ejercicios de la materia son de **práctica personal**. No tienen fecha de entrega obligatoria ni suman nota directa, pero pueden entregarse opcionalmente a los ayudantes (David y Hernán) para recibir correcciones y feedback.
- La secuencia temática de las clases no sigue al pie de la letra el orden de los capítulos de los libros de texto (Proakis u Holton). Se avanza según el criterio pedagógico y las necesidades detectadas en el grupo.

---

> **Documento finalizado.** Apuntes compilados y verificados listos para estudio y repaso.
