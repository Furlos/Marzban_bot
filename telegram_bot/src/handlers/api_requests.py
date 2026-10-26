"""Calls to the internal backend. Never log subscription credentials."""
import asyncio

import aiohttp
from config import internal_api_key, url


async def _request(method: str, path: str, payload: dict | None = None) -> dict:
    if not internal_api_key:
        return {"status": 503, "error": "Internal API key not configured", "data": None}

    try:
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.request(
                method,
                f"{url}{path}",
                json=payload,
                headers={"X-Internal-Token": internal_api_key},
            ) as response:
                if response.content_type == "application/json":
                    result = await response.json()
                else:
                    result = None
                if response.status >= 400:
                    return {
                        "status": response.status,
                        "error": f"Backend returned HTTP {response.status}",
                        "data": None,
                    }
                if not isinstance(result, dict):
                    return {"status": 502, "error": "Unexpected backend response", "data": None}
                return {"status": response.status, "error": None, "data": result}
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return {"status": 503, "error": "Backend unavailable", "data": None}


async def create_user(username, expire_days, data_limit_gb):
    return await _request(
        "POST",
        "/users/",
        {"username": str(username), "expire_days": expire_days, "data_limit_gb": data_limit_gb},
    )


async def get_user_by_username(username):
    return await _request("GET", f"/users/{username}")


async def update_user(username, traffic_gb=None, expire_days=None, reset_usage=None):
    payload = {}
    if traffic_gb is not None:
        payload["traffic_gb"] = traffic_gb
    if expire_days is not None:
        payload["expire_days"] = expire_days
    # reset_usage is not implemented by the backend; do not claim to reset counters.
    return await _request("PUT", f"/users/{username}", payload)
