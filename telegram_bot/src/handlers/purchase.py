from aiogram import Router, types
from aiogram.filters import Command

purchase_router = Router()

@purchase_router.callback_query(lambda c: c.data == "pay")
async def process_pay(callback: types.CallbackQuery):
    # Создаем клавиатуру с вариантами подписки
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="1 месяц - 1$", callback_data="sub_1"),
            types.InlineKeyboardButton(text="3 месяца - 2$", callback_data="sub_3")
        ],
        [
            types.InlineKeyboardButton(text="6 месяцев - 3$", callback_data="sub_6"),
            types.InlineKeyboardButton(text="12 месяцев - 4$", callback_data="sub_12")
        ]
    ])

    await callback.message.answer(
        "Вы можете оплатить VPN. Выберите один из вариантов подписки:",
        reply_markup=keyboard
    )

    # Подтверждаем обработку callback, чтобы убрать "часики" у кнопки
    await callback.answer()

# Обработчики для выбора подписки
@purchase_router.callback_query(lambda c: c.data.startswith("sub_"))
async def process_subscription(callback: types.CallbackQuery):
    months = callback.data.split("_")[1]  # Получаем количество месяцев из callback_data
    prices = {"1": "1$", "3": "2$", "6": "3$", "12": "4$"}

    await callback.message.answer(
        f"Вы выбрали подписку на {months} месяц(ев) за {prices[months]}. "
        "Теперь вам нужно произвести оплату."
    )

    # Здесь можно добавить логику для обработки оплаты
    # Например, отправить счет или перенаправить на платежный шлюз

    await callback.answer()