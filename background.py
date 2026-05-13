from asyncio import sleep


async def background_loop():
    # Отдельный бесконечный цикл для действий, которые должны выполняться сами.
    # Сейчас он просто ждет по минуте, но позже сюда можно добавить напоминания.
    while True:
        await sleep(60)
