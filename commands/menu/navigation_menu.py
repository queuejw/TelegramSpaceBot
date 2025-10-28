import random

from aiogram import F, Router
from aiogram.types import CallbackQuery

from commands.menu.menu_keyboards import get_menu_navigation_keyboard
from core import constants
from core.command_utils import callback_check_is_game_active, bot_edit_message
from game.classes.planet import Planet
from game.game_main import PLANETS

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


# Возвращает планету по её ID
def get_planet_by_id(m_id: int) -> Planet:
    l = [x for x in PLANETS if x.id == m_id]
    if len(l) < 1:
        return random.choice(PLANETS)
    return l[0]


@menu_router.callback_query(F.data.contains("_action_navigation_menu"))
async def change_navigation_menu_page(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return
    if callback.data == "back_action_navigation_menu":
        if constants.DEBUG_MODE:
            print("Назад")
        update_page_value(callback.message.chat.id, False)
        await update_navigation_menu(callback.message.chat.id, callback.message.message_id, callback.message.text,
                                     get_navigation_text(get_planet_by_id(current_planet[callback.message.chat.id])))
    if callback.data == "next_action_navigation_menu":
        if constants.DEBUG_MODE:
            print("Дальше")
        update_page_value(callback.message.chat.id, True)
        await update_navigation_menu(callback.message.chat.id, callback.message.message_id, callback.message.text,
                                     get_navigation_text(get_planet_by_id(current_planet[callback.message.chat.id])))


async def update_navigation_menu(chat_id: int, message_id: int, old_text: str, new_text: str):
    await bot_edit_message(chat_id, message_id, new_text, get_menu_navigation_keyboard().as_markup())


@menu_router.callback_query(F.data == "navigation_menu")
async def navigation(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return
    planet = random.choice(PLANETS)
    current_planet[callback.message.chat.id] = planet.id
    await update_navigation_menu(callback.message.chat.id, callback.message.message_id, callback.message.text,
                                 get_navigation_text(planet))
