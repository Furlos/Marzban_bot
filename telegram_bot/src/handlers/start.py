from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()

@start_router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем инлайн-клавиатуру с callback-кнопками
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Profile", callback_data="profile"),
            types.InlineKeyboardButton(text="Pay", callback_data="pay"),
            types.InlineKeyboardButton(text="Instruction", callback_data="instruction")
        ]
    ])

    await message.answer(
        "Привет! Я бот для покупки доступа к VPN!",
        reply_markup=keyboard
    )

