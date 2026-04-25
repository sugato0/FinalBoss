from aiogram import Bot, Dispatcher
from asyncio import run
from configs.config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.tasks import router as tasks_router

async def main():
    bot=Bot(token=BOT_TOKEN)
    dp=Dispatcher()

    dp.include_router(start_router)
    dp.include_router(tasks_router)

    print("[LOG] бот запущен")
    await dp.start_polling(bot)
run(main())

