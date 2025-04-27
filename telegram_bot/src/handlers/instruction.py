from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from telegram_bot.src.handlers.api_requests import get_user_by_username

instruction_router = Router()

@instruction_router.callback_query(lambda c: c.data == "instruction")
async def show_instruction(callback: types.CallbackQuery):
    try:
        # Получаем данные пользователя
        api_response = await get_user_by_username(str(callback.from_user.id))

        # Проверяем успешность запроса
        if not api_response or api_response.get("status") != 200:
            await callback.answer("❌ Не удалось получить данные подключения", show_alert=True)
            return

        data = api_response.get("data", {})

        # Используем connection_link если есть, иначе username
        connection_link = data.get("connection_link", data.get("connection_file", data.get("username", "Конфигурация недоступна")))

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

<code>{connection_link}</code>

Просто нажмите на сообщение, чтобы скопировать!
"""

        await callback.message.answer(
            credentials,
            parse_mode="HTML"
        )

    except Exception as e:
        print(f"Error in show_instruction: {e}")
        await callback.answer("⚠️ Произошла ошибка при получении инструкции", show_alert=True)

    await callback.answer()