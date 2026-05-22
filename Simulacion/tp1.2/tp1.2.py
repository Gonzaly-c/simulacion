import matplotlib.pyplot as plt
import random
import numpy as np
import argparse
import sys

CAJA_INICIAL = 500
APUESTA_BASE = 1
TIRADAS = 1000
CORRIDAS = 5


rojos = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}


def crear_ruleta():
    ruleta = []
    for i in range(37):
        if i == 0:
            ruleta.append({"numero": 0, "color": "verde", "tercio": None})
        else:
            color = "rojo" if i in rojos else "negro"
            tercio = 1 if i <= 12 else (2 if i <= 24 else 3)
            ruleta.append({"numero": i, "color": color, "tercio": tercio})
    return ruleta

def verificar_ganancia(ruleta, numero, tipo_apuesta):
    """Verifica si se ganó la apuesta"""
    if tipo_apuesta == "pleno":
        return numero == 17
    elif tipo_apuesta == "color":
        return ruleta[numero]["color"] == "rojo"
    elif tipo_apuesta == "tercio":
        return ruleta[numero]["tercio"] == 2
    return False

def obtener_ganancia(tipo_apuesta):
    """Retorna el multiplicador de ganancia"""
    return {"pleno": 35, "color": 1, "tercio": 2}.get(tipo_apuesta, 1)

def generar_valores_aleatorios(tiradas, corridas):
    """Genera números aleatorios de la ruleta"""
    resultados = []
    for j in range(corridas):
        resultados.append([])
        for i in range(tiradas):
            resultados[j].append(random.randint(0, 36))
    return resultados

def frecuencia_x_tipo_apuesta(resultados, tiradas, corridas, tipo_apuesta, valor_elegido, fr_esperada, ruleta):

    frecuencia_x_corridas = []

    for i in range(corridas):
        frecuencias = []
        frecuencia_color_abs = 0

        for j in range(tiradas):

            if ruleta[resultados[i][j]][tipo_apuesta] == valor_elegido:
                frecuencia_color_abs += 1

            frecuencia_relativa = frecuencia_color_abs / (j + 1)
            frecuencias.append(frecuencia_relativa)

        frecuencia_x_corridas.append(frecuencias)

    frecuencia_x_corridas = np.array(frecuencia_x_corridas)

    frecuencias_promedio = np.mean(
        frecuencia_x_corridas,
        axis=0
    )

    # Creamos la figura con los 2 subplots independientes
    fig, axs = plt.subplots(1, 2, figsize=(18, 5))

    for i in range(corridas):
        axs[0].plot(
            frecuencia_x_corridas[i],
            alpha=0.6,
            
        )

    axs[0].axhline(
        y=fr_esperada,
        color='red',
        linestyle='--',
        label='Frecuencia Esperada'
    )

    axs[0].set_xlabel("Tiradas")
    axs[0].set_ylabel("Frecuencia relativa")
    axs[0].set_title(f"Frecuencia relativa del {tipo_apuesta} {valor_elegido} según n (por corrida)")
    axs[0].legend()

    lim_bajo = 0
    lim_alto = 1
    if(tipo_apuesta == "numero"): # para ver las funciones de más cerca (el valor esperado es muy bajo)
        lim_bajo = 0
        lim_alto = 0.3
    
    axs[0].set_ylim(lim_bajo, lim_alto)

    ticks_axs0 = list(axs[0].get_yticks())
    if fr_esperada not in ticks_axs0:
        ticks_axs0.append(fr_esperada)
    axs[0].set_yticks(ticks_axs0)

    axs[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.4f}'))

    axs[1].plot(
        frecuencias_promedio,
        color='darkblue',  
        linewidth=2,
        alpha=0.8,
        label='Promedio entre corridas'
    )

    axs[1].axhline(
        y=fr_esperada,
        color='red',
        linestyle='--',
        label='Frecuencia Esperada'
    )

    axs[1].set_xlabel("Tiradas")
    axs[1].set_ylabel("Frecuencia relativa")
    axs[1].set_title(f"Frecuencia relativa del {tipo_apuesta} {valor_elegido} según n (promedio de las corridas)")
    axs[1].legend()

    axs[1].set_ylim(lim_bajo, lim_alto)

    ticks_axs1 = list(axs[1].get_yticks())
    if fr_esperada not in ticks_axs1:
        ticks_axs1.append(fr_esperada)
    axs[1].set_yticks(ticks_axs1)

    axs[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.4f}'))

