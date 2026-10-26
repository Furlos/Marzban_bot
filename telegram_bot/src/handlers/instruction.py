"""Deliver a user's connection instructions privately and safely."""
from html import escape

from aiogram import Router, types
from .api_requests import get_user_by_username

instruction_router = Router()


@instruction_router.callback_query(lambda c: c.data == "instruction")
async def show_instruction(callback: types.CallbackQuery):
    response = await get_user_by_username(str(callback.from_user.id))
    if response.get("status") != 200:
        await callback.answer("Не удалось получить настройки подключения.", show_alert=True)
        return

    data = response.get("data") or {}
    connection_link = data.get("connection_link")
    if not connection_link:
        await callback.answer("Настройки подключения пока недоступны.", show_alert=True)
        return

    instructions = (
        "Настройка Outline:\n"
        "1. Установите клиент с официального сайта проекта.\n"
        "2. Нажмите «Добавить сервер».\n"
        "3. Вставьте ключ из следующего сообщения."
    )
    await callback.message.answer(instructions)
    # Escaping is essential: an external connection string must not inject HTML.
    await callback.message.answer(
        f"🔐 <b>Ваш ключ подключения:</b>\n<code>{escape(str(connection_link))}</code>",
        parse_mode="HTML",
    )
    await callback.answer()
