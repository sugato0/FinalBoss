from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lexicons.lexicons_ru import START_BTN_1, START_BTN_2, START_BTN_3, START_BTN_4


def start_keyboard():
    # Кнопки внутри сообщения с основными действиями.
    # Сейчас чаще используется нижняя клавиатура, но этот вариант тоже готов.
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=START_BTN_1, callback_data="add_task")],
        [InlineKeyboardButton(text=START_BTN_2, callback_data="list_tasks")],
        [InlineKeyboardButton(text=START_BTN_3, callback_data="delete_task")],
        [InlineKeyboardButton(text=START_BTN_4, callback_data="toggle_task")]
    ])


def delete_task_keyboard(tasks):
    # Для каждой задачи создаем отдельную кнопку удаления.
    # Внутри кнопки хранится номер задачи, чтобы бот понял, что именно удалять.
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🗑 {task.title}", callback_data=f"delete_task:{task.id}")]
            for task in tasks
        ]
    )


def toggle_task_keyboard(tasks):
    # Для каждой задачи создаем кнопку смены статуса.
    # Внутри кнопки хранится номер задачи и информация, выполнена она сейчас или нет.
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
