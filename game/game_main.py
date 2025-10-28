ALL_PLAYERS = {}  # Словарь активных кораблей игроков; chat id - объект ship

from core.manager import planet_manager
PLANETS = planet_manager.load_planets() # Список планет

# Вернет True, если игра в чате chat_id активна.
def is_game_active(chat_id: int) -> bool:
    return ALL_PLAYERS.__contains__(chat_id)


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
