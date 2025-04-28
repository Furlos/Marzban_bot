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
                print(response_text)
                print(f"Status code: {response.status}")
                return "Server returned non-JSON response"




import aiohttp
import asyncio

import aiohttp
import json

import aiohttp
import json


async def get_user_by_username(username):
    url = f"http://localhost:3000/users/(user_id?username={username}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"accept": "application/json"}) as response:
                if response.status != 200:
                    return {
                        "error": f"API error: {response.status}",
                        "status": response.status
                    }

                try:
                    data = await response.json()
                    return {
                        "status": 200,
                        "data": data,
                        "error": None
                    }
                except json.JSONDecodeError:
                    return {
                        "status": 500,
                        "error": "Invalid JSON response",
                        "data": None
                    }
    except Exception as e:
        return {
            "status": 500,
            "error": str(e),
            "data": None
        }
import aiohttp
import asyncio


async def update_user(username, traffic_gb, expire_days, reset_usage):
    url = f"http://localhost:3000/users/(user_id)?username={username}"

    payload = {
        "traffic_gb": traffic_gb,
        "expire_days": expire_days,
        "reset_usage": reset_usage
    }

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "execute": "true"  # Добавляем заголовок execute как в примере curl
    }

    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=payload, headers=headers) as response:
            print(f"Request URL: {url}")
            print(f"Status code: {response.status}")

            try:
                response_data = await response.json()
                print("Response data:")
                print(response_data)
            except Exception as e:
                print(f"Could not parse JSON: {e}")
                print("Raw response:")
                print(await response.text())


# Пример использования
#asyncio.run(update_user(
    ##    username="cool123",
#    traffic_gb=10,
 #   copire_keys=30,
 #   reset_image=False
#))