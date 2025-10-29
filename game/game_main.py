import random

from core.constants import ALLOWED_USERS
from game.classes.planet import Planet

ALL_PLAYERS = {}  # Словарь активных кораблей игроков; chat id - объект ship

from core.manager import planet_manager

PLANETS = planet_manager.load_planets()  # Список планет

# Возвращает планету по её ID
def get_planet_by_id(m_id: int) -> Planet:
    l = [x for x in PLANETS if x.id == m_id]
    if len(l) < 1:
        return random.choice(PLANETS)
    return l[0]

# Вернет True, если игра в чате chat_id активна.
def is_game_active(chat_id: int) -> bool:
    return ALL_PLAYERS.__contains__(chat_id)


def user_allowed(user_id: int) -> bool:
    if len(ALLOWED_USERS) == 0:
        return True
    return user_id in ALLOWED_USERS


# Возвращает значение в пределах от минимума до максимума
def clamp(min_value, max_value, value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


# Удалит чат chat_id из словаря, завершив игру и вернув True.
def stop_game(chat_id: int) -> bool:
    if is_game_active(chat_id):
        ALL_PLAYERS.pop(chat_id)
        return True
    else:
        return False
