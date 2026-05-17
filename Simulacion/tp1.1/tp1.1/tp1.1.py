import random
import matplotlib.pyplot as plt
import numpy as np
import sys

def generar_valores_aleatorios(tiradas, corridas):
  resultados = []
  for j in range(corridas):
      resultados.append([])
      for i in range(tiradas):
        resultados[j].append(random.randint(0, 36))
      
  return resultados

def graficar_frecuencia_relativa(tiradas, corridas, resultados, n):
  fig, axs = plt.subplots(1, 3, figsize=(18, 4))
  frEsperada = 1 / 37
  frecuencias_promediadas = [0] * tiradas
  frecuencias = [[] for _ in range(corridas)]
  for j in range(corridas):
    frecuencia_relativa_absoluta = 0
    for i in range(tiradas):
        if resultados[j][i] == n:
          frecuencia_relativa_absoluta += 1
        frecuencia_relativa = frecuencia_relativa_absoluta / (i + 1)
        frecuencias[j].append(frecuencia_relativa)
  axs[0].plot(frecuencias[0], label='Frecuencia Relativa')
  axs[0].axhline(y=frEsperada, color='r', linestyle='-', label='Frecuencia Esperada = ' + str(round(frEsperada, 4)))
  axs[0].set_title('Frecuencia Relativa de la corrida 1')
  axs[0].set_xlabel('Número de Tiradas')
  axs[0].set_ylabel('Frecuencia Relativa')
  axs[0].legend()

  for i in range(corridas):
    axs[1].plot(frecuencias[i], label='Frecuencia Relativa Corrida ' + str(i + 1), linewidth=2, alpha=0.7)
  axs[1].axhline(y=frEsperada, color='r', linestyle='-', linewidth=2, label='Frecuencia Esperada = ' + str(round(frEsperada, 4)))
  axs[1].set_title('Frecuencia Relativa de cada corrida')
  axs[1].set_xlabel('Número de Tiradas')
  axs[1].set_ylabel('Frecuencia Relativa')
  axs[1].legend()
  axs[2].set_ylim([0, max([max(f) for f in frecuencias]) * 1.1])
  for i in range(tiradas):
     for j in range(corridas):
        frecuencias_promediadas[i] += frecuencias[j][i]
     frecuencias_promediadas[i] /= corridas
        
      


  axs[2].plot(frecuencias_promediadas, label='Frecuencia Relativa Promediada en ' + str(corridas) + ' corridas')
  axs[2].axhline(y=frEsperada, color='r', linestyle='-', label='Frecuencia Esperada = ' + str(round(frEsperada, 4)))
  axs[2].set_title('Frecuencia Relativa Promediada en ' + str(corridas) + ' corridas')
  axs[2].set_xlabel('Número de Tiradas')
  axs[2].set_ylabel('Frecuencia Relativa')
  axs[2].legend()
  plt.tight_layout()
  fig.savefig('frecuencia_relativa.png')

def graficar_valor_promedio(tiradas, corridas, resultados):
  fig, axs = plt.subplots(1, 3, figsize=(18, 4))
  vpe = 18
  valores_promediados = [[] for _ in range(corridas)]
  valores_promediados_promediados = [0] * tiradas
  for j in range(corridas):
      suma = 0
      for i in range(tiradas):
        suma += resultados[j][i]
        valor_promedio = suma / (i + 1)
        valores_promediados[j].append(valor_promedio)
  axs[0].plot(valores_promediados[0], label='Valor Promedio')
  axs[0].axhline(y=vpe, color='r', linestyle='-',label='Valor Promedio Esperado = ' + str(vpe))
  axs[0].set_title('Valor Promedio de las tiradas de la corrida 1')
  axs[0].set_xlabel('Número de Tiradas')
  axs[0].set_ylabel('Valor Promedio')
  axs[0].legend()
  for j in range(corridas):
      axs[1].plot(valores_promediados[j], label='Valor Promedio Corrida ' + str(j + 1), linewidth=2, alpha=0.7)
  axs[1].axhline(y=vpe, color='r', linestyle='-', linewidth=2, label='Valor Promedio Esperado = ' + str(vpe))
  axs[1].set_title('Valor Promedio de cada corrida')
  axs[1].set_xlabel('Número de Tiradas')
  axs[1].set_ylabel('Valor Promedio')
  axs[1].legend()
  
  for i in range(tiradas):
    for j in range(corridas):
      valores_promediados_promediados[i] += valores_promediados[j][i]
    valores_promediados_promediados[i] /= corridas

  axs[2].plot(valores_promediados_promediados, label='Valor Promedio Promediado en ' + str(corridas) + ' corridas')
  axs[2].axhline(y=vpe, color='r', linestyle='-', label='Valor Promedio Esperado = ' + str(vpe))
  axs[2].set_title('Valor Promedio Promediado en ' + str(corridas) + ' corridas')
  axs[2].set_xlabel('Número de Tiradas')
  axs[2].set_ylabel('Valor Promedio')
  axs[2].legend()
  plt.tight_layout()
  fig.savefig('valor_promedio.png')

