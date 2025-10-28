from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from commands.menu.menu_keyboards import get_main_info_commands_keyboard, get_info_back_keyboard
from core import constants
from core.command_utils import bot_send_message, bot_edit_message
from game import start_game
from game.game_main import is_game_active

router = Router(name="info_commands_router")


@router.callback_query(F.data == "play_callback")
async def bot_start_game(callback: CallbackQuery):
    # Искусственно ограничиваем работу бота в группах / каналах. Это временно, я надеюсь.
    if callback.message.chat.type != ChatType.PRIVATE:
        await callback.answer(
            text="❌ В данный момент бот не работает в группах.",
            show_alert=True
        )
        return
    # Если игра уже активна, запрещаем создание новой игры.
    if is_game_active(callback.message.chat.id):
        await callback.answer(
            text="❌ Игра уже активна!",
            show_alert=True
        )
        return
    await callback.answer(text="Загружаем игру...")
    await start_game.start_new_game(callback.message.chat.id, callback.message.message_id)


@router.callback_query(F.data == "help_callback")
async def help_bot_callback(callback: CallbackQuery):
    await callback.answer(
        text="Спасибо за интерес!\n\nПомощь с ботом переедет на наш GitHub в ближайшее время.",
        show_alert=True
    )


@router.callback_query(F.data == "info_callback_exit")
async def info_close(callback: CallbackQuery):
    await send_start_command_text(callback.message.chat.id, True, callback.message.message_id)


# Обработка кнопки Об игре
@router.callback_query(F.data == "info_callback")
async def info_bot_callback(callback: CallbackQuery):
    # Заменяем текст
    text = (
        f"Открытый космос - игровой бот про путешествия в открытом космосе от {constants.DEVELOPER_USERNAME}.\n"
        f"Исходный код и помощь с игрой: {constants.GITHUB_LINK}\n"
    )
    await bot_edit_message(callback.message.chat.id, callback.message.message_id, text,
                           get_info_back_keyboard().as_markup())


# Заменяет или отправляет сообщение с основным меню.
async def send_start_command_text(chat_id: int, edit_text: bool = False, message_id: int = None):
    text = (
        "Привет! Добро пожаловать в открытый космос.\n"
        "Это игра, в которой Вам нужно выжить в космосе на космическом корабле.\n"
    )
    if not edit_text:
        await bot_send_message(chat_id, text, get_main_info_commands_keyboard().as_markup())
    else:
        await bot_edit_message(chat_id, message_id, text, get_main_info_commands_keyboard().as_markup())


# Обрабатывает команду /start. Отправляет приветствие (с кнопками).
@router.message(CommandStart())
async def start_command_handler(message: Message):
    await send_start_command_text(chat_id=message.chat.id)
