from aiogram.filters import CommandStart
from keyboards.inline import start_keyboard
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

router=Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(f"""Здравствуйте, {message.from_user.first_name}!

Я помогу вам организовать задачи и своевременно напомню о сроках выполнения.

Доступные действия:""",reply_markup=start_keyboard())