from aiogram import F, Router
from aiogram.types import CallbackQuery

from commands.menu.menu_main import update_menu
from core.command_utils import callback_check_is_game_active
from game import game_main

menu_router = Router(name="menu_captain_command_router")


@menu_router.callback_query(F.data == "menu_captain")
async def navigation(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return
    game_main.ALL_PLAYERS[callback.message.chat.id].screen = "captain"
    await update_menu("captain", callback.message.chat.id, callback.message.message_id, callback.message.text)
