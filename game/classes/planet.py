class Planet:

    def __init__(self, m_id: int, m_name: str, m_description: str, m_danger: int):
        self.id = m_id  # Id планеты
        self.name = m_name  # Название планеты
        self.description = m_description  # Описание планеты
        self.danger = m_danger  # Уровень опасности (не более 10)
