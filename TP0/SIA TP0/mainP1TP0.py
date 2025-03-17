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

def atrapar(pokemon,pokebola,intentos):
    resultados = []
    resultados_por_tirada = []
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
            # resultados.append([pokemon,bolas,exitos/intentos,np.mean(probabilidad_exito)])
        
        resultados.append([pokemon,bolas,exitos/intentos,np.mean(probabilidad_exito)])
        
    
    return resultados
        
# Usamos esta función para cada uno de los pokemones 
            
INTENTOS = 100;
resultados = []
for pkmn in pokemon:
    resultados.extend((atrapar(pkmn, pokebolas,INTENTOS)))
    
# Ahora lo que quiero es reunir las estadisticas de cada bola por pojemon


    
# Crear un DataFrame con los resultados
df_results = pd.DataFrame(resultados, columns=["Pokemon", "Pokebola", "Tasa exito", "Media de captura"])

print(df_results)

# df_results = df_results[df_results["Pokemon"] == "caterpie"] # Selecciono solo los datos del pokemon que quiero 
df_sea = df_results.pivot(index = "Pokemon", columns = "Pokebola", values = "Tasa exito") # reordeno
sns.barplot(data=df_results, x="Pokebola", y="Tasa exito", hue="Pokemon")
#sns.barplot(df_results)

 # Etiquetas y título
plt.xlabel("Pokemon")
plt.ylabel("Tasa de Captura (%) = exitos/tiradas")
plt.title("Probabilidad de Captura por Pokébola")
plt.xticks(rotation=45)

# Mostrar el gráfico
plt.show()


## Punto 2

