import numpy as np
import scipy.stats as stats
import math
import matplotlib.pyplot as plt
from collections import Counter

def prueba_chi_cuadrado(datos, num_intervalos=10, alfa=0.05):
    """Test de Uniformidad (Chi-Cuadrado 1D)."""
    n = len(datos)
    frecuencia_esperada = n / num_intervalos
    frecuencias_observadas, _ = np.histogram(datos, bins=num_intervalos, range=(0, 1))
    
    chi2_calc = np.sum((frecuencias_observadas - frecuencia_esperada)**2 / frecuencia_esperada)
    p_valor = 1 - stats.chi2.cdf(chi2_calc, num_intervalos - 1)
    
    resultado = "OK" if p_valor > alfa else "ERROR"
    return round(p_valor, 4), resultado

def prueba_rachas(datos, alfa=0.05):
    """Test de Independencia (Rachas respecto a la mediana)."""
    n = len(datos)
    mediana = np.median(datos)
    signos = datos > mediana
    
    n1 = np.sum(signos)
    n2 = n - n1
    
    rachas = 1
    for i in range(1, n):
        if signos[i] != signos[i-1]:
            rachas += 1
            
    media_esperada = ((2 * n1 * n2) / n) + 1
    varianza_esperada = (2 * n1 * n2 * (2 * n1 * n2 - n)) / ((n ** 2) * (n - 1))
    
    if varianza_esperada == 0:
        return 0.0000, "ERROR"
        
    z_calc = (rachas - media_esperada) / math.sqrt(varianza_esperada)
    p_valor = 2 * (1 - stats.norm.cdf(abs(z_calc)))
    
    resultado = "OK" if p_valor > alfa else "ERROR"
    return round(p_valor, 4), resultado

def prueba_series(datos, divisiones=10, alfa=0.05):
    """Test de Series (Uniformidad 2D / Independencia)."""
    n_pares = len(datos) // 2
    x = datos[0:2*n_pares:2]
    y = datos[1:2*n_pares:2]
    
    frecuencia_esperada = n_pares / (divisiones ** 2)
    
    # Histograma 2D
    H, _, _ = np.histogram2d(x, y, bins=divisiones, range=[[0, 1], [0, 1]])
    
    chi2_calc = np.sum((H - frecuencia_esperada)**2 / frecuencia_esperada)
    grados_libertad = (divisiones ** 2) - 1
    
    p_valor = 1 - stats.chi2.cdf(chi2_calc, grados_libertad)
    resultado = "OK" if p_valor > alfa else "ERROR"
    
    return round(p_valor, 4), resultado

def prueba_poker(datos, alfa=0.05):
    """Test del Póker (5 decimales)."""
    n = len(datos)
    # Probabilidades teóricas para 5 dígitos
    probabilidades = {
        'Todos distintos': 0.3024,
        'Un par': 0.5040,
        'Dos pares': 0.1080,
        'Tercia': 0.0720,
        'Full/Poker/Quintilla': 0.0136 # Agrupados por baja probabilidad
    }
    
    conteos = {k: 0 for k in probabilidades.keys()}
    
    for num in datos:
        
        str_num = f"{num:.5f}".split('.')[1] 
        frecuencias = list(Counter(str_num).values())
        frecuencias.sort(reverse=True)
        
        if frecuencias == [1, 1, 1, 1, 1]:
            conteos['Todos distintos'] += 1
        elif frecuencias == [2, 1, 1, 1]:
            conteos['Un par'] += 1
        elif frecuencias == [2, 2, 1]:
            conteos['Dos pares'] += 1
        elif frecuencias == [3, 1, 1]:
            conteos['Tercia'] += 1
        else:
            conteos['Full/Poker/Quintilla'] += 1
            
    chi2_calc = 0
    for categoria in probabilidades.keys():
        esperado = n * probabilidades[categoria]
        observado = conteos[categoria]
        chi2_calc += ((observado - esperado)**2) / esperado
        
    grados_libertad = len(probabilidades) - 1
    p_valor = 1 - stats.chi2.cdf(chi2_calc, grados_libertad)
    
    resultado = "OK" if p_valor > alfa else "ERROR"
    return round(p_valor, 4), resultado

