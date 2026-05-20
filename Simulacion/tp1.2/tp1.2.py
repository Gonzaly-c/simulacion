import random

def generar_valores_aleatorios(tiradas, corridas):
  resultados = []
  for j in range(corridas):
      resultados.append([])
      for i in range(tiradas):
        resultados[j].append(random.randint(0, 36))
      
  return print[resultados]

def evaluar_resultados(resultados, tiradas, corridas):
  for j in range(corridas):
    for i in range(tiradas):
      print(resultados[j][i])
      

ruleta = []

# Definimos los números rojos de la ruleta europea
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
        # 1. Determinar color
        color = "rojo" if i in rojos else "negro"
        
        # 2. Determinar paridad
        paridad = "par" if i % 2 == 0 else "impar"
        
        # 3. Determinar fila (1, 2 o 3)
        # Los números de la fila 1 al dividirlos por 3 dejan resto 1 (1, 4, 7...)
        # Los de la fila 2 dejan resto 2 (2, 5, 8...) y la fila 3 son múltiplos de 3.
        if i % 3 == 1:
            fila = 1
        elif i % 3 == 2:
            fila = 2
        else:
            fila = 3
            
        # 4. Determinar tercio (Docena)
        # En la ruleta se apuesta por 1ª, 2ª o 3ª docena (1-12, 13-24, 25-36)
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


def simular_ruleta_martingala(giros=100000, apuesta_base=10, saldo_inicial_finito=1000):
    # Generamos los 100 giros de antemano para comparar ambas carteras bajo el mismo escenario
    # En la ruleta europea (0 al 36), apostamos a Rojo. 
    # Consideramos "Ganar" si sale un número del 1 al 18 (simulando los 18 números rojos, 48.65% de probabilidad)
    giros_ruleta = [random.randint(0, 36) for _ in range(giros)]
    
    # --- 1. CARTERA INFINITA ---
    saldo_inf = 0  # Empieza en 0 y mide el beneficio/pérdida neto. Puede ser negativo.
    apuesta_actual_inf = apuesta_base
    peor_momento_inf = 0  # El saldo negativo más bajo registrado
    racha_perdidas_actual = 0
    max_racha_perdidas = 0
    
    for num in giros_ruleta:
        ganó = (1 <= num <= 18)
        if ganó:
            saldo_inf += apuesta_actual_inf
            apuesta_actual_inf = apuesta_base
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
    saldo_fin = saldo_inicial_finito
    apuesta_actual_fin = apuesta_base
    bancarrota = False
    giro_quiebra = None
    
    for i, num in enumerate(giros_ruleta):
        if bancarrota:
            continue
            
        # Si la apuesta requerida supera lo que nos queda en el bolsillo, apostamos todo lo restante
        if apuesta_actual_fin > saldo_fin:
            apuesta_actual_fin = saldo_fin
            
        ganó = (1 <= num <= 18)
        if ganó:
            saldo_fin += apuesta_actual_fin
            apuesta_actual_fin = apuesta_base
        else:
            saldo_fin -= apuesta_actual_fin
            apuesta_actual_fin *= 2
            if saldo_fin <= 0:
                saldo_fin = 0
                bancarrota = True
                giro_quiebra = i + 1

    # --- MOSTRAR RESULTADOS ---
    print("=" * 50)
    print("      RESULTADOS DE LA SIMULACIÓN (100 GIROS)      ")
    print("=" * 50)
    print(f"Racha máxima de pérdidas consecutivas: {max_racha_perdidas}")
    print(f"Apuesta más alta que se llegó a requerir: {apuesta_base * (2**max_racha_perdidas):,}")
    print("-" * 50)
    print(" CARTERA INFINITA:")
    print(f"  -> Saldo neto final: {saldo_inf:+,}")
    print(f"  -> Mayor deuda temporal alcanzada: {peor_momento_inf:,}")
    print("-" * 50)
    print(" CARTERA FINITA (Empieza con 1,000):")
    if bancarrota:
        print(f"  -> ¡BANCARROTA! Te quedaste sin dinero en el giro número: {giro_quiebra}")
    else:
        print(f"  -> Saldo final: {saldo_fin:,}")
    print("=" * 50)

# Ejecutar la simulación
resultados=generar_valores_aleatorios(100,1)  # Ejemplo de acceso a la información del número 11
evaluar_resultados(resultados, 100, 1)  