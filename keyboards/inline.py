from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lexicons.lexicons_ru import START_BTN_1,START_BTN_2,START_BTN_3

def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=START_BTN_1, callback_data="add_task")],
        [InlineKeyboardButton(text=START_BTN_2, callback_data="list_tasks")],
        [InlineKeyboardButton(text=START_BTN_3, callback_data="delete_task")]])
