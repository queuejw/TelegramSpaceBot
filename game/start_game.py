from core import constants
from core.command_utils import bot_edit_message
from core.manager import save_manager
from game import game_main


def get_menu_tip() -> str:
    return f"\n\nИспользуйте команду /menu{constants.BOT_USERNAME} , чтобы открыть меню управления кораблём."


# Запускает игру
async def start_new_game(chat_id: int, menu_message_id: int):
    player_dict = save_manager.load_ship_state(chat_id)  # Загрузка сохранения, либо создание нового.
    game_main.ALL_PLAYERS[chat_id] = player_dict['ship']  # Добавляем в список игроков загруженный корабль
    if player_dict['default']:
        text = (
                "🚀 Игра началась!" + get_menu_tip()
        )
        await bot_edit_message(chat_id, menu_message_id, text)
    else:
        text = (
                "🚀 Продолжаем игру!" + get_menu_tip()
        )
        await bot_edit_message(chat_id, menu_message_id, text)
