import random
import argparse
import sys

# Caja y apuesta iniciales
caja = 1000
valor_apuesta = 10

# Apuestas iniciales
color_apostado = "rojo"
numero_apostado = 17
tercio_apostado = 2
fila_apostada = 1
paridad_apostada = "impar"

#Datos de la ruleta
ruleta = []

rojos = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}

for i in range(37):
    if i == 0:
        datos_numero = {
            "numero": 0,
            "color": "verde",
            "paridad": None,
            "fila": None,
            "tercio": None
        }
    else:
        color = "rojo" if i in rojos else "negro"
        paridad = "par" if i % 2 == 0 else "impar"
        
        if i % 3 == 1:
            fila = 1
        elif i % 3 == 2:
            fila = 2
        else:
            fila = 3
            
        if i <= 12:
            tercio = 1
        elif i <= 24:
            tercio = 2
        else:
            tercio = 3

        datos_numero = {
            "numero": i,
            "color": color,
            "paridad": paridad,
            "fila": fila,
            "tercio": tercio
        } 
    ruleta.append(datos_numero)

# Defiinimos la funcion que genera los valores pseudoaleatorios de la ruleta
def generar_valores_aleatorios(tiradas, corridas):
  resultados = []
  for j in range(corridas):
      resultados.append([])
      for i in range(tiradas):
        resultados[j].append(random.randint(0, 36))
      
  return print[resultados]

def evaluar_resultados(resultados, tiradas, corridas):
  fr_color = [ [] for_in range corridas]  
  fr_valor = [ [] for_in range corridas]  
  fr_tercio = [ [] for_in range corridas]  
  for j in range(corridas):
      fa_color = 0
      fa_valor = 0
      fa_tercio = 0
    for i in range(tiradas):
        if resultados[j][i] == numero:
            fa_cnumero = fa_numero + 1
        if ruleta[resultado[j][i]].["color"] = color_apostado:
            fa_color = fa_color + 1
        if ruleta[resultado[j][i]].["tercio"] = tercio_apostado: 
            fa_tercio = fa_tercio + 1
        
        fr_color[j].append(fa_color / i)
        fr_numero[j].append(fa_valor / i)
        fr_tercio[j].append(fa_tercio / i)

    
        
      print(resultados[j][i])

# Ejecutar la simulación
resultados = generar_valores_aleatorios(100,1) 
evaluar_resultados(resultados, 100, 1)  

# Declaracion de los argumentos con argparse

parser = argparse.ArgumentParser(
    description="Simulador de estrategias.",
    usage="main.py -c <corridas> -n <repeticiones> [-e <numero>] -s <tipo_estrategia> -a <tipo>"
)

parser.add_argument("-c", type=int, required=True, dest="corridas")
parser.add_argument("-n", type=int, required=True, dest="tiradas")
parser.add_argument("-e", type=int, required=False, dest="numero", default=None) # Opcional
parser.add_argument("-s", type=str, required=True, dest="tipo_estrategia")
parser.add_argument("-a", type=str, required=True, dest="tipo_capital")

try:
    args = parser.parse_args()
except SystemExit:
    sys.exit(1)
    
corridas = args.corridas
tiradas = args.tiradas
numero = args.numero
tipo_estrategia = args.tipo_estrategia
tipo_capital = args.tipo_capital

resultados = generar_valores_aleatorios(tiradas, corridas)
















def simular_ruleta_martingala(caja, valor_apuesta, tiradas, corridas, tipo_capital):
    generar_valores_aleatorios(tiradas, corridas)
    
    # --- 1. CARTERA INFINITA ---
    saldo_inf = 0  # Empieza en 0 y mide el beneficio/pérdida neto. Puede ser negativo.
    apuesta_actual_inf = valor_apuesta
    peor_momento_inf = 0  # El saldo negativo más bajo registrado
    racha_perdidas_actual = 0
    max_racha_perdidas = 0
    
    for num in giros_ruleta:
        ganó = (1 <= num <= 18)
        if ganó:
            saldo_inf += apuesta_actual_inf
            apuesta_actual_inf = valor_apuesta
            racha_perdidas_actual = 0
        else:
            saldo_inf -= apuesta_actual_inf
            apuesta_actual_inf *= 2
            racha_perdidas_actual += 1
            if racha_perdidas_actual > max_racha_perdidas:
                max_racha_perdidas = racha_perdidas_actual
        
        if saldo_inf < peor_momento_inf:
            peor_momento_inf = saldo_inf

    # --- 2. CARTERA FINITA ---
    saldo_fin = caja
    apuesta_actual_fin = valor_apuesta
    bancarrota = False
    giro_quiebra = None
    
    for i, num in enumerate(tiradas):
        if bancarrota:
            continue
            
        # Si la apuesta requerida supera lo que nos queda en el bolsillo, apostamos todo lo restante
        if apuesta_actual_fin > saldo_fin:
            apuesta_actual_fin = saldo_fin
            
        ganó = (1 <= num <= 18)
        if ganó:
            saldo_fin += apuesta_actual_fin
            apuesta_actual_fin = valor_apuesta
        else:
            saldo_fin -= apuesta_actual_fin
            apuesta_actual_fin *= 2
            if saldo_fin <= 0:
                saldo_fin = 0
                bancarrota = True
                giro_quiebra = i + 1

    # --- MOSTRAR RESULTADOS ---
    print(f"Racha máxima de pérdidas consecutivas: {max_racha_perdidas}")
    print(f"Apuesta más alta que se llegó a requerir: {valor_apuesta * (2**max_racha_perdidas):,}")
    print("-" * 50)
    print(f"  -> Saldo neto final: {saldo_inf:+,}")
    print(f"  -> Mayor deuda temporal alcanzada: {peor_momento_inf:,}")
    print("-" * 50)
    print(" CARTERA FINITA (Empieza con 1,000):")
    if bancarrota:
        print(f"  -> ¡BANCARROTA! Te quedaste sin dinero en el giro número: {giro_quiebra}")
    else:
        print(f"  -> Saldo final: {saldo_fin:,}")
    print("=" * 50)