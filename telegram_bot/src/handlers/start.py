from aiogram import Router, types
from aiogram.filters import Command

from telegram_bot.src.handlers.api_requests import create_user

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

    # Вызываем create_user без asyncio.run()
    await create_user(f"{message.from_user.id}", 12, 12)

    # Отправляем сообщение и сохраняем его ID
    await message.answer(
        "Привет! Я бот для покупки доступа к VPN!",
        reply_markup=keyboard
    )