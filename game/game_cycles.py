import asyncio
import random

from core import constants
from core.manager import save_manager
from game import game_main
from game.classes.player_ship import Ship


def get_new_ship_speed(ship: Ship) -> int:
    if ship.fuel < 1:
        return random.randint(100, 199)
    return game_main.clamp(100, 9999, ship.speed + random.randint(-45, 145))


# Основной цикл игры.
async def main_game_cycle(chat_id: int):
    while game_main.is_game_active(chat_id):
        player_ship: Ship = game_main.ALL_PLAYERS[chat_id]
        player_ship.speed = get_new_ship_speed(player_ship)

        # Изменение переменных завершено.
        game_main.ALL_PLAYERS[chat_id] = player_ship
        if constants.DEBUG_MODE:
            print(f"Основной цикл для чата {chat_id} завершён")
        save_manager.save_ship_state(chat_id,
                                     player_ship.export_as_dict())  # Надо перенести авто-сохранения в другое место
        await asyncio.sleep(10)
