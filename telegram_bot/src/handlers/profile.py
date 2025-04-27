from aiogram import Router, types
from aiogram.filters import Command

profile_router = Router()
# Обработчики для callback-кнопок
@profile_router.callback_query(lambda c: c.data == "profile")
async def process_profile(callback: types.CallbackQuery):
    await callback.message.answer("Вы выбрали Profile")
