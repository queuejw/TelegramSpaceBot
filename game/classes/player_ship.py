# Объект корабля игрока.
class Ship:

    # Инициализция объекта
    def __init__(self, chat_id: int, user_ship_name: str):
        self.chat_id = chat_id
        self.ship_name = user_ship_name
        self.health = 100
        self.fuel = 100
        self.oxygen = 100

    # Экспортирует этот объект в виде словаря, для удобного сохранения в json.
    def export_as_dict(self) -> dict:
        ex_dict = {
            'chat_id': self.chat_id,
            'ship_name' : self.ship_name,
            'health': self.health,
            'fuel': self.fuel,
            'oxygen': self.oxygen
        }
        return ex_dict

    # Применяет значения из словаря.
    def import_from_dict(self, imported_ship: dict):
        self.chat_id = imported_ship['chat_id']
        self.ship_name = imported_ship['ship_name']
        self.health = imported_ship['health']
        self.fuel = imported_ship['fuel']
        self.oxygen = imported_ship['oxygen']
