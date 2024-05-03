"""
@Author: Rubén Luque
@date: 13/11/2023
@email: luqueruben@uniovi.es
"""
import random
import time

player_name = ""
health = 100
protector = ""
coins = 0
animals = ["Lobo", "Oso", "Tigre", "Rottweiler", "Akita Inu"]
treasures = ["monedas de oro", "latas de cobre", "baratijas", "kgs de arroz"]

"""
Juego sencillo con 1 sola condición de victoria: Encontrar 5 monedas de oro y salud > 0.
Y una condición de derrota: Tu salud es 0 o menor.
"""


def start_adventure():
    global player_name
    print("Bienvenido a la Aventura en el Bosque Encantado.")
    player_name = input("¿Serías tan amable de indicarme tu nombre?: ").capitalize()
    print(f"Hola {player_name}, comenzamos...\n")

    while True:
        choice = input(
            "Ves un camino que se divide en dos: ¿Vas a la izquierda "
            "o a la derecha? (I/D) ").lower()
        if choice in ["izquierda", "i"]:
            # Genero número aleatorio para el animal
            animal_id = random.randrange(0, len(animals))  # No llega al fin, se queda en uno menos.
            encounter_animal(animals[animal_id])
        elif choice in ["derecha", "d"]:
            treasure_id = random.randrange(0, len(treasures))  # No llega al fin, se queda en uno
            find_treasure(treasures[treasure_id])
        else:
            print("Opción no válida. Elige 'I' o 'D'.")

        if check_game_over():
            print(f"FIN DEL JUEGO!\n"
                  f"Lo siento {player_name}, has perdido. "
                  f"Salud: {health}. Monedas: {coins}")
            break
        if check_victory():
            print(f"FIN DEL JUEGO!\n"
                  f"Enhorabuena {player_name}!! Has ganado la partida. "
                  f"Salud: {health}. Monedas: {coins}")
            break


def encounter_animal(animal_name):
    global protector
    print(f"¡Te encuentras con un {animal_name}!. Parece hambriento...")
    action = input("¿Qué haces? (correr(C)/pelear(P)/alimentar(A)): ").lower()
    if action in ["correr", "c"]:
        print(f"Corres rápido y escapas del {animal_name}. ¡Seguro por ahora!")
    elif action in ["pelear", "p"]:
        print(f"Decides enfrentarte al {animal_name}.")
        fight_animal(animal_name)
    elif action in ["alimentar", "a"]:
        print(f"Le das tu comida al {animal_name}. "
              f"Se convierte en tu amigo y te acompaña en tu aventura.")
        protector = animal_name
    else:
        print("Opción no válida.")


def fight_animal(animal_name):
    global health
    # global nombre  # Si solo leemos su valor, no hace falta definirla aquí como global
    strength = int(input("¿Cuánto mides tu fuerza en una escala de 1 a 10?: "))
    protector_help = ""

    while strength < 1 or strength > 10:
        strength = int(input("ERROR: Te he dicho una escala de 1 a 10! Introduce otra vez: "))
    if len(protector) > 0:
        protector_help = f"Tu {protector} te ayuda atacando al {animal_name}\n"
        damage_reduction_factor = 0.5  # Si tienes protector, se reduce el daño a la mitad
    else:
        damage_reduction_factor = 1  # Sin protector, el daño es completo
    if strength > 5:
        damage = random.randint(0, 50)
        health -= damage * damage_reduction_factor
        print(f"Tu fuerza es suficiente. Vences al {animal_name} en la pelea. {protector_help}Salud actual: {health}")
    else:
        damage = random.randint(20, 100)
        health -= damage * damage_reduction_factor
        print(f"No eres lo suficientemente fuerte. Lo siento {player_name}, {animal_name} te vence."
              f"{protector_help}Salud actual: {health}")


def find_treasure(treasure_name):
    global coins
    print("Encuentras un tesoro escondido detrás de un árbol...\n"
          "Vamos a ver que hay....")
    quantity_found = 0
    for i in range(random.randrange(0, 6)):
        quantity_found += 1
        print(f"Descubriendo el tesoro, espera... ")
        time.sleep(1)
    if treasure_name == "monedas de oro":
        coins += quantity_found
    print(f"Has encontrado {quantity_found} {treasure_name}. ¡Felicidades {player_name}!."
          f" Tienes: {coins} monedas de oro.")


def check_game_over():
    return health <= 0


def check_victory():
    return health > 0 and coins >= 5


start_adventure()
