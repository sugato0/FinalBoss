from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.inline import start_keyboard
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State,StatesGroup


class AddTask(StatesGroup):
    waiting_title=State()

router=Router()

@router.callback_query(F.data == "add_task")
async def add_task_handler(callback: CallbackQuery,state: FSMContext):
    await callback.message.answer("Введите название задачи:")
    await state.set_state(AddTask.waiting_title)


@router.message(AddTask.waiting_title)
async def waiting_title_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Задача добавлена: {message.text}")