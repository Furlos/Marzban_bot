import aiohttp
import asyncio
import json

async def create_user(username, expire_days, data_limit_gb):
    url = "http://localhost:3000/users/"
    payload = {
        "username": username,
        "expire_days": expire_days,
        "data_limit_gb": data_limit_gb
    }

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            # Получаем текст ответа независимо от Content-Type
            response_text = await response.text()

            try:
                # Пытаемся распарсить как JSON
                data = json.loads(response_text)
                print("Response:", data)

                # Получаем connection_file из ответа
                connection_file = data.get("connection_file")
                if connection_file:
                    print("Connection file:", connection_file)
                else:
                    print("No connection_file in response")

                # Выводим полный ответ сервера
                print("Full response text:", response_text)

            except json.JSONDecodeError:
                # Если не JSON, выводим как есть
                print("Server returned non-JSON response:")
                print(response_text)
                print(f"Status code: {response.status}")

asyncio.run(create_user("cool123", 12, 12))