from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicons.lexicons_ru import START_BTN_1, START_BTN_2, START_BTN_3, START_BTN_4


def start_reply_keyboard():
    # Клавиатура с одной кнопкой /start для пользователя, который еще не открыл меню.
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start")]
        ],
        resize_keyboard=True
    )


def main_reply_keyboard():
    # Главное меню внизу Telegram: добавить, посмотреть, удалить или изменить задачу.
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=START_BTN_1), KeyboardButton(text=START_BTN_2)],
            [KeyboardButton(text=START_BTN_3), KeyboardButton(text=START_BTN_4)]
        ],
        resize_keyboard=True
    )
