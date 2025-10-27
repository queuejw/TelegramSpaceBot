import json

from core import constants
from game.classes.planet import Planet


# Загружает список планет из json файла.
def load_planets() -> list:
    if constants.DEBUG_MODE:
        print(f"Попытка загрузить планеты из файла {constants.PLANETS_PATH}")
    try:
        with open(constants.PLANETS_PATH, 'r', encoding="utf-8") as planets_file:
            planets = json.load(planets_file)
            planets_file.close()
            if constants.DEBUG_MODE:
                print(f"Планеты успешно загружены, создание списка ...")
                print(planets)

            generated_list = []
            for m in planets:
                generated_list.append(Planet(m['name'], m['description'], m['danger']))
            return generated_list
    except FileNotFoundError:
        print(
            f"[E] Файл {constants.PLANETS_PATH}, который должен содержать планеты, не найден. Невозможно продолжить работу.")
        exit(1)
