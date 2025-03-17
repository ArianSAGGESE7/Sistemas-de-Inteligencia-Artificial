# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 19:38:18 2025

@author: Arian
"""

import json 
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

# carga de pókemon

pokemon_file = "pokemon.json"

with open(pokemon_file,"r") as f:
    datos_pokemon = json.load(f)
     
# Pokebolas y pokemones

pokemon = ["jolteon", "caterpie", "snorlax", "onix", "mewtwo"]
pokebolas = ["pokeball", "ultraball", "fastball", "heavyball"]

# Generacion

gen_pokemon = PokemonFactory(pokemon_file)



# La idea es generar una función que utilice attemp catch pero para varios pokemones

def atrapar(pokemon,pokebola,intentos =1000):
    resultados = []
    resultados_promediados = []
    NIVEL = 100
    HP = 1
    for bolas in pokebolas:
        exitos = 0
        probabilidad_exito = []
        
        for _ in range(intentos):
            pokes = gen_pokemon.create(pokemon, NIVEL, StatusEffect.NONE, HP)
            exitos_tasa, capture = attempt_catch(pokes, bolas)
            
            if exitos_tasa:
                exitos += 1
            probabilidad_exito.append(capture)   
            
        resultados.append([pokemon,bolas,exitos/intentos,np.mean(probabilidad_exito)])
        
            
    return resultados
        
# Usamos esta función para cada uno de los pokemones 
            

all_results = []
for pkmn in pokemon:
    all_results.extend(atrapar(pkmn, pokebolas))

# Crear un DataFrame con los resultados
df_results = pd.DataFrame(all_results, columns=["Pokemon", "Pokebola", "Tasa exito", "Media de captura"])

print(df_results)

# Generar gráfico de barras
plt.figure(figsize=(12, 6))

# Colores para diferenciar las pokebolas
colors = {
    "pokeball": "black",
    "ultraball": "blue",
    "fastball": "grey",
    "heavyball": "red"
}

# Agrupar por pokebola y graficar
for ball in pokebolas:
    subset = df_results[df_results["Pokebola"] == ball]
    plt.bar(subset["Pokemon"], subset["Tasa exito"] * 100, color=colors[ball], alpha=0.8, label=ball)

# Etiquetas y título
plt.xlabel("Pokémon")
plt.ylabel("Tasa de Captura (%)")
plt.title("Probabilidad de Captura por Pokébola")
plt.legend(title="Pokebola")
plt.xticks(rotation=45)

# Mostrar el gráfico
plt.show()


## Punto 2

