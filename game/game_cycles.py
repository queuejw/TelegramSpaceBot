import asyncio
import random

from core import constants
from core.command_utils import bot_send_message
from core.manager import save_manager
from game import game_main
from game.classes.player_ship import Ship
from game.game_main import clamp, stop_game


def get_new_ship_speed(ship: Ship) -> int:
    current_speed = ship.speed
    if ship.fuel < 1:
        if random.random() < 0.75:
            current_speed = clamp(0, 9999, current_speed - random.randint(10, 125))
        else:
            current_speed = clamp(0, 9999, current_speed + random.randint(5, 25))
    else:
        if random.random() < 0.75:
            current_speed = clamp(0, 9999, current_speed + random.randint(100, 400))
        else:
            current_speed = clamp(0, 9999, current_speed - random.randint(5, 100))

    return current_speed


# Основной цикл игры.
async def main_game_cycle(chat_id: int):
    fuel_warning_enabled = True
    while game_main.is_game_active(chat_id):
        player_ship: Ship = game_main.ALL_PLAYERS[chat_id]

        # Завершаем игру, если прочность корабля на нуле
        if player_ship.health < 1:
            stop_game(chat_id)
            await bot_send_message(chat_id, "❌ Игра завершена!\n\nКорабль был уничтожен.")
            break

        # Если повезёт, уменьшаем количество топлива.
        if random.random() > 0.9:
            player_ship.fuel = clamp(0, 100, player_ship.fuel - 1)

        # Если закончилось топливо, уведомляем игрока и уменьшаем уровень кислорода
        if player_ship.fuel < 1:

            # Если везёт, уменьшаем кислорода
            if random.random() > 0.6:
                player_ship.oxygen = clamp(0, 100, player_ship.oxygen - 1)

            if fuel_warning_enabled:
                fuel_warning_enabled = False
                await bot_send_message(chat_id,
                                       "⚠️ Закончилось топливо!\n\nПодача кислорода приостановлена из-за отключения генераторов.")
        else:
            if not fuel_warning_enabled:
                fuel_warning_enabled = True

        # Когда кислород заканчивается, мы должны медленно убивать экипаж корабля. В данный момент это не реализовано, поскольку я хочу сделать более масштабную систему экипажей.
        if player_ship.oxygen < 1:
            pass

        player_ship.speed = get_new_ship_speed(player_ship)

        # Изменение переменных завершено.
        game_main.ALL_PLAYERS[chat_id] = player_ship
        if constants.DEBUG_MODE:
            print(f"Основной цикл для чата {chat_id} завершён")

        del player_ship
        await asyncio.sleep(10)

    if constants.DEBUG_MODE:
        print(f"Основной цикл для чата {chat_id} был завершён. Это должно означать конец игры или её приостановку.")


# Цикл для создания различных внутриигровых событий
async def event_game_cycle(chat_id: int):
    while game_main.is_game_active(chat_id):
        player_ship: Ship = game_main.ALL_PLAYERS[chat_id]
        save_manager.save_ship_state(chat_id,
                                     player_ship.export_as_dict())
        del player_ship
        await asyncio.sleep(30)


# Цикл для работы авто-сохранения игры и других технических штук
async def tech_game_cycle(chat_id: int):
    while game_main.is_game_active(chat_id):
        player_ship: Ship = game_main.ALL_PLAYERS[chat_id]
        save_manager.save_ship_state(chat_id,
                                     player_ship.export_as_dict())
        del player_ship
        await asyncio.sleep(60)