def histograma_x_tipo_apuesta(
        resultados,
        ruleta,
        tipo_apuesta,
        valores,
        frecuencias_esperadas):

    total = len(np.array(resultados).flatten())

    frecuencias_observadas = []

    todos = np.array(resultados).flatten()

    for valor in valores:

        contador = sum(
            1
            for numero in todos
            if ruleta[numero][tipo_apuesta] == valor
        )

        frecuencias_observadas.append(
            contador/total
        )

    diferencias = np.abs(
        np.array(frecuencias_observadas)
        -
        np.array(frecuencias_esperadas)
    )

    fig, axs = plt.subplots(
        1,
        3,
        figsize=(18,5)
    )

    datos = [
        (
            axs[0],
            frecuencias_observadas,
            f"Frecuencias observadas ({tipo_apuesta})",
            "Frecuencia relativa"
        ),
        (
            axs[1],
            frecuencias_esperadas,
            f"Frecuencias esperadas ({tipo_apuesta})",
            "Frecuencia relativa"
        ),
        (
            axs[2],
            diferencias,
            "Error absoluto",
            "|Experimental - Esperado|"
        )
    ]

    for ax, valores_y, titulo, ylabel in datos:

        barras = ax.bar(
            [str(v) for v in valores],
            valores_y
        )

        ax.set_title(titulo)

        ax.set_ylabel(ylabel)

        ymin, ymax = ax.get_ylim()

        offset = (ymax - ymin) * 0.015

        mostrar_valores = len(valores) <= 10

        if tipo_apuesta == "numero":
            ax.tick_params(axis='x', rotation=90)

        if mostrar_valores:

            for barra in barras:

                altura = barra.get_height()

                ax.text(
                    barra.get_x() + barra.get_width()/2,
                    altura + offset,
                    f"{altura:.4f}",
                    ha='center',
                    va='bottom',
                    fontsize=8
                )

    plt.tight_layout()



def evaluar_estrategia(resultados, tiradas, corridas, caja_inicial, apuesta_base, 
                       tipo_estrategia, tipo_apuesta, ruleta, capital_finito=True):
    """Función para evaluar una estrategia con un tipo de apuesta específico"""
    historial_corridas = []
    

    secuencia_fibo = [1, 1]
    if tipo_estrategia == 'f':
        for k in range(2, tiradas + 20):  
            secuencia_fibo.append(secuencia_fibo[k-1] + secuencia_fibo[k-2])
    
    for j in range(corridas):
        caja = caja_inicial
        apuesta_actual = apuesta_base
        flujo_caja_corrida = [caja]
        indice_fibo = 0
        
        for i in range(tiradas):
            num_obtenido = resultados[j][i]
            gano_la_tirada = verificar_ganancia(ruleta, num_obtenido, tipo_apuesta)
            
            if capital_finito and apuesta_actual > caja:
                apuesta_actual = caja
            
            if gano_la_tirada:
                caja += apuesta_actual * obtener_ganancia(tipo_apuesta)
            else:
                caja -= apuesta_actual
            
            flujo_caja_corrida.append(caja)
            
            if capital_finito and caja <= 0:
                caja = 0
            
            if tipo_estrategia == 'm': 
                if gano_la_tirada:
                    apuesta_actual = apuesta_base
                else:
                    apuesta_actual *= 2
            
            elif tipo_estrategia == 'd':  
                if gano_la_tirada:
                    apuesta_actual = max(apuesta_base, apuesta_actual - apuesta_base)
                else:
                    apuesta_actual += apuesta_base
            
            elif tipo_estrategia == 'o':
                if gano_la_tirada:
                    apuesta_actual = apuesta_base
                else:
                    apuesta_actual += 1
            
            elif tipo_estrategia == 'f':  
                if gano_la_tirada:
                    indice_fibo = max(0, indice_fibo - 2)
                else:
                    indice_fibo = min(indice_fibo + 1, len(secuencia_fibo) - 1)
                apuesta_actual = secuencia_fibo[indice_fibo] * apuesta_base
        
        historial_corridas.append(flujo_caja_corrida)
    
    return historial_corridas

def evaluar_resultados(resultados, tiradas, corridas, caja_inicial, apuesta_base, ruleta, capital_finito=True):
    """Función para evaluar todas las estrategias y tipos de apuesta"""
    tipos_apuesta = ["pleno", "color", "tercio"]
    nombres_apuesta = ["Pleno (1:35)", "Color (1:1)", "Tercio (1:2)"]
    tipo_estrategia = ["m", "d", "f", "o"]
    nombres_estrategia = ["Martingala", "D'Alembert", "Fibonacci", "Otro"]
   
    resultados_simulacion = {}
    
    for tipo_ap, nombre_ap in zip(tipos_apuesta, nombres_apuesta):
  
        
        resultados_simulacion[tipo_ap] = {}
        
        for tipo_est, nombre_est in zip(tipo_estrategia, nombres_estrategia):
            historial = evaluar_estrategia(resultados, tiradas, corridas, caja_inicial, 
                                          apuesta_base, tipo_est, tipo_ap, ruleta, capital_finito)
            
            resultados_simulacion[tipo_ap][nombre_est] = historial

            capitales_finales = [flujo[-1] for flujo in historial]
            ganancias = [c - caja_inicial for c in capitales_finales]
            corridas_ganadoras = sum(1 for g in ganancias if g > 0)
            
            
    
    return resultados_simulacion

