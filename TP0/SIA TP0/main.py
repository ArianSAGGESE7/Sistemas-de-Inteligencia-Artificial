import json
import matplotlib.pyplot as plt
import pandas as pd
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

N = 100
balls = ["pokeball", "ultraball", "fastball", "heavyball"]
pokemon_configs = ["configs\caterpie.json", "configs\snorlax.json"]
status_effects = [StatusEffect.NONE, StatusEffect.BURN, StatusEffect.FREEZE, StatusEffect.PARALYSIS, StatusEffect.POISON, StatusEffect.SLEEP]
levels_of_life = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

if __name__ == "__main__":
    factory = PokemonFactory("pokemon.json")
    
    for config_file in pokemon_configs:
        with open(config_file, "r") as f:
            config = json.load(f)
            best_combination = None
            highest_probability = 0
            data = []

            for status in status_effects:
                for level in levels_of_life:
                    pokemon = factory.create(config["pokemon"], 100, status, level)
                    
                    results = {ball: 0 for ball in balls}
                    for ball in balls:
                        success_count = 0
                        for i in range(N):
                            caught, _ = attempt_catch(pokemon, ball)
                            if caught:
                                success_count += 1
                        results[ball] = success_count / N

                    print(f"Results for {config['pokemon']} with status {status.name} and life level {level}:")
                    for ball, probability in results.items():
                        print(f"Probability of catching with {ball}: {probability * 100:.2f}%")
                        data.append([config["pokemon"], status.name, level, ball, probability * 100])

                    # Encontrar la mejor combinación
                    max_ball = max(results, key=results.get)
                    max_probability = results[max_ball]
                    if max_probability > highest_probability:
                        highest_probability = max_probability
                        best_combination = (config["pokemon"], status.name, level, max_ball, max_probability)

                    # Crear gráfico de barras
                    # plt.bar(results.keys(), [prob * 100 for prob in results.values()])
                    # plt.xlabel('Pokebola')
                    # plt.ylabel('Probabilidad de captura (%)')
                    # plt.title(f'Probabilidad de captura promedio para cada pokebola ({config["pokemon"]} - {status.name} - Vida {level})')
                    # plt.show()

            if best_combination:
                print(f"La mejor combinación para {best_combination[0]} es:")
                print(f"Estado: {best_combination[1]}, Nivel de vida: {best_combination[2]}, Pokebola: {best_combination[3]}, Probabilidad: {best_combination[4] * 100:.2f}%")

            # Crear y mostrar la tabla de resultados
            df = pd.DataFrame(data, columns=["Pokemon", "Estado", "Nivel de vida", "Pokebola", "Probabilidad (%)"])
            print(df)