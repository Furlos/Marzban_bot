from aiogram import Router, types
from aiogram.filters import Command
from src.utils.clear_chat import save_message  # Исправленный импорт

start_router = Router()

@start_router.message(Command("start"))
async def cmd_start(message: types.Message):
    bot = message.bot
    chat_id = message.chat.id

    # Создаем инлайн-клавиатуру с callback-кнопками
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Profile", callback_data="profile"),
            types.InlineKeyboardButton(text="Pay", callback_data="pay"),
            types.InlineKeyboardButton(text="Instruction", callback_data="instruction")
        ]
    ])

    # Отправляем сообщение и сохраняем его ID
    sent_message = await message.answer(
        "Привет! Я бот для покупки доступа к VPN!",
        reply_markup=keyboard
    )
    await save_message(chat_id=chat_id, message_id=sent_message.message_id)