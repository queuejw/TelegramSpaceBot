# Инициализация бота
async def start_bot():
    from core.bot_core import BOT
    from aiogram import Dispatcher

    dp = Dispatcher()

    from core.routers import ROUTERS
    dp.include_router(ROUTERS)

    await BOT.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(BOT)


# Здесь происходит запуск программы.
if __name__ == "__main__":
    import sys
    import logging
    import asyncio

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("Завершение работы.")
