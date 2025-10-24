from core import constants


def load_token(path: str) -> str:
    if constants.DEBUG_MODE:
        print(f"Попытка загрузить токен из файла {path}")
    try:
        with open(path, 'r') as token_file:
            token = token_file.read()
            if len(token) == 0:
                print(f"Критическая ошибка: Файл {path} не содержит токен. Невозможно продолжить работу.")
                exit(1)
            if constants.DEBUG_MODE:
                print("Токен успешно загружен.")
            return token
    except FileNotFoundError:
        print(f"Критическая ошибка: Файл {path} не найден. Невозможно продолжить работу.")
        exit(1)
