from aiogram.filters import CommandStart

from keyboards import reply
from aiogram import Router
from aiogram.types import Message
from lexicons.lexicons_ru import START_TEXT
router=Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(START_TEXT)