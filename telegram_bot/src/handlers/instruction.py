from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from telegram_bot.src.handlers.api_requests import get_user_by_username

instruction_router = Router()

@instruction_router.callback_query(lambda c: c.data == "instruction")
async def show_instruction(callback: types.CallbackQuery):
    # Получаем данные пользователя
    user_data = await get_user_by_username(str(callback.from_user.id))
    username = user_data["username"]
    password = f"vpn{callback.from_user.id}"

    # Форматируем красивую инструкцию
    instruction = """
🎯 <b>Полная инструкция по подключению VPN</b>

1️⃣ <b>Скачайте приложение</b> для вашего устройства:
   • <a href="https://apps.apple.com/us/app/outline-app/id1356177741">iOS (iPhone/iPad)</a>
   • <a href="https://play.google.com/store/apps/details?id=org.outline.android.client">Android</a>
   • <a href="https://outline-vpn.com/download.php?os=c_windows">Windows</a>
   • <a href="https://outline-vpn.com/download.php?os=c_macos">Mac</a>

3️⃣ <b>Как подключиться:</b>
   1. Откройте приложение Outline
   2. Нажмите "Добавить сервер"
   3. Введите данные из следующего сообщения
   4. Готово! Ваш VPN активен 🚀
"""

    # Отправляем инструкцию
    await callback.message.answer(
        instruction,
        parse_mode="HTML",
        disable_web_page_preview=True
    )

    # Отправляем данные для копирования в отдельном сообщении
    credentials = f"""
🔐 <b>Ваши данные для подключения:</b>

<code>┌───────────────────────┐
│ Логин: {username:<15} │
│ Пароль: {password:<14} │
└───────────────────────┘</code>

Просто нажмите на сообщение, чтобы скопировать!
"""

    await callback.message.answer(
        credentials,
        parse_mode="HTML"
    )

    # Кнопка "Я скопировал"
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Я скопировал данные", callback_data="copied")

    await callback.message.answer(
        "Нажмите кнопку ниже после копирования:",
        reply_markup=builder.as_markup()
    )

    await callback.answer()

@instruction_router.callback_query(lambda c: c.data == "copied")
async def confirm_copy(callback: types.CallbackQuery):
    await callback.answer(
        "Отлично! Теперь вы можете подключиться к VPN",
        show_alert=True
    )
    await callback.message.delete()  # Удаляем кнопку после нажатия