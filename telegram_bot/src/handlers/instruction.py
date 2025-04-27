from aiogram import Router, types

instruction_router = Router()

@instruction_router.callback_query(lambda c: c.data == "instruction")
async def process_instruction(callback: types.CallbackQuery):
    """
    Обрабатывает запрос на отправку инструкции по подключению.
    """
    # Конфигурационные данные
    ss_config = "ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTphTWZfWklnS2NaODhpX1BQRFJvMWZn@147.45.68.227:1080#%F0%9F%9A%80%20Marz%20%28PREMIUM%29%20%5BShadowsocks%20-%20tcp%5D"

    # Форматируем сообщение с инструкцией
    instruction_text = (
        "🚀 <b>Инструкция по подключению:</b>\n\n"
        "1. Скачайте приложение:\n"
        "👉 <a href='https://play.google.com/store/apps/details?id=org.outline.android.client'>Outline для Android</a>\n"
        "👉 <a href='https://apps.apple.com/us/app/outline-app/id1356177741'>Outline для iOS</a>\n"
        "👉 <a href='https://outline-vpn.com/download.php?os=c_windows'>Outline для Windows</a>\n"
        "👉 <a href='https://outline-vpn.com/download.php?os=c_macos'>Outline для Mac</a>\n\n"
        "🔑 <b>Ваши параметры подключения:</b>\n"
        "Скопируйте конфигурационный код и вставьте в приложение.\n\n"
        "3. Нажмите 'Подключиться' в приложении\n\n"
        "💡 <b>Подсказка:</b>\n"
        "Нажмите на сообщение с кодом, чтобы скопировать его."
    )

    # Отправляем основное сообщение с инструкцией
    await callback.message.answer(
        instruction_text,
        parse_mode="HTML",
        disable_web_page_preview=True
    )

    # Отправляем конфигурационный код отдельным сообщением
    await callback.message.answer(
        f"📋 <b>Ваш конфигурационный код:</b>\n\n<code>{ss_config}</code>",
        parse_mode="HTML"
    )

    # Добавляем кнопку для перехода в профиль
    profile_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="👤 Перейти в профиль", callback_data="profile")]
    ])
    await callback.message.answer(
        "Если вы хотите посмотреть ваш профиль, нажмите на кнопку ниже:",
        reply_markup=profile_keyboard
    )

    await callback.answer()

@instruction_router.callback_query(lambda c: c.data == "copy_config")
async def copy_config(callback: types.CallbackQuery):
    """
    Уведомляет пользователя о том, как скопировать конфигурационный код.
    """
    await callback.answer(
        "Конфигурационный код уже отправлен в сообщении. Просто нажмите на него, чтобы скопировать!",
        show_alert=True
    )