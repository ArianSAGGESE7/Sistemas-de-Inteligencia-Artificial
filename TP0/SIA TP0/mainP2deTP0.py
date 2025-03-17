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
NIVEL = 10
HP =0.1
# Generacion

gen_pokemon = PokemonFactory(pokemon_file)



# La idea es generar una función que utilice attemp catch pero para varios pokemones

def atrapar(pokemon,pokebola,intentos,NIVEL,HP,estado):
    resultados = []
    resultados_promediados = []
    
    for bolas in pokebolas:
        exitos = 0
        probabilidad_exito = []
        
        for _ in range(intentos):
            pokes = gen_pokemon.create(pokemon, NIVEL, StatusEffect[estado], HP)
            exitos_tasa, capture = attempt_catch(pokes, bolas)
            
            if exitos_tasa:
                exitos += 1
            probabilidad_exito.append(capture)   
            
        resultados.append([pokemon,bolas,exitos/intentos,np.mean(probabilidad_exito)])   
   
    return resultados

INTENTOS = 100;

resultados = []
for pkmn in pokemon:
    resultados.extend((atrapar(pkmn, pokebolas,INTENTOS,NIVEL,HP,"SLEEP")))
    
pokemon_seleccionado = "caterpie"
df_results = pd.DataFrame(resultados, columns=["Pokemon", "Pokebola", "Tasa exito", "Media de captura"])
print(df_results)

plt.figure(figsize=(10, 6))
sns.barplot(data=df_results, x="Pokemon", y="Tasa exito", hue="Pokebola")
plt.xlabel("Estado del Pokémon")
plt.ylabel("Tasa de Éxito")
plt.title(f"Tasa de Captura según Estado y Pokébola ({pokemon_seleccionado})")
plt.legend(title="Pokébola")
plt.show()





