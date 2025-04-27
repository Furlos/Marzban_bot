from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.formatting import (
    Bold, TextLink, as_list, as_marked_section
)

instruction_router = Router()

@instruction_router.callback_query(lambda c: c.data == "instruction")
async def process_instruction(callback: types.CallbackQuery):
    # Конфигурационные данные
    ss_config = "ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTphTWZfWklnS2NaODhpX1BQRFJvMWZn@147.45.68.227:1080#%F0%9F%9A%80%20Marz%20%28PREMIUM%29%20%5BShadowsocks%20-%20tcp%5D"

    # Форматируем сообщение с интерактивными ссылками
    message = as_list(
        as_marked_section(
            Bold("🚀 Инструкция по подключению:"),
            "1. Скачайте приложение:",
            TextLink("Outline для Android", url="https://play.google.com/store/apps/details?id=org.outline.android.client"),
            TextLink("Outline для iOS", url="https://apps.apple.com/us/app/outline-app/id1356177741"),
            TextLink("Outline для Windows", url="https://outline-vpn.com/download.php?os=c_windows"),
            TextLink("Outline для Mac", url="https://outline-vpn.com/download.php?os=c_macos"),
            marker="👉 "
        ),
        "\n",
        as_marked_section(
            Bold("🔑 Ваши параметры подключения:"),
            "Скопируйте конфигурационный код и вставьте в приложение",
            marker="• "
        ),
        f"\n",
        "3. Нажмите 'Подключиться' в приложении",
        "\n",
        Bold("💡 Подсказка: "),
        "Нажмите на сообщение с кодом, чтобы скопировать его",
    )

    # Отправляем основное сообщение
    await callback.message.answer(
        **message.as_kwargs(),
        disable_web_page_preview=True
    )

    # Отправляем конфиг отдельным сообщением для удобного копирования
    await callback.message.answer(
        f"📋 Ваш конфигурационный код:\n\n<code>{ss_config}</code>",
        parse_mode="HTML"
    )

    await callback.answer()

@instruction_router.callback_query(lambda c: c.data == "copy_config")
async def copy_config(callback: types.CallbackQuery):
    await callback.answer(
        "Конфигурационный код уже отправлен в сообщении. Просто нажмите на него, чтобы скопировать!",
        show_alert=True
    )