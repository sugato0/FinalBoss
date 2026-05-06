from aiogram import Bot, Dispatcher
from asyncio import create_task, run
from configs.config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.tasks import router as tasks_router
from database import create_tables
from background import background_loop

async def main():
    await create_tables()

    bot=Bot(token=BOT_TOKEN)
    dp=Dispatcher()

    dp.include_router(start_router)
    dp.include_router(tasks_router)

    print("[LOG] бот запущен")
    create_task(background_loop())
    await dp.start_polling(bot)
run(main())
