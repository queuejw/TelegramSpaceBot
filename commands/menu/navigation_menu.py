import asyncio
import random

from aiogram import F, Router
from aiogram.types import CallbackQuery

from commands.menu import menu_main
from commands.menu.menu_keyboards import get_menu_navigation_keyboard, get_on_planet_menu_navigation_keyboard
from core import constants
from core.command_utils import callback_check_is_game_active, bot_edit_message, bot_send_message
from game import game_main
from game.classes.planet import Planet
from game.classes.player_ship import Ship
from game.game_cycles import fly_cycle

menu_router = Router(name="menu_navigation_command_router")
current_planet = {}  # Текущая планета в списке: chat_id - planet_id


# Возвращает эмодзи в зависимости от уровня угрозы
def get_danger_emoji(level: int) -> str:
    if level <= 3:
        return "✅"
    if 4 <= level <= 6:
        return "⚠️"
    if 7 <= level <= 9:
        return "⛔️"
    if level >= 10:
        return "☢️"

    return "⚠️"


# Возвращает текст с описанием планеты
def get_navigation_text(planet: Planet) -> str:
    text = (
        f"🪐 {planet.name}\n\n"
        f"📂 {planet.description}\n\n"
        f"{get_danger_emoji(planet.danger)} Уровень опасности: {planet.danger}"
    )
    return text


# Обновляет id выбранной планеты
def update_page_value(chat_id: int, is_next: bool):
    if current_planet[chat_id] - 1 < 0:
        current_planet[chat_id] = len(game_main.PLANETS) - 1

    if current_planet[chat_id] + 1 > len(game_main.PLANETS):
        current_planet[chat_id] = 0

    if is_next:
        current_planet[chat_id] += 1
    else:
        current_planet[chat_id] -= 1


@menu_router.callback_query(F.data.contains("_action_navigation_menu"))
async def change_navigation_menu_page(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return

    match callback.data:

        # Игрок листает список назад
        case "back_action_navigation_menu":
            if constants.DEBUG_MODE:
                print("Назад")
            update_page_value(callback.message.chat.id, False)
            await update_navigation_menu(callback.message.chat.id, callback.message.message_id,
                                         get_navigation_text(
                                             game_main.get_planet_by_id(current_planet[callback.message.chat.id])))

        # Игрок листает список дальше
        case "next_action_navigation_menu":
            if constants.DEBUG_MODE:
                print("Дальше")
            update_page_value(callback.message.chat.id, True)
            await update_navigation_menu(callback.message.chat.id, callback.message.message_id,
                                         get_navigation_text(
                                             game_main.get_planet_by_id(current_planet[callback.message.chat.id])))
        # Игрок выбрал планету
        case "accept_action_navigation_menu":
            if constants.DEBUG_MODE:
                print("Выбрана планета.")

            planet = game_main.get_planet_by_id(current_planet[callback.message.chat.id])
            asyncio.create_task(fly_cycle(callback.message.chat.id, planet.name, False))
            await menu_main.bot_send_menu(callback.message.chat.id, callback.message.message_id)
            await bot_send_message(callback.message.chat.id, f"🕒 Отправляемся на планету {planet.name} ...")
            del planet

        # Игрок покидает планету
        case "leave_planet_action_navigation_menu":
            if constants.DEBUG_MODE:
                print("Игрок хочет покинуть планету.")

            planet = game_main.get_planet_by_id(game_main.ALL_PLAYERS[callback.message.chat.id].planet_id)
            asyncio.create_task(fly_cycle(callback.message.chat.id, planet.name, True))
            await menu_main.bot_send_menu(callback.message.chat.id, callback.message.message_id)
            await bot_send_message(callback.message.chat.id, f"🕒 Покидаем планету {planet.name} ...")
            del planet

    await callback.answer("> Обработка информации ...")


async def update_navigation_menu(chat_id: int, message_id: int, new_text: str):
    await bot_edit_message(chat_id, message_id, new_text, get_menu_navigation_keyboard().as_markup())


def get_on_planet_text(planet: Planet) -> str:
    return (
        f"Сейчас мы находимся на планете {planet.name}\n\n"
        f"📂 {planet.description}\n\n"
        f"Чтобы выбрать другую планету, сначала нужно покинуть эту."
    )


def get_fly_text(ship: Ship) -> str:
    return (
        f"🚀 Корабль находится в пути!\n\n"
        f"🕒 Осталось {ship.tech_nav_clock} секунд до завершения полёта."
    )


async def handle_navigation_callback(chat_id: int, message_id: int, old_text: str):
    ship: Ship = game_main.ALL_PLAYERS[chat_id]

    # Если корабль в пути, блокируем другие варианты меню.
    if ship.actions_blocked and ship.tech_nav_clock != -1:
        ship.tech_screen = "navigation_waiting"
        game_main.ALL_PLAYERS[chat_id] = ship
        await menu_main.update_menu("navigation_waiting", chat_id, message_id,
                                    old_text)
        return

    if not ship.on_planet:
        planet = random.choice(game_main.PLANETS)
        current_planet[chat_id] = planet.id
        await update_navigation_menu(chat_id, message_id, get_navigation_text(planet))
        del planet
    else:
        planet = game_main.get_planet_by_id(ship.planet_id)
        await bot_edit_message(chat_id, message_id, get_on_planet_text(planet),
                               get_on_planet_menu_navigation_keyboard().as_markup())
        del planet

    del ship


@menu_router.callback_query(F.data == "navigation_menu")
async def navigation(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return

    await handle_navigation_callback(callback.message.chat.id, callback.message.message_id, callback.message.text)
