import random

from aiogram import F, Router
from aiogram.types import CallbackQuery

from commands.menu.menu_keyboards import get_menu_navigation_keyboard, get_on_planet_menu_navigation_keyboard
from core import constants
from core.command_utils import callback_check_is_game_active, bot_edit_message
from game.classes.planet import Planet
from game.classes.player_ship import Ship
from game.game_main import PLANETS, get_planet_by_id, ALL_PLAYERS

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
        current_planet[chat_id] = len(PLANETS) - 1

    if current_planet[chat_id] + 1 > len(PLANETS):
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
                                             get_planet_by_id(current_planet[callback.message.chat.id])))

        # Игрок листает список дальше
        case "next_action_navigation_menu":
            if constants.DEBUG_MODE:
                print("Дальше")
            update_page_value(callback.message.chat.id, True)
            await update_navigation_menu(callback.message.chat.id, callback.message.message_id,
                                         get_navigation_text(
                                             get_planet_by_id(current_planet[callback.message.chat.id])))
        # Игрок выбрал планету
        case "accept_action_navigation_menu":
            if constants.DEBUG_MODE:
                print("Выбрана планета.")

        # Игрок покидает планету
        case "leave_planet_action_navigation_menu":
            if constants.DEBUG_MODE:
                print("Игрок хочет покинуть планету.")

    await callback.answer("> Обработка информации ...")


async def update_navigation_menu(chat_id: int, message_id: int, new_text: str):
    await bot_edit_message(chat_id, message_id, new_text, get_menu_navigation_keyboard().as_markup())


def get_on_planet_text(planet: Planet) -> str:
    return (
        f"Сейчас мы находимся на планете {planet.name}\n\n"
        f"📂 {planet.description}\n\n"
        f"Чтобы выбрать другую планету, сначала нужно покинуть эту."
    )


@menu_router.callback_query(F.data == "navigation_menu")
async def navigation(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return
    ship: Ship = ALL_PLAYERS[callback.message.chat.id]
    if not ship.on_planet:
        planet = random.choice(PLANETS)
        current_planet[callback.message.chat.id] = planet.id
        await update_navigation_menu(callback.message.chat.id, callback.message.message_id, get_navigation_text(planet))
        del planet
    else:
        planet = get_planet_by_id(ship.planet_id)
        await bot_edit_message(callback.message.chat.id, callback.message.message_id, get_on_planet_text(planet),
                               get_on_planet_menu_navigation_keyboard().as_markup())
        del planet

    del ship
