from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.types import CallbackQuery

from game import game_main, start_game

menu_router = Router(name="menu_start_game_command_router")


@menu_router.callback_query(F.data == "menu_start_game")
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
