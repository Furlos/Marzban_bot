from aiogram import Router
import aiohttp
import asyncio
from config.config import url
# Создаем роутер
start_router = Router()

@start_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для покупки доступа к VPN!"
    )
    user_id = message.from_user.id
    

async def create_user():
    url = "http://localhost:3000/users/"
    headers = {"Content-Type": "application/json"}
    payload = {
        "username": "test_user123456",
        "expire_days": 30,
        "data_limit_gb": 10
    }

    async with aiohttp.ClientSession() as session:  # Используем контекстный менеджер
        async with session.post(url, headers=headers, json=payload) as response:
            data = await response.json()
            print("Пользователь создан:", data)

asyncio.run(create_user())