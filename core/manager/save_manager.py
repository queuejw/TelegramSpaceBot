import json
import os

from core import constants
from game.classes.player_ship import Ship


def create_random_name() -> str:
    return "TestPlane-52"


def get_default_ship(chat_id: int) -> Ship:
    return Ship(chat_id, create_random_name())


# Загружает сохранение игрока. Если его нет, создает новый корабль. Возвращает словарь со значениями ship : Ship, default: bool
def load_ship_state(chat_id: int) -> dict:
    path = f'{constants.SAVES_PATH}\\{chat_id}\\save.json'
    if constants.DEBUG_MODE:
        print(f"Попытка загрузить файл {path}")
    try:
        with open(path, 'r', encoding="utf-8") as save_file:
            state = json.load(save_file)
            save_file.close()
            if constants.DEBUG_MODE:
                print(f"Файл {path} успешно загружен")
                print(state)
            return {
                'default': False,
                'ship': Ship(chat_id, 'loaded').import_from_dict(state)
            }
    except FileNotFoundError:
        print(f"[E] Файл {path} не найден. Используем стандартный.")

    # Если загрузить не удалось, возвращаем None.
    default = get_default_ship(chat_id)
    save_ship_state(chat_id, default.export_as_dict())
    return {
        'default': True,
        'ship': default
    }


def save_ship_state(chat_id: int, state: dict):
    folder_path = f'{constants.SAVES_PATH}\\{chat_id}\\'
    path = f'{folder_path}\\save.json'
    if constants.DEBUG_MODE:
        print(f"Попытка сохранить на диск файл {path}")
    try:
        os.makedirs(folder_path, exist_ok=True)
        with open(path, 'w', encoding="utf-8") as save_file:
            save_file.write(json.dumps(state, indent=4, ensure_ascii=False))
            save_file.close()
    except IOError as e:
        print(f"[E] По какой-то причине не удалось сохранить файл {path}. Детали: {e}")
    pass
