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
HP = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# Generacion

gen_pokemon = PokemonFactory(pokemon_file)



# La idea es generar una función que utilice attemp catch pero para varios pokemones

def atrapar(pokemon,pokebola,intentos,HP):
    resultados = []
    resultados_promediados = []
    NIVEL = 100
    
    
    for HPP in HP:
        for bolas in pokebolas:
            exitos = 0
            probabilidad_exito = []
            
            for _ in range(intentos):
                pokes = gen_pokemon.create(pokemon, HPP, StatusEffect.NONE, 1)
                exitos_tasa, capture = attempt_catch(pokes, bolas)

                if exitos_tasa:
                    exitos += 1
                probabilidad_exito.append(capture)   
                
            resultados.append([pokemon,HPP,bolas,exitos/intentos,np.mean(probabilidad_exito)])    
   
    return resultados
        
INTENTOS = 100;
pokemon_comparacion = ["caterpie","snorlax"]
resultados = []
for pkmn in pokemon_comparacion:
    resultados.extend((atrapar(pkmn, pokebolas,INTENTOS,HP)))
    
df_results = pd.DataFrame(resultados, columns=["Pokemon","HP", "Pokebola", "Tasa exito", "Media de captura"])

print(df_results)

pokemon_seleccionado = "caterpie"
df_filtrado = df_results[df_results["Pokemon"] == pokemon_seleccionado] # Selecciono solo los datos del pokemon que quiero 
sns.barplot(data=df_filtrado, x="HP", y="Tasa exito", hue="Pokebola")



plt.xlabel("HP")
plt.ylabel("Tasa de Éxito")
plt.title(f"Tasa de Captura según Estado y Pokébola ({pokemon_seleccionado})")
plt.legend(title="Pokébola")
plt.show()