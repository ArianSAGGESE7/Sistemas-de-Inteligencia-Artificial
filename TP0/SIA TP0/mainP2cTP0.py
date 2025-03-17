# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 23:07:16 2025

@author: USUARIO
"""

# Verificamos si las condiciones de salud tienen algun efecto sobre la efectividad de captura
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
NIVEL = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# Generacion

gen_pokemon = PokemonFactory(pokemon_file)



# La idea es generar una función que utilice attemp catch pero para varios pokemones

def atrapar(pokemon,pokebola,intentos,NIVEL):
    resultados = []
    resultados_promediados = []
    HP = 1
    
    for NV in NIVEL:
        for bolas in pokebolas:
            exitos = 0
            probabilidad_exito = []
            
            for _ in range(intentos):
                pokes = gen_pokemon.create(pokemon, NV, StatusEffect.NONE, HP)
                exitos_tasa, capture = attempt_catch(pokes, bolas)

                if exitos_tasa:
                    exitos += 1
                probabilidad_exito.append(capture)   
                
            resultados.append([pokemon,NV,bolas,exitos/intentos,np.mean(probabilidad_exito)])    
   
    return resultados

INTENTOS = 100;

resultados = []
for pkmn in pokemon:
    resultados.extend((atrapar(pkmn, pokebolas,INTENTOS,NIVEL)))
    
df_results = pd.DataFrame(resultados, columns=["Pokemon","NIVEL", "Pokebola", "Tasa exito", "Media de captura"])
# df_results =  df_results[df_results["Pokebola"] == "pokeball"]
print(df_results)

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_results, x="NIVEL", y="Tasa exito", hue="Pokemon", marker="o",ci="sd")
plt.show()