def graficar(resultados_simulacion, caja_inicial, estrategia=None, capital_finito=True):
    """Grafica todos los resultados en un solo plot 3x1"""
    tipos = ["pleno", "color", "tercio"]
    nombres_tipos = ["Pleno", "Color", "Tercio"]
    estrategias = ["Martingala", "D'Alembert", "Fibonacci", "Otro"] if estrategia is None else [estrategia]
    
    capital_str = "FINITO" if capital_finito else "INFINITO"
    
    fig, axs = plt.subplots(3, 1, figsize=(12, 12))
    
    for row, (tipo, nombre_tipo) in enumerate(zip(tipos, nombres_tipos)):
        ax = axs[row]
        
        for est in estrategias:
            # Graficar todas las corridas
            for flujo in resultados_simulacion[tipo][est]:
                ax.plot(flujo, alpha=0.3, linewidth=1)
            
            # Graficar promedio
            promedio = np.mean([f for f in resultados_simulacion[tipo][est]], axis=0)
            ax.plot(promedio, color='red', linewidth=2.5, label='Promedio')
        
        ax.axhline(caja_inicial, color='green', linestyle='--', alpha=0.5, label='Capital inicial')
        ax.set_title(f"{nombre_tipo} - {estrategias[0]} - Capital {capital_str}", fontsize=12, fontweight='bold')
        ax.set_xlabel("Tirada")
        ax.set_ylabel("Capital ($)")
        ax.grid(True, alpha=0.2)
        ax.legend()
    
    plt.tight_layout()
    fig.savefig('grafica_simulacion.png', dpi=150)
    print("\n[OK] Grafica guardada: grafica_simulacion.png")
   
def main():
    parser = argparse.ArgumentParser(
        description="Simulador de estrategias de ruleta",
        usage="main.py -c <corridas> -n <repeticiones> [-e <numero>] -s <tipo_estrategia> -a <tipo>"
    )
    parser.add_argument("-c", type=int, required=True, dest="corridas", help="Número de corridas")
    parser.add_argument("-n", type=int, required=True, dest="tiradas", help="Número de tiradas")
    parser.add_argument("-e", type=int, required=False, dest="numero", default=None, help="Número elegido (opcional)")
    parser.add_argument("-s", type=str, required=True, dest="tipo_estrategia", help="Tipo de estrategia")
    parser.add_argument("-a", type=str, required=True, dest="tipo_capital", help="Tipo de capital (f=finito, i=infinito)")
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(1)
    corridas = args.corridas
    tiradas = args.tiradas
    numero_elegido = args.numero
    tipo_estrategia = args.tipo_estrategia
    tipo_capital_arg = args.tipo_capital.lower()
    capital_finito = tipo_capital_arg == "f"
    tipo_capital_str = "FINITO" if capital_finito else "INFINITO"
    
    # Mapear tipo de estrategia a nombre mostrable
    mapeo_estrategias = {
        'm': 'Martingala',
        'd': "D'Alembert",
        'f': 'Fibonacci',
        'o': 'Otro'
    }
    nombre_estrategia = mapeo_estrategias.get(tipo_estrategia.lower(), None)
    
    ruleta = crear_ruleta()
    resultados = generar_valores_aleatorios(tiradas, corridas)
    resultados_simulacion = evaluar_resultados(resultados, tiradas, corridas, 
                                              CAJA_INICIAL, APUESTA_BASE, ruleta, capital_finito)
    frecuencia_x_tipo_apuesta(resultados, tiradas, corridas, "color","rojo", 18/37, ruleta)
    frecuencia_x_tipo_apuesta(resultados, tiradas, corridas, "tercio",1, 12/37, ruleta)
    if(numero_elegido):
        frecuencia_x_tipo_apuesta(resultados, tiradas, corridas, "numero",numero_elegido, 1/37, ruleta)
    histograma_x_tipo_apuesta(
        resultados,
        ruleta,
        "color",
        ["rojo","negro","verde"],
        [18/37,18/37,1/37]
    )
    histograma_x_tipo_apuesta(
        resultados,
        ruleta,
        "tercio",
        [1,2,3,"Número 0"],
        [12/37,12/37,12/37,1/37]
    )
    histograma_x_tipo_apuesta(
        resultados,
        ruleta,
        "numero",
        list(range(37)),
        [1/37]*37
    )

    
    graficar(resultados_simulacion, CAJA_INICIAL, nombre_estrategia, capital_finito)
    plt.show()

    
    print("\n✓ Simulación completada!")

if __name__ == "__main__":
    main()
    
