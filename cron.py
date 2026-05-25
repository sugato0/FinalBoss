from database import get_tasks
from datetime import date
from aiogram import Bot
from datetime import datetime
from lexicons.lexicons_ru import notification
from asyncio import sleep
async def sender(bot: Bot):
    
    
    while True:
        now = datetime.now()
        tasks = await get_tasks(task_date=date.today())
        if now.hour == 9 and now.minute == 0:
            for task in tasks:
                print(task.user_id, task.title)
                await bot.send_message(
                    chat_id = task.user_id, 
                    text = await notification(task.title)
                )
        await sleep(61)