from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core import constants
from core.command_utils import bot_send_message, bot_edit_message

router = Router(name="info_commands_router")

@router.callback_query(F.data == "play_callback")
async def start_game(callback: CallbackQuery):
    await callback.answer(
        text="Спасибо за интерес!\n\nВ данный момент не реализовано.",
        show_alert=True
    )

@router.callback_query(F.data == "help_callback")
async def help_bot_callback(callback: CallbackQuery):
    await callback.answer(
        text="Спасибо за интерес!\n\nПомощь с ботом переедет на наш GitHub в ближайшее время.",
        show_alert=True
    )

@router.callback_query(F.data == "info_callback_exit")
async def info_close(callback: CallbackQuery):
    await send_start_command_text(callback.message.chat.id, True, callback.message.message_id)

# Возвращает клавиатуру с кнопками в меню Об игре.
def get_info_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="info_callback_exit"
        )
    )
    return builder

# Обработка кнопки Об игре
@router.callback_query(F.data == "info_callback")
async def info_bot_callback(callback: CallbackQuery):
    # Заменяем текст
    text = (
        f"Открытый космос - игровой бот про путешествия в открытом космосе от {constants.DEVELOPER_USERNAME}.\n"
        f"Исходный код и помощь с игрой: {constants.GITHUB_LINK}\n"
        "Последнее обновление - 24.10.2025"
    )
    await bot_edit_message(callback.message.chat.id, callback.message.message_id, text, get_info_keyboard().as_markup())

# Возвращает клавиатуру с кнопками в основном меню.
def get_main_info_commands_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Играть 🚀",
            callback_data="play_callback"
        ),
        InlineKeyboardButton(
            text="Помощь ❓",
            callback_data="help_callback"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Об игре ⚙️",
            callback_data="info_callback"
        )
    )
    return builder

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

# Обрабатывает команду /start. Отправляет текст и меню (с кнопками).
@router.message(CommandStart())
async def start_command_handler(message: Message):
    await send_start_command_text(chat_id=message.chat.id)
