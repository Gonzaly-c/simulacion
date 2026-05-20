import random

caja = 1000
valor_apuesta = 10
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

# Ejecutar la simulación
resultados = generar_valores_aleatorios(100,1) 
evaluar_resultados(resultados, 100, 1)  