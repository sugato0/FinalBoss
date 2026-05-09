from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lexicons.lexicons_ru import START_BTN_1, START_BTN_2, START_BTN_3, START_BTN_4

def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=START_BTN_1, callback_data="add_task")],
        [InlineKeyboardButton(text=START_BTN_2, callback_data="list_tasks")],
        [InlineKeyboardButton(text=START_BTN_3, callback_data="delete_task")],
        [InlineKeyboardButton(text=START_BTN_4, callback_data="toggle_task")]
    ])

def delete_task_keyboard(tasks):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🗑 {task.title}", callback_data=f"delete_task:{task.id}")]
            for task in tasks
        ]
    )

def toggle_task_keyboard(tasks):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{'✅' if task.is_done else '⬜'} {task.title}",
                    callback_data=f"toggle_task:{task.id}:{int(task.is_done)}"
                )
            ]
            for task in tasks
        ]
    )
