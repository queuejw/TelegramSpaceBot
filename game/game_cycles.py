import asyncio
import random

from core import constants
from core.command_utils import bot_send_message
from core.manager import save_manager
from game import game_main
from game.classes.player_ship import Ship


def get_new_ship_speed(ship: Ship) -> int:
    current_speed = ship.speed
    if ship.fuel < 1:
        if random.random() < 0.75:
            current_speed = game_main.clamp(0, 1200, current_speed - random.randint(10, 25))
        else:
            current_speed = game_main.clamp(0, 1200, current_speed + random.randint(10, 25))
    else:
        if random.random() < 0.75 and current_speed < 1150:
            current_speed = game_main.clamp(0, 1200, current_speed + random.randint(25, 150))
        else:
            current_speed = game_main.clamp(0, 1200, current_speed - random.randint(25, 100))

    return current_speed


# Основной цикл игры.
async def main_game_cycle(chat_id: int):
    fuel_warning_enabled = True
    while game_main.is_game_active(chat_id):
        player_ship: Ship = game_main.ALL_PLAYERS[chat_id]

        # Завершаем игру, если прочность корабля на нуле
        if player_ship.health < 1:
            game_main.stop_game(chat_id)
            await bot_send_message(chat_id, "❌ Игра завершена!\n\nКорабль был уничтожен.")
            break

        if not player_ship.on_planet:  # Если мы не на планете
            # Если повезёт, уменьшаем количество топлива.
            if random.random() > 0.9:
                player_ship.fuel = game_main.clamp(0, 100, player_ship.fuel - 1)
        else:
            # Нулевая скорость, если мы на планете
            player_ship.speed = random.randint(0, 1)

        # Если закончилось топливо, уведомляем игрока и уменьшаем уровень кислорода
        if player_ship.fuel < 1:

            # Если везёт, уменьшаем кислорода
            if random.random() > 0.6:
                player_ship.oxygen = game_main.clamp(0, 100, player_ship.oxygen - 1)

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


# Цикл для работы системы полетов.
async def fly_cycle(chat_id: int, planet_name: str, leave: bool):
    time = random.randint(45, 120)
    if leave: time = random.randint(20, 40)

    game_main.ALL_PLAYERS[chat_id].actions_blocked = True

    while time > 0:
        time -= 1
        if not game_main.is_game_active(chat_id):
            if constants.DEBUG_MODE:
                print("Отмена полета, игра завершена.")
            return
        if game_main.ALL_PLAYERS[chat_id].fuel < 1:
            if constants.DEBUG_MODE:
                print("Отмена полета, топливо закончилось")
            game_main.ALL_PLAYERS[chat_id].actions_blocked = False
            await bot_send_message(chat_id,
                                   "⚠️ Мы не можем продолжить полёт!\n\nДвигатели отключены из-за нехватки топлива")
            return

        game_main.ALL_PLAYERS[chat_id].tech_nav_clock = time
        await asyncio.sleep(1)

    if constants.DEBUG_MODE:
        print("Полёт завершен.")
    game_main.ALL_PLAYERS[chat_id].actions_blocked = False
    game_main.ALL_PLAYERS[chat_id].tech_nav_clock = -1
    if leave:
        game_main.ALL_PLAYERS[chat_id].on_planet = False
        await bot_send_message(chat_id, f"✅ Мы успешно покинули планету {planet_name}!")
    else:
        game_main.ALL_PLAYERS[chat_id].on_planet = True
        await bot_send_message(chat_id, f"✅ Полёт успешно завершён.\nДобро пожаловать на планету {planet_name}!")
