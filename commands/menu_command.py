from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core import constants
from core.command_utils import bot_send_message, bot_edit_message, callback_check_is_game_active
from game import game_main
from game import start_game
from game.classes.player_ship import Ship

router = Router(name="menu_command_router")


async def update_menu(menu_name: str, chat_id: int, message_id: int, old_text: str):
    match menu_name:
        case "computer":
            new_text = get_computer_text(chat_id)
            if new_text != old_text:
                await bot_edit_message(chat_id, message_id,
                                       new_text, get_back_keyboard().as_markup())
            else:
                if constants.DEBUG_MODE:
                    print("Текст не изменился, невозможно обновить меню.")
        case "navigation":
            new_text = "Не реализовано."
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


@router.callback_query(F.data == "menu_start_game")
async def create_new_game_callback(callback: CallbackQuery):
    if game_main.is_game_active(callback.message.chat.id):
        return
    # Искусственно ограничиваем работу бота в группах / каналах. Это временно, я надеюсь.
    if callback.message.chat.type != ChatType.PRIVATE:
        await callback.answer(
            text="❌ В данный момент бот не работает в группах.",
            show_alert=True
        )
        return
    await callback.answer(text="Загружаем игру...")
    await start_game.start_new_game(callback.message.chat.id, callback.message.message_id)


# Возвращает клавиатуру с кнопкой назад (возврат в главное меню).
def get_back_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="menu_back"
        ),
        InlineKeyboardButton(
            text="🔄 Обновить",
            callback_data="menu_update_screen"
        )
    )
    return builder


@router.callback_query(F.data == "menu_back")
async def bot_menu_back(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return
    await callback.answer("Возврат в главное меню")
    await bot_send_menu(callback.message.chat.id, callback.message.message_id)


@router.callback_query(F.data == "menu_update_screen")
async def bot_update_menu(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return
    await update_menu(game_main.ALL_PLAYERS[callback.message.chat.id].screen, callback.message.chat.id,
                      callback.message.message_id, callback.message.text)
    await callback.answer("Обновляем меню ...")


# Возвращает клавиатуру с кнопкой создать игру. Используется, если игрок вводит команду меню, но при этом игра не активна.
def get_create_game_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🚀 Начать игру",
            callback_data="menu_start_game"
        )
    )
    return builder


def get_computer_text(chat_id: int) -> str:
    ship: Ship = game_main.ALL_PLAYERS[chat_id]
    return (
        f"🚀 Корабль {ship.ship_name}\n"
        "Состояние: 🟢\n"
        "======\n"
        f"💨 Скорость: {ship.speed}\n"
        f"🛡 Прочность: {ship.health}%\n"
    )


@router.callback_query(F.data == "menu_computer")
async def computer(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return
    game_main.ALL_PLAYERS[callback.message.chat.id].screen = "computer"
    await update_menu("computer", callback.message.chat.id, callback.message.message_id, callback.message.text)


@router.callback_query(F.data == "navigation_menu")
async def navigation(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return
    game_main.ALL_PLAYERS[callback.message.chat.id].screen = "navigation"
    await update_menu("navigation", callback.message.chat.id, callback.message.message_id, callback.message.text)


@router.callback_query(F.data == "menu_captain")
async def navigation(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return
    game_main.ALL_PLAYERS[callback.message.chat.id].screen = "captain"
    await update_menu("captain", callback.message.chat.id, callback.message.message_id, callback.message.text)


# Возвращает клавиатуру главного меню.
def get_game_main_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🖥 Компьютер",
            callback_data="menu_computer"
        ),
        InlineKeyboardButton(
            text="🗺 Навигация",
            callback_data="navigation_menu"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="⚓️ Главный отсек",
            callback_data="menu_captain"
        )
    )
    return builder


# Отправляет главное меню
async def bot_send_menu(chat_id: int, message_id: int = None):
    game_main.ALL_PLAYERS[chat_id].screen = "main"
    if message_id is None:
        await bot_send_message(chat_id, "Меню управления кораблём", get_game_main_keyboard().as_markup())
    else:
        await bot_edit_message(chat_id, message_id, "Меню управления кораблём", get_game_main_keyboard().as_markup())


@router.message(Command("menu"))
async def send_game_menu(message: Message):
    if not game_main.is_game_active(message.chat.id):
        await bot_send_message(message.chat.id, "❌ Игра не активна!", get_create_game_keyboard().as_markup())
    else:
        await bot_send_menu(message.chat.id)
