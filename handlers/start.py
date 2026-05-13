from aiogram.filters import CommandStart, StateFilter
from aiogram import F, Router
from aiogram.types import Message
from keyboards.reply import main_reply_keyboard, start_reply_keyboard
from lexicons.lexicons_ru import START_BTN_1, START_BTN_2, START_BTN_3, START_BTN_4


# Здесь собираются реакции бота на команду /start и обычный текст пользователя.

router=Router()

# Это тексты кнопок главного меню. По ним бот понимает,
# что пользователь нажал кнопку, а не написал произвольный текст.
MAIN_MENU_BUTTONS = {START_BTN_1, START_BTN_2, START_BTN_3, START_BTN_4}


@router.message(CommandStart())
async def start_handler(message: Message):
    # Когда пользователь пишет /start, бот здоровается и показывает главное меню.
    await message.answer(
        f"""👋 <b>Привет, {message.from_user.first_name}!</b>

Я помогу держать задачи под контролем и не забывать важное.

Выберите действие на клавиатуре ниже:""",
        reply_markup=main_reply_keyboard(),
        parse_mode="HTML"
    )


@router.message(StateFilter(None), ~F.text.in_(MAIN_MENU_BUTTONS))
async def any_message_handler(message: Message):
    # Если пользователь написал непонятный текст, бот предлагает открыть меню через /start.
    await message.answer(
        "Нажмите /start, чтобы открыть меню задач.",
        reply_markup=start_reply_keyboard()
    )