def graficar_varianza(tiradas, corridas, resultados):
  fig, axs = plt.subplots(1, 3, figsize=(18, 4))
  varianza_esperada = 114  
  varianzas = [[] for _ in range(corridas)]
  varianzas_promedio = [0] * tiradas
  for j in range(corridas):
      for i in range(1, tiradas + 1):
          var = np.var(resultados[j][:i])
          varianzas[j].append(var)

  axs[0].plot(varianzas[0], label='Varianza')
  axs[0].axhline(y=varianza_esperada, color='r', linestyle='-', label='Varianza esperada = ' + str(varianza_esperada))
  axs[0].set_title('Varianza de las tiradas de la corrida 1')
  axs[0].set_xlabel('Número de Tiradas')
  axs[0].set_ylabel('Varianza')
  axs[0].legend()

  for i in range(0, tiradas):
      for j in range(corridas):
          varianzas_promedio[i] += varianzas[j][i]
      varianzas_promedio[i] /= corridas
  
  axs[2].plot(varianzas_promedio, label='Varianza Promediada en ' + str(corridas) + ' corridas')
  axs[2].axhline(y=varianza_esperada, color='r', linestyle='-', label='Varianza esperada = ' + str(varianza_esperada))
  axs[2].set_title('Varianza Promediada en ' + str(corridas) + ' corridas')
  axs[2].set_xlabel('Número de Tiradas')
  axs[2].set_ylabel('Varianza')
  axs[2].legend()

   
  for j in range(corridas):
    axs[1].plot(varianzas[j], label='Varianza Corrida ' + str(j + 1), linewidth=2, alpha=0.7)
  axs[1].axhline(y=varianza_esperada, color='r', linestyle='-', linewidth=2, label='Varianza esperada = ' + str(varianza_esperada))
  axs[1].set_title('Varianza de cada corrida')
  axs[1].set_xlabel('Número de Tiradas')
  axs[1].set_ylabel('Varianza')
  axs[1].legend()
  plt.tight_layout()
  fig.savefig('varianza.png')
  
def graficar_desvio_estandar(resultados, tiradas, corridas):
  fig, axs = plt.subplots(1, 3, figsize=(18, 4))
  ## Calculo del desvio estandar de la corrida uno

  corridaUno = resultados[0]
  desvios_corridaUno = []
  for i in range(1, tiradas + 1):
     desvios_corridaUno.append(np.std(corridaUno[:i]))

  axs[0].plot(desvios_corridaUno, label='Valor desvio estandar')
  axs[0].axhline(y=10.667, color='r', linestyle='-', label='Valor desvio estandar esperado= ' + str(10.667))
  axs[0].set_title('Valor desvio estandar de las tiradas de la corrida 1')
  axs[0].set_xlabel('Número de Tiradas')
  axs[0].set_ylabel('Valor desvio estandar')
  axs[0].legend()

  desvios_promedio = []
  for i in range(1, tiradas + 1):
      desvios_corridas = []
      for j in range(corridas):
          acumulado = resultados[j][:i]
          ds = np.std(acumulado)
          desvios_corridas.append(ds)
      promedio = np.mean(desvios_corridas)
      desvios_promedio.append(promedio)

  axs[2].plot(desvios_promedio, label='Valor desvio estandar')
  axs[2].axhline(y=10.667, color='r', linestyle='-', label='Valor desvio estandar esperado= ' + str(10.667))
  axs[2].set_title('Valor desvio estandar promediado en ' + str(corridas) + ' corridas')
  axs[2].set_xlabel('Número de Tiradas')
  axs[2].set_ylabel('Valor desvio estandar')
  axs[2].legend()

  desvios_por_corrida = []
  for j in range(0, corridas):
    desvios_por_corrida.append([])
    for i in range(0, tiradas):
      desvios_por_corrida[j].append(np.std(resultados[j][:i]))
  
  for i in range(0, corridas):
    num_tirada = i+1
    axs[1].plot(desvios_por_corrida[i], label='Valor desvio estandar (corrida ' + str(num_tirada) + ')')   
  
  axs[1].axhline(y=10.667, color='r', linestyle='-', label='Valor desvio estandar esperado = ' + str(10.667))
  axs[1].set_title('Valor desvio estandar de cada corrida')
  axs[1].set_xlabel('Número de Tiradas')
  axs[1].set_ylabel('Valor desvio estandar')
  axs[1].legend()
  plt.tight_layout()
  fig.savefig('desvio_estandar.png')

## Histograma de las medias muestrales, comprobando que la distribución de las medias muestrales aproxima a una distribucion normal (campana de Gauss) con un n >= 30
def graficar_histogramas(resultados: list, tiradas):
  medias_muestrales = np.mean(resultados, 0); 
  bins = np.arange(0, 38) - 0.5

  fig, axs = plt.subplots(1, 2, figsize=(18, 4))
  axs[1].hist(medias_muestrales, bins=bins, color='skyblue', edgecolor='black', density = True, rwidth = 0.8)
  axs[1].set_title(f'Distribución de Medias (n={str(tiradas)})')
  axs[1].set_xlabel('Media de la muestra')
  axs[1].set_ylabel('Densidad')

  datos_concatenados = np.array(resultados).flatten().tolist()

  axs[0].hist(datos_concatenados, bins=bins, color='skyblue', edgecolor='black', density = True, rwidth = 0.8)
  axs[0].set_title('Distribución Uniforme')
  axs[0].set_xlabel('Valor obtenido')
  axs[0].set_ylabel('Frecuencia')

  plt.tight_layout()
  fig.savefig('histograma_medias.png')

  


if(len(sys.argv) != 5 or sys.argv[1] != "-n"):
  print("Uso: main.py -n <num_valores> <tiradas> <corridas>")
  sys.exit(1)
n = int(sys.argv[2])
tiradas = int(sys.argv[3])
corridas = int(sys.argv[4])
resultados = generar_valores_aleatorios(tiradas, corridas)

graficar_frecuencia_relativa(tiradas, corridas, resultados, n)
graficar_valor_promedio(tiradas, corridas, resultados)
graficar_varianza(tiradas, corridas, resultados)
graficar_desvio_estandar(resultados, tiradas, corridas)
graficar_histogramas(resultados, tiradas)

plt.show()



