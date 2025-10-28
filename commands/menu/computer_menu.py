from aiogram import F, Router
from aiogram.types import CallbackQuery

from commands.menu import menu_main
from core.command_utils import callback_check_is_game_active
from game import game_main
from game.classes.player_ship import Ship

menu_router = Router(name="menu_computer_command_router")


def get_computer_text(chat_id: int) -> str:
    ship: Ship = game_main.ALL_PLAYERS[chat_id]
    return (
        f"🚀 Корабль {ship.ship_name}\n"
        "Состояние: 🟢\n"
        "======\n"
        f"💨 Скорость: {ship.speed}\n"
        f"🛡 Прочность: {ship.health}%\n"
    )


@menu_router.callback_query(F.data == "menu_computer")
async def computer(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return
    game_main.ALL_PLAYERS[callback.message.chat.id].screen = "computer"
    await menu_main.update_menu("computer", callback.message.chat.id, callback.message.message_id,
                                callback.message.text)
