import aiohttp
import asyncio

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