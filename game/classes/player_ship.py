# Объект корабля игрока.
class Ship:

    # Инициализция объекта
    def __init__(self, chat_id: int, user_ship_name: str):
        self.chat_id = chat_id  # Id чата, к которому корабль привязан
        self.ship_name = user_ship_name  # Название корабля
        self.health = 100  # Прочность корабля 0 - 100
        self.speed = 100  # Скорость корабля
        self.fuel = 100  # Уровень топлива 0 - 100
        self.oxygen = 100  # Уровень кислорода 0 - 100
        self.on_planet = False  # Корабль находится на планете?
        self.planet_id = -1 # ID планеты, на которой находится корабль. Если -1, значит корабль не находится на планете (см. выше)
        self.actions_blocked = False  # Действия игроков заблокированы?
        self.screen = "main"  # Текущий экран меню. Это значение сохранять не нужно.

    # Экспортирует этот объект в виде словаря, для удобного сохранения в json.
    def export_as_dict(self) -> dict:
        ex_dict = {
            'chat_id': self.chat_id,
            'ship_name': self.ship_name,
            'health': self.health,
            'speed': self.speed,
            'fuel': self.fuel,
            'oxygen': self.oxygen,
            'on_planet': self.on_planet,
            'actions_blocked': self.actions_blocked
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
            self.on_planet = imported_ship['on_planet']
            self.actions_blocked = imported_ship['actions_blocked']
        except KeyError as e:
            print(f"[E] Не удалось импортировать какие-то данные из JSON. Возможно, файл устарел. Детали: {e}")

        return self
