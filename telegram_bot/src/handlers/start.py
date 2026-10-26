"""Welcome flow: do not recreate an existing subscription on each /start."""
from aiogram import Router, types
from aiogram.filters import Command

from .api_requests import create_user, get_user_by_username

start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton(text="💰 Купить", callback_data="pay"),
        types.InlineKeyboardButton(text="📚 Инструкция", callback_data="instruction"),
    ]])
    username = str(message.from_user.id)
    lookup = await get_user_by_username(username)
    if lookup["status"] == 200:
        text = "С возвращением! Выберите действие:"
    elif lookup["status"] == 404:
        created = await create_user(username, 7, 12)
        if created["status"] not in (200, 201):
            await message.answer("Сервис временно недоступен. Попробуйте позже.")
            return
        text = "Добро пожаловать! Пробный период активирован. Инструкция в меню."
    else:
        await message.answer("Сервис временно недоступен. Попробуйте позже.")
        return
    await message.answer(text, reply_markup=keyboard)
