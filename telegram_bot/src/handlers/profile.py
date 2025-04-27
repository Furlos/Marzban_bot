from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime, timedelta

profile_router = Router()

async def generate_profile_message(user: types.User):
    """
    Генерирует текст и клавиатуру для профиля пользователя.
    """
    user_id = user.id
    username = user.username or "не указан"

    # Заглушки данных (в реальном боте нужно получать из БД)
    traffic_used = 3.2  # GB
    traffic_limit = 10  # GB
    traffic_left = traffic_limit - traffic_used
    subscription_end = datetime.now() + timedelta(days=7)  # +7 дней от текущей даты

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
        f"{subscription_end.strftime('%d.%m.%Y %H:%M')}"
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