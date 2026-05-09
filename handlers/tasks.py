from aiogram.fsm.context import FSMContext
from datetime import date
from keyboards.inline import delete_task_keyboard, toggle_task_keyboard
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State,StatesGroup
from database import add_task, get_tasks, delete_task, update_task
from lexicons.lexicons_ru import START_BTN_1, START_BTN_2, START_BTN_3, START_BTN_4

class AddTask(StatesGroup):
    waiting_title=State()

router=Router()
MAIN_MENU_BUTTONS = {START_BTN_1, START_BTN_2, START_BTN_3, START_BTN_4}

async def show_add_task_prompt(message: Message, state: FSMContext):
    await message.answer(
        "➕ <b>Новая задача</b>\n\nВведите название задачи:",
        parse_mode="HTML"
    )
    await state.set_state(AddTask.waiting_title)

async def show_tasks_list(message: Message):
    tasks = await get_tasks(task_date=date.today())
    if not tasks:
        await message.answer("📭 На сегодня задач пока нет.")
        return

    text = "📋 <b>Задачи на сегодня</b>\n\n"
    for number, task in enumerate(tasks, start=1):
        status = "✅" if task.is_done else "⬜"
        text += f"{number}. {status} {task.title}\n"

    await message.answer(text, parse_mode="HTML")

async def show_delete_task_menu(message: Message):
    tasks = await get_tasks(task_date=date.today())

    if not tasks:
        await message.answer("📭 На сегодня задач пока нет.")
        return

    await message.answer(
        "🗑 <b>Удаление задачи</b>\n\nВыберите задачу, которую нужно удалить:",
        reply_markup=delete_task_keyboard(tasks),
        parse_mode="HTML"
    )

async def show_toggle_task_menu(message: Message):
    tasks = await get_tasks(task_date=date.today())

    if not tasks:
        await message.answer("📭 На сегодня задач пока нет.")
        return

    await message.answer(
        "✅ <b>Статус задачи</b>\n\nВыберите задачу, чтобы изменить статус:",
        reply_markup=toggle_task_keyboard(tasks),
        parse_mode="HTML"
    )

@router.message(F.text == START_BTN_1)
async def add_task_message_handler(message: Message, state: FSMContext):
    await show_add_task_prompt(message, state)

@router.callback_query(F.data == "add_task")
async def add_task_handler(callback: CallbackQuery,state: FSMContext):
    await show_add_task_prompt(callback.message, state)
    await callback.answer()


@router.message(AddTask.waiting_title)
async def waiting_title_handler(message: Message, state: FSMContext):
    title = message.text.strip()

    if title in MAIN_MENU_BUTTONS:
        await state.clear()
        await message.answer("Добавление задачи отменено. Выберите действие на клавиатуре.")
        return

    if not title:
        await message.answer("⚠️ Название задачи не может быть пустым.")
        return

    task_id = await add_task(title=title)

    await state.clear()
    await message.answer(
        f"✅ <b>Задача добавлена</b>\n\n{title}",
        parse_mode="HTML"
    )

@router.message(F.text == START_BTN_2)
async def list_tasks_message_handler(message: Message):
    await show_tasks_list(message)

@router.callback_query(F.data=="list_tasks")
async def list_tasks_handler(callback: CallbackQuery):
    await show_tasks_list(callback.message)
    await callback.answer()

@router.message(F.text == START_BTN_3)
async def delete_task_message_handler(message: Message):
    await show_delete_task_menu(message)

@router.callback_query(F.data=="delete_task")
async def delete_task_handler(callback: CallbackQuery):
    await show_delete_task_menu(callback.message)
    await callback.answer()

@router.callback_query(F.data.startswith("delete_task:"))
async def confirm_delete_task_handler(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])

    is_deleted = await delete_task(task_id)

    if not is_deleted:
        await callback.answer("Задача не найдена.", show_alert=True)
        return

    tasks = await get_tasks(task_date=date.today())

    if tasks:
        await callback.message.edit_text(
            "🗑 <b>Удаление задачи</b>\n\nВыберите задачу, которую нужно удалить:",
            reply_markup=delete_task_keyboard(tasks),
            parse_mode="HTML"
        )
    else:
        await callback.message.edit_text("📭 Задач больше нет.")

    await callback.answer("Задача удалена.")

@router.message(F.text == START_BTN_4)
async def toggle_task_message_handler(message: Message):
    await show_toggle_task_menu(message)

@router.callback_query(F.data == "toggle_task")
async def toggle_task_handler(callback: CallbackQuery):
    await show_toggle_task_menu(callback.message)
    await callback.answer()

@router.callback_query(F.data.startswith("toggle_task:"))
async def confirm_toggle_task_handler(callback: CallbackQuery):
    _, task_id, current_status = callback.data.split(":")

    task_id = int(task_id)
    current_status = bool(int(current_status))

    new_status = not current_status

    is_updated = await update_task(task_id=task_id, is_done=new_status)

    if not is_updated:
        await callback.answer("Задача не найдена.", show_alert=True)
        return

    tasks = await get_tasks(task_date=date.today())

    await callback.message.edit_text(
        "✅ <b>Статус задачи</b>\n\nВыберите задачу, чтобы изменить статус:",
        reply_markup=toggle_task_keyboard(tasks),
        parse_mode="HTML"
    )

    text = "Задача выполнена." if new_status else "Задача снова не выполнена."
    await callback.answer(text)
