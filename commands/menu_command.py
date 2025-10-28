from aiogram import Router

from commands.menu import captain_menu, computer_menu, menu_main, navigation_menu, start_game_menu

# Команды меню были раздроблены и перенесены в директорию menu для дальнейшего улучшения работы бота.
router = Router(name="menu_command_router")

menu_routers = [captain_menu.menu_router, computer_menu.menu_router, menu_main.menu_router, navigation_menu.menu_router,
                start_game_menu.menu_router]

for r in menu_routers:
    router.include_router(r)
