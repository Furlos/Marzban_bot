from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime
from telegram_bot.src.handlers.api_requests import get_user_by_username

profile_router = Router()


async def generate_profile_message(user: types.User):
    """
    Генерирует текст и клавиатуру для профиля пользователя.
    """
    user_id = user.id
    username = user.username or "не указан"

    # Получаем данные от API
    api_response = await get_user_by_username(str(user_id))

    # Проверяем успешность запроса
    if not api_response or api_response.get("status") != 200:
        error_msg = api_response.get("error", "Unknown error") if api_response else "No response"
        return f"❌ Ошибка получения данных: {error_msg}", None

    data = api_response.get("data", {})

    # Проверяем наличие обязательных полей
    required_fields = ["used_traffic_gb", "data_limit_gb", "expire_date"]
    if not all(field in data for field in required_fields):
        return "❌ В данных профиля отсутствуют необходимые поля", None

    try:
        # Получаем и преобразуем данные
        traffic_used = float(data["used_traffic_gb"])
        traffic_limit = float(data["data_limit_gb"])
        traffic_left = traffic_limit - traffic_used

        # Преобразуем строку даты в объект datetime
        expire_date = datetime.strptime(data["expire_date"], "%Y-%m-%d")

        # Форматируем сообщение
        profile_text = (
            f"👤 <b>Ваш профиль</b>\n\n"
            f"🆔 ID: <code>{user_id}</code>\n"
            f"📛 Username: @{username}\n\n"
            f"📊 <b>Трафик:</b>\n"
            f"• Использовано: {traffic_used:.1f} GB\n"
            f"• Лимит: {traffic_limit} GB\n"
            f"• Осталось: {traffic_left:.1f} GB\n\n"
            f"⏳ <b>Подписка активна до:</b>\n"
            f"{expire_date.strftime('%d.%m.%Y')}"
        )

        # Создаем клавиатуру
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_profile"),
                types.InlineKeyboardButton(text="💰 Купить подписку", callback_data="pay")
            ],
            [
                types.InlineKeyboardButton(text="📖 Инструкция", callback_data="instruction")
            ]
        ])

        return profile_text, keyboard

    except (ValueError, KeyError) as e:
        print(f"Error processing profile data: {e}")
        return "❌ Ошибка обработки данных профиля", None


# ... остальные обработчики остаются без изменений ...

@profile_router.callback_query(lambda c: c.data == "profile")
async def process_profile(callback: types.CallbackQuery):
    """
    Обрабатывает запрос на просмотр профиля пользователя.
    """
    profile_text, keyboard = await generate_profile_message(callback.from_user)
    await callback.message.answer(
        profile_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()

@profile_router.callback_query(lambda c: c.data == "refresh_profile")
async def refresh_profile(callback: types.CallbackQuery):
    """
    Обновляет данные профиля пользователя.
    """
    profile_text, keyboard = await generate_profile_message(callback.from_user)
    await callback.message.answer(
        profile_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer("Данные обновлены! ✅", show_alert=False)

@profile_router.message(Command("start"))  # Исправлено: используется фильтр Command
async def process_start(message: types.Message):
    """
    Обрабатывает команду /start и отправляет приветственное сообщение.
    """
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Перейти в профиль", callback_data="profile")]
    ])
    await message.answer(
        "Добро пожаловать! Нажмите кнопку ниже, чтобы перейти в свой профиль.",
        reply_markup=keyboard
    )