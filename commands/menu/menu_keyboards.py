from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Возвращает клавиатуру с кнопкой назад в меню Об игре
def get_info_back_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="info_callback_exit"
        )
    )
    return builder


# Возвращает клавиатуру с кнопками в основном меню.
def get_main_info_commands_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Играть 🚀",
            callback_data="play_callback"
        ),
        InlineKeyboardButton(
            text="Помощь ❓",
            callback_data="help_callback"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Об игре ⚙️",
            callback_data="info_callback"
        )
    )
    return builder


# Возвращает клавиатуру с кнопкой назад (возврат в главное меню).
def get_back_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="menu_back"
        ),
        InlineKeyboardButton(
            text="🔄 Обновить",
            callback_data="menu_update_screen"
        )
    )
    return builder


# Возвращает клавиатуру с кнопкой создать игру. Используется, если игрок вводит команду меню, но при этом игра не активна.
def get_create_game_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🚀 Начать игру",
            callback_data="menu_start_game"
        )
    )
    return builder


# Возвращает клавиатуру главного меню.
def get_game_main_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🖥 Компьютер",
            callback_data="menu_computer"
        ),
        InlineKeyboardButton(
            text="🗺 Навигация",
            callback_data="navigation_menu"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="⚓️ Главный отсек",
            callback_data="menu_captain"
        )
    )
    return builder


# Возвращает клавиатуру с кнопками навигации по планетам.
def get_menu_navigation_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="back_action_navigation_menu"
        ),
        InlineKeyboardButton(
            text="✅ Лететь!",
            callback_data="accept_action_navigation_menu"
        ),
        InlineKeyboardButton(
            text="▶️ Дальше",
            callback_data="next_action_navigation_menu"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="❌ Отмена",
            callback_data="menu_back"
        )
    )
    return builder


# Возвращает клавиатуру с кнопками навигации в случае, если игрок уже находится на планете.
def get_on_planet_menu_navigation_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🚀 Покинуть планету",
            callback_data="leave_planet_action_navigation_menu"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="menu_back"
        )
    )
    return builder
