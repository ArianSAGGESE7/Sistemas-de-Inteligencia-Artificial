import json
import sys
import matplotlib.pyplot as plt

from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

config_file = "configs/caterpie.json"  # Archivo fijo

with open(config_file, "r") as f:
    config = json.load(f)

factory = PokemonFactory("pokemon.json")
ball = config["pokeball"]
pokemon = factory.create(config["pokemon"], 100, StatusEffect.NONE, 1)

# for i in range(100, 1, -1):
#     pokemon = factory.create(config["pokemon"], 100, StatusEffect.NONE, i / 100)
#     print(pokemon.current_hp)

#print("No noise: ", attempt_catch(pokemon, ball))
#for i in range(10):
#    print("Noisy: ", attempt_catch(pokemon, ball, 0.15*i))


print("Pruebas")
resultados = []
probabilidades = []
booleans = []
bolas = ["pokeball","ultraball","fastball","heavyball"]
# for ball in bolas:   
#         print("Tipo de bola:    ",ball)
#         print("Ruido: off")
#         bolean,prob=attempt_catch(pokemon, ball)
        
#         resultados.append((ball,bolean,prob))
#         print("iteracion",resultados)
        
        
for ball in bolas:
    for i in range(100):
        bolean,prob=attempt_catch(pokemon, ball)
        resultados.append((ball,bolean,prob))
        probabilidades.append(prob)
        booleans.append(bolean)
        
#  Calculo promedio de probabilidad 
Prob_captura_media = 0

for proba in probabilidades[0:99]:
    Prob_captura_media += proba     
        
Prob_captura_media = Prob_captura_media/100;

contador_true = 0
contador_false = 0

for atrapado in booleans[0:99]:
    if atrapado:
        contador_true += 1
    else:
        contador_false += 1


print(Prob_captura_media)

# Gráfico de línea
plt.figure(figsize=(10, 5))
plt.show()
plt.plot(range(1, len(probabilidades[0:99]) + 1), probabilidades[0:99], marker="o", linestyle="-", color="b", label="Probabilidad por intento")

plt.figure(figsize=(10, 5))
plt.show()
plt.hist(probabilidades[0:99], bins=10, color="c", edgecolor="black", alpha=0.7)
