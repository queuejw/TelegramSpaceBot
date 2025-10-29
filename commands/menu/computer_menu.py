from aiogram import F, Router
from aiogram.types import CallbackQuery

from commands.menu import menu_main
from core.command_utils import callback_check_is_game_active
from game import game_main
from game.classes.player_ship import Ship

menu_router = Router(name="menu_computer_command_router")


# Возвращает эмодзи со значением статуса корабля.
def get_ship_status_emoji(ship: Ship) -> str:
    crew_sum_health = 0 * 100  # Общее максимально возможное здоровье членов экипажа. Например, если на корабле 2 игрока, значение будет равно 200.

    current_level = ship.health + ship.oxygen + ship.fuel + 0  # Пока что без учета экипажа.

    # Условия без учета экипажа
    if current_level > 150 + crew_sum_health:
        return "🟢"
    if 75 + crew_sum_health <= current_level <= 150 + crew_sum_health:
        return "🟡"
    if 30 + crew_sum_health <= current_level <= 74 + crew_sum_health:
        return "🟠"
    if current_level < 29 + crew_sum_health:
        return "🔴"

    return "🟢"


def get_computer_text(chat_id: int) -> str:
    ship: Ship = game_main.ALL_PLAYERS[chat_id]
    return (
        f"🚀 Корабль {ship.ship_name}\n\n"
        f"Состояние: {get_ship_status_emoji(ship)}\n"
        "======\n"
        f"💨 Скорость: {ship.speed}\n"
        f"⛽️ Топливо: {ship.fuel}%\n"
        f"💨 Кислород: {ship.oxygen}%"
        f"🛡 Прочность: {ship.health}%\n"
    )


@menu_router.callback_query(F.data == "menu_computer")
async def computer(callback: CallbackQuery):
    if not await callback_check_is_game_active(callback):
        return
    game_main.ALL_PLAYERS[callback.message.chat.id].screen = "computer"
    await menu_main.update_menu("computer", callback.message.chat.id, callback.message.message_id,
                                callback.message.text)