def graficar_analisis(datos, titulo_generador):
    """Genera un panel de 4 gráficas coherentes con las pruebas teóricas."""
    n = len(datos)
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Análisis Visual - {titulo_generador}', fontsize=16, fontweight='bold')

    # 1. Histograma (Chi-Cuadrado)
    axs[0, 0].hist(datos, bins=10, color='skyblue', edgecolor='black', alpha=0.7)
    axs[0, 0].axhline(y=n/10, color='red', linestyle='--', linewidth=2, label='Frecuencia Esperada')
    axs[0, 0].set_title('1. Uniformidad (Chi-Cuadrado)')
    axs[0, 0].legend()

    # 2. Lag Plot (Test de Series / Independencia)
    axs[0, 1].scatter(datos[:-1], datos[1:], alpha=0.3, s=2, color='orange')
    axs[0, 1].set_title('2. Independencia Bidimensional (Lag Plot)')
    axs[0, 1].set_xlabel('X_i')
    axs[0, 1].set_ylabel('X_{i+1}')

    # 3. Secuencia temporal (Para intuir Rachas)
    muestra = datos[:100] # Mostrar solo los primeros 100 para no saturar
    axs[1, 0].plot(muestra, marker='o', linestyle='-', color='purple', markersize=3, alpha=0.7)
    axs[1, 0].axhline(y=np.median(datos), color='red', linestyle='--', label='Mediana')
    axs[1, 0].set_title('3. Comportamiento Secuencial (Rachas - 100 nums)')
    axs[1, 0].legend()

    # 4. Histograma 2D (Base visual del Test de Series)
    axs[1, 1].hist2d(datos[:-1], datos[1:], bins=10, cmap='Blues')
    axs[1, 1].set_title('4. Densidad de pares (Uniformidad 2D)')
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.show()

if __name__ == "__main__":
    
    cantidad = 10000
    
    # 1. GCL (Congruencial Lineal)
    a, c, m, semilla_gcl = 1664525, 1013904223, 2**32, 12345
    x = semilla_gcl
    datos_gcl = []
    for _ in range(cantidad):
        x = (a * x + c) % m
        datos_gcl.append(x / m)
    datos_gcl = np.array(datos_gcl)
    
    # 2. Mid-Square (Cuadrados Medios - intencionalmente débil)
    semilla_ms = 1931
    datos_ms = []
    for _ in range(cantidad):
        cuadrado = semilla_ms ** 2
        s = str(cuadrado).zfill(8)
        semilla_ms = int(s[2:6])
        datos_ms.append(semilla_ms / 10000)
    datos_ms = np.array(datos_ms)

    # 3. Generador de Python (Mersenne Twister)
    datos_py = np.random.rand(cantidad)

    # Ejecutamos las pruebas
    generadores = {
        "GCL (Propio)": datos_gcl,
        "Mid-Square": datos_ms,
        "Python (Nativo)": datos_py
    }

    print(f"\n{'-'*95}")
    print(f"{'Generador':<18} | {'Chi-Cuadrado':<16} | {'Rachas':<16} | {'Series (2D)':<16} | {'Póker':<16}")
    print(f"{'-'*95}")
    
    for nombre, datos in generadores.items():
        r_chi = prueba_chi_cuadrado(datos)
        r_rac = prueba_rachas(datos)
        r_ser = prueba_series(datos)
        r_pok = prueba_poker(datos)
        
        t1 = f"{r_chi[0]} ({r_chi[1]})"
        t2 = f"{r_rac[0]} ({r_rac[1]})"
        t3 = f"{r_ser[0]} ({r_ser[1]})"
        t4 = f"{r_pok[0]} ({r_pok[1]})"
        
        print(f"{nombre:<18} | {t1:<16} | {t2:<16} | {t3:<16} | {t4:<16}")
    print(f"{'-'*95}\n")

    # Mostramos las gráficas (puedes comentar las que no quieras ver)
    graficar_analisis(datos_gcl, "Generador Congruencial Lineal (GCL)")
    graficar_analisis(datos_ms, "Método de Cuadrados Medios")
    graficar_analisis(datos_py, "Módulo 'random' de Python")