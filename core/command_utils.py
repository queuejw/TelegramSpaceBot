from aiogram.exceptions import TelegramNetworkError, TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, CallbackQuery

from core.bot_core import BOT
from game import game_main


def print_send_message_error(exception: str):
    print(f"[E] Не удалось отправить сообщение: {exception}")


def print_edit_message_error(exception: str):
    print(f"[E] Не удалось изменить сообщение: {exception}")


async def bot_send_message(chat_id: int, m_message: str, m_reply_markup: InlineKeyboardMarkup = None):
    try:
        await BOT.send_message(chat_id, text=m_message, reply_markup=m_reply_markup)
    except TelegramNetworkError as e:
        print_send_message_error(e.message)


async def bot_edit_message(chat_id: int, message_id: int, m_message: str, m_reply_markup: InlineKeyboardMarkup = None):
    try:
        await BOT.edit_message_text(text=m_message, chat_id=chat_id, message_id=message_id, reply_markup=m_reply_markup)
    except TelegramNetworkError as e:
        print_edit_message_error(e.message)
    except TelegramBadRequest as e:
        print_edit_message_error(e.message)


async def callback_check_is_game_active(callback: CallbackQuery) -> bool:
    if not game_main.is_game_active(callback.message.chat.id):
        await callback.answer(
            text="❌ Игра не активна",
            show_alert=True
        )
        return False
    return True
