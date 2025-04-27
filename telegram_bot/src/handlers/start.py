from aiogram import Router, types
from aiogram.filters import Command
import aiohttp
import asyncio
from  config.config import url

# Создаем роутер
start_router = Router()

@start_router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    headers = {"Content-Type": "application/json"}
    payload = {
        "username": f"tg-{message.from_user.id}",
        "expire_days": 7,
        "data_limit_gb": 100
    }
    async def create_user(url, headers,payload):
        async with aiohttp.ClientSession() as session:  # Используем контекстный менеджер
            async with session.post(url, headers=headers, json=payload) as response:
                return await response.json()

    await message.answer(
        f"Привет! Я бот для покупки доступа к VPN! Ваш  ник - {asyncio.run(create_user(url, headers, payload))}"
    )