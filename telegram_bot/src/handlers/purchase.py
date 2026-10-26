from aiogram import types, F, Router

from aiogram.types import LabeledPrice, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


from .api_requests import update_user


purchase_router = Router()

# Конфигурация подписок
SUBSCRIPTIONS = {
    "1": {"months": 1, "price": 150, "label": "1 месяц - 150⭐"},  # цена в звездах
    "3": {"months": 3, "price": 350, "label": "3 месяца - 350⭐"},
    "6": {"months": 6, "price": 750, "label": "6 месяцев - 750⭐"},
    "12": {"months": 12, "price": 1000, "label": "12 месяцев - 1000⭐"}
}

def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Оплатить", pay=True)
    return builder.as_markup()

def get_subscription_keyboard():
    builder = InlineKeyboardBuilder()
    for sub_id, sub_data in SUBSCRIPTIONS.items():
        builder.button(text=sub_data["label"], callback_data=f"sub_{sub_id}")
    builder.adjust(2)
    return builder.as_markup()


@purchase_router.callback_query(F.data == "pay")
async def show_subscriptions(callback: types.CallbackQuery):
    await callback.message.answer(
        "Выберите вариант подписки:",
        reply_markup=get_subscription_keyboard()
    )
    await callback.answer()

@purchase_router.callback_query(F.data.startswith("sub_"))
async def process_subscription(callback: types.CallbackQuery):
    sub_id = callback.data.split("_")[1]
    sub_data = SUBSCRIPTIONS.get(sub_id)

    if not sub_data:
        await callback.answer("Неверный вариант")
        return

    try:
        await callback.message.answer_invoice(
            title=f"VPN подписка {sub_data['months']} мес",
            description=f"Доступ на {sub_data['months']} месяцев",
            payload=f"sub_{sub_id}_{callback.from_user.id}",
            provider_token="",  # Замените на реальный токен
            currency="XTR",
            prices=[LabeledPrice(label="Stars", amount=sub_data["price"])],
            reply_markup=payment_keyboard()
        )
    except Exception as e:
        await callback.message.answer("Ошибка платежа")
        print(f"Error: {e}")

    await callback.answer()

@purchase_router.pre_checkout_query()
async def pre_checkout(pre_checkout_q: PreCheckoutQuery):
    payload = pre_checkout_q.invoice_payload.split("_", 2)
    is_valid = (
        len(payload) == 3
        and payload[0] == "sub"
        and payload[1] in SUBSCRIPTIONS
        and payload[2] == str(pre_checkout_q.from_user.id)
        and pre_checkout_q.currency == "XTR"
        and pre_checkout_q.total_amount == SUBSCRIPTIONS[payload[1]]["price"]
    )
    await pre_checkout_q.answer(ok=is_valid, error_message=None if is_valid else "Некорректная подписка")


@purchase_router.message(F.successful_payment)
async def success_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload
    if not payload.startswith("sub_"):
        return

    _, sub_id, user_id = payload.split("_", 2)
    sub_data = SUBSCRIPTIONS.get(sub_id)

    if not sub_data or user_id != str(message.from_user.id):
        return

    # Создаем клавиатуру с кнопкой инструкции
    builder = InlineKeyboardBuilder()
    builder.button(text="📚 Инструкция", callback_data="instruction")
    days = sub_data["months"]*30
    activation = await update_user(f"{message.from_user.id}", 100, days)
    if activation.get("status") != 200:
        await message.answer(
            "Оплата прошла, но автоматическая активация не удалась. "
            "Обратитесь к администратору с подтверждением оплаты."
        )
        return
    await message.answer(
        f"✅ Оплачено {sub_data['months']} мес!\n"
        "Нажмите кнопку ниже для получения инструкции:",
        reply_markup=builder.as_markup()
    )