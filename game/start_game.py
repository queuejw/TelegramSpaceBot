from core.manager import save_manager

def start_new_game(chat_id: int):
    ship = save_manager.load_ship_state(chat_id)