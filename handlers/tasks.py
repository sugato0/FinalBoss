from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from datetime import date
from keyboards.inline import start_keyboard
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State,StatesGroup
from database import add_task, get_tasks

class AddTask(StatesGroup):
    waiting_title=State()

router=Router()

@router.callback_query(F.data == "add_task")
async def add_task_handler(callback: CallbackQuery,state: FSMContext):
    await callback.message.answer("Введите название задачи:")
    await state.set_state(AddTask.waiting_title)


@router.message(AddTask.waiting_title)
async def waiting_title_handler(message: Message, state: FSMContext):
    title = message.text.strip()
    if not title:
        await message.answer("Название задачи не может быть пустым.")
        return

    task_id = await add_task(title=title)

    await state.clear()
    await message.answer(f"Задача добавлена: {message.text}")

@router.callback_query(F.data=="list_tasks")
async def list_tasks_handler(callback: CallbackQuery):
    tasks = await get_tasks(task_date=date.today())
    if not tasks:
        await callback.message.answer("У вас пока нет задач на сегодня.")
        await callback.answer()
        return
    text = "Ваши задачи:\n"
    for task in tasks:
        status = "(выполнена)" if task.is_done else "(не выполнена)"
        text += f"{task.id}. {task.title} {status} \n"

    await callback.message.answer(text)
