import aiohttp
import asyncio
import json
from .config import url  # Import the URL from your config file

async def create_user(username, expire_days, data_limit_gb):
    api_url = f"{url}/users/"  # Use the URL from config
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
        async with session.post(api_url, json=payload, headers=headers) as response:
            response_text = await response.text()

            try:
                data = json.loads(response_text)
                print("Response:", data)

                connection_file = data.get("connection_file")
                if connection_file:
                    print("Connection file:", connection_file)
                else:
                    print("No connection_file in response")

                print("Full response text:", response_text)
                return data

            except json.JSONDecodeError:
                print(response_text)
                print(f"Status code: {response.status}")
                return {"error": "Server returned non-JSON response", "status": response.status}


async def get_user_by_username(username):
    api_url = f"{url}/users/(user_id?username={username}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers={"accept": "application/json"}) as response:
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


async def update_user(username, traffic_gb=None, expire_days=None, reset_usage=None):
    api_url = f"{url}/users/(user_id)?username={username}"

    # Only include parameters that are not None
    payload = {}
    if traffic_gb is not None:
        payload["traffic_gb"] = traffic_gb
    if expire_days is not None:
        payload["expire_days"] = expire_days
    if reset_usage is not None:
        payload["reset_usage"] = reset_usage

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "execute": "true"
    }

    async with aiohttp.ClientSession() as session:
        async with session.put(api_url, json=payload, headers=headers) as response:
            print(f"Request URL: {api_url}")
            print(f"Status code: {response.status}")

            try:
                response_data = await response.json()
                print("Response data:")
                print(response_data)
                return response_data
            except Exception as e:
                error_text = await response.text()
                print(f"Could not parse JSON: {e}")
                print("Raw response:")
                print(error_text)
                return {"error": str(e), "response_text": error_text}