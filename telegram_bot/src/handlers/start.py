from aiogram import Router, types
from aiogram.filters import Command

from telegram_bot.src.handlers.api_requests import create_user, get_user_by_username

start_router = Router()

@start_router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем инлайн-клавиатуру с callback-кнопками
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="👤Профиль", callback_data="profile"),
            types.InlineKeyboardButton(text="💰 Купить", callback_data="pay"),
            types.InlineKeyboardButton(text="📚 Инструкция", callback_data="instruction")
        ]
    ])
    if   await create_user(f"{message.from_user.id}", 7, 12)  != "Server returned non-JSON response":
        # Вызываем create_user без asyncio.run()

        await message.answer(
            "╔═══════════════════════╗\n   🚀 *ПРИВЕТ, ПУТЕШЕСТВЕННИК!* \n               🌐 *Instant-Paris VPN *\n      ⚡ *Пробный период активен!*  \n          📜 Перейдите в инструкцию  \n╚═══════════════════════╝  ",
            reply_markup=keyboard
        )
    # Отправляем сообщение и сохраняем его ID
    else:
        await message.answer(
        "╔═══════════════════════╗ \n   🚀 *ПРИВЕТ, ПУТЕШЕСТВЕННИК!*\n          ТВОЙ VPN — ТВОЯ СВОБОДА!\n ╚═══════════════════════╝  ",
        reply_markup=keyboard
    )