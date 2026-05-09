from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicons.lexicons_ru import START_BTN_1, START_BTN_2, START_BTN_3, START_BTN_4

def start_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start")]
        ],
        resize_keyboard=True
    )

def main_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=START_BTN_1), KeyboardButton(text=START_BTN_2)],
            [KeyboardButton(text=START_BTN_3), KeyboardButton(text=START_BTN_4)]
        ],
        resize_keyboard=True
    )
