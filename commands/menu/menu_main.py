from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from commands.menu import computer_menu
from commands.menu.menu_keyboards import get_back_keyboard, get_game_main_keyboard, get_create_game_keyboard
from commands.menu.navigation_menu import get_fly_text
from core import constants
from core.command_utils import bot_edit_message, callback_check_is_game_active, bot_send_message
from game import game_main
from game.game_main import user_allowed

menu_router = Router(name="menu_main_command_router")


# Изменяет текст и кнопки меню
async def update_menu(menu_name: str, chat_id: int, message_id: int, old_text: str):
    match menu_name:
        case "computer":
            new_text = computer_menu.get_computer_text(chat_id)
            if new_text != old_text:
                await bot_edit_message(chat_id, message_id,
                                       new_text, get_back_keyboard().as_markup())
            else:
                if constants.DEBUG_MODE:
                    print("Текст не изменился, невозможно обновить меню.")
        case "captain":
            new_text = "Не реализовано. Пока что"
            if new_text != old_text:
                await bot_edit_message(chat_id, message_id,
                                       new_text, get_back_keyboard().as_markup())
            else:
                if constants.DEBUG_MODE:
                    print("Текст не изменился, невозможно обновить меню.")

        case "navigation_waiting":
            ship = game_main.ALL_PLAYERS[chat_id]

            # Если полёт был завершен, выводим обычное меню навигации.
            if ship.tech_nav_clock == -1 and not ship.actions_blocked:
                ship.tech_screen = "main"
                game_main.ALL_PLAYERS[chat_id] = ship
                del ship
                return

            new_text = get_fly_text(ship)
            if new_text != old_text:
                await bot_edit_message(chat_id, message_id,
                                       new_text, get_back_keyboard().as_markup())
            else:
                if constants.DEBUG_MODE:
                    print("Текст не изменился, невозможно обновить меню.")

            del ship


@menu_router.callback_query(F.data == "menu_back")
async def bot_menu_back(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return
    await callback.answer("Возврат в главное меню")
    await bot_send_menu(callback.message.chat.id, callback.message.message_id)


@menu_router.callback_query(F.data == "menu_update_screen")
async def bot_update_menu(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return
    await update_menu(game_main.ALL_PLAYERS[callback.message.chat.id].tech_screen, callback.message.chat.id,
                      callback.message.message_id, callback.message.text)
    await callback.answer("Обновляем меню ...")


# Отправляет главное меню
async def bot_send_menu(chat_id: int, message_id: int = None):
    game_main.ALL_PLAYERS[chat_id].tech_screen = "main"
    if message_id is None:
        await bot_send_message(chat_id, "Меню управления кораблём", get_game_main_keyboard().as_markup())
    else:
        await bot_edit_message(chat_id, message_id, "Меню управления кораблём", get_game_main_keyboard().as_markup())


@menu_router.message(Command("menu"))
async def send_game_menu(message: Message):
    if not user_allowed(message.from_user.id):
        await message.reply(
            f"Уважаемый(ая) {message.from_user.first_name}!\n\nК сожалению, для Вас доступ к боту ограничен. Свяжитесь с разработчиками, чтобы получить доступ.")
        return
    if not game_main.is_game_active(message.chat.id):
        await bot_send_message(message.chat.id, "❌ Игра не активна!", get_create_game_keyboard().as_markup())
    else:
        await bot_send_menu(message.chat.id)
