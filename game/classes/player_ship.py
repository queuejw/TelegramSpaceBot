# Объект корабля игрока.
class Ship:

    # Инициализция объекта
    def __init__(self, chat_id: int, user_ship_name: str):
        self.chat_id = chat_id
        self.ship_name = user_ship_name
        self.health = 100
        self.speed = 100
        self.fuel = 100
        self.oxygen = 100
        self.screen = "main"  # Текущий экран меню. Это значение сохранять не нужно.

    # Экспортирует этот объект в виде словаря, для удобного сохранения в json.
    def export_as_dict(self) -> dict:
        ex_dict = {
            'chat_id': self.chat_id,
            'ship_name': self.ship_name,
            'health': self.health,
            'speed': self.speed,
            'fuel': self.fuel,
            'oxygen': self.oxygen
        }
        return ex_dict

    # Применяет значения из словаря.
    def import_from_dict(self, imported_ship: dict):
        try:
            self.chat_id = imported_ship['chat_id']
            self.ship_name = imported_ship['ship_name']
            self.health = imported_ship['health']
            self.speed = imported_ship['speed']
            self.fuel = imported_ship['fuel']
            self.oxygen = imported_ship['oxygen']
        except KeyError as e:
            print(f"[E] Не удалось импортировать данные из JSON. Детали: {e}")

        return self
