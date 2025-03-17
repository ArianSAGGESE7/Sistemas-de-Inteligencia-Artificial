import json
import matplotlib.pyplot as plt
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

N = 100
balls = ["pokeball", "ultraball", "fastball", "heavyball"]
pokemon_configs = ["TP0\SIA TP0\configs\caterpie.json", "TP0\SIA TP0\configs\snorlax.json"]
status_effects = [StatusEffect.NONE, StatusEffect.BURN, StatusEffect.FREEZE, StatusEffect.PARALYSIS, StatusEffect.POISON, StatusEffect.SLEEP]

if __name__ == "__main__":
    factory = PokemonFactory("TP0\SIA TP0\pokemon.json")
    
    for config_file in pokemon_configs:
        with open(config_file, "r") as f:
            config = json.load(f)
            for status in status_effects:
                pokemon = factory.create(config["pokemon"], 100, status, 1)
                
                results = {ball: 0 for ball in balls}
                for ball in balls:
                    success_count = 0
                    for i in range(N):
                        caught, _ = attempt_catch(pokemon, ball)
                        if caught:
                            success_count += 1
                    results[ball] = success_count / N

                print(f"Results for {config['pokemon']} with status {status.name}:")
                for ball, probability in results.items():
                    print(f"Probability of catching with {ball}: {probability * 100:.2f}%")

                # Crear gráfico de barras
                plt.bar(results.keys(), [prob * 100 for prob in results.values()])
                plt.xlabel('Pokebola')
                plt.ylabel('Probabilidad de captura (%)')
                plt.title(f'Probabilidad de captura promedio para cada pokebola ({config["pokemon"]} - {status.name})')
                plt.show()