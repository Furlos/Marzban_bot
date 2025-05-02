from uuid import uuid4
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from .schemas import UserCreate, UserUpdate
from .config import config_name
from .token_manager import TokenManager, MarzbanAPIError

router = APIRouter(tags=["Users"], prefix="/users")

class UserService:
    def __init__(self, token_manager: Optional[TokenManager] = None):
        self.token_manager = token_manager
        self.client = httpx.AsyncClient(timeout=30.0)
        self._update_headers()

    def _update_headers(self):
        self.client.headers.update({
            "Authorization": f"Bearer {config_name.api_token}",
            "Content-Type": "application/json"
        })

    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        url = f"{config_name.api_url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            response = await self.client.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_detail = f"Status: {e.response.status_code}, Response: {e.response.text}"
            if e.response.status_code == 401 and self.token_manager:
                if await self.token_manager.manual_refresh():
                    self._update_headers()
                    return await self._make_request(method, endpoint, data)
            raise MarzbanAPIError(f"API Error: {error_detail}")
        except Exception as e:
            raise MarzbanAPIError(f"Connection Error: {str(e)}")

    @staticmethod
    def _generate_vless_link(uuid: str, domain: str, port: int, username: str) -> str:
        """Генерация корректной VLESS-ссылки"""
        return (
            f"vless://{uuid}@{domain}:{port}?"
            f"type=tcp&"
            f"security=tls&"
            f"flow=xtls-rprx-vision&"
            f"sni={domain}#"
            f"{username}"
        )

    async def create_user(self, telegram_id: str, limit_traffic_gb: float, expire_days: int) -> Dict[str, Any]:
        expire_date = datetime.now() + timedelta(days=expire_days)
        user_uuid = str(uuid4())
        domain = "instant-paris.space"  # Ваш домен
        vless_port = 8443  # Порт из конфига Xray

        user_data = {
            "username": str(telegram_id),
            "proxies": {
                "vless": {
                    "id": user_uuid,
                    "flow": "xtls-rprx-vision"
                }
            },
            "inbounds": {"vless": ["VLESS-TLS"]},
            "expire": int(expire_date.timestamp()),
            "data_limit": int(limit_traffic_gb * 1073741824),
            "data_limit_reset_strategy": "month"
        }

        try:
            response = await self._make_request("POST", "/api/user", user_data)
            return {
                "username": response["username"],
                "expire_date": expire_date.strftime("%Y-%m-%d"),
                "data_limit_gb": limit_traffic_gb,
                "connection_link": self._generate_vless_link(
                    uuid=user_uuid,
                    domain=domain,
                    port=vless_port,
                    username=response["username"]
                )
            }
        except Exception as e:
            raise MarzbanAPIError(f"Ошибка создания пользователя: {str(e)}")

    async def update_user(self, telegram_id: str,
                          limit_traffic_gb: Optional[float] = None,
                          expire_days: Optional[int] = None) -> Dict[str, Any]:
        current_user = await self._make_request("GET", f"/api/user/{telegram_id}")
        update_data = {}

        if expire_days is not None:
            new_expire = datetime.now() + timedelta(days=expire_days)
            update_data["expire"] = int(new_expire.timestamp())

        if limit_traffic_gb is not None:
            update_data["data_limit"] = int(limit_traffic_gb * 1073741824)

        if update_data:
            updated_user = await self._make_request("PUT", f"/api/user/{telegram_id}", update_data)
            return await self._format_user_response(updated_user)
        return await self._format_user_response(current_user)

    async def get_user(self, telegram_id: str) -> Dict[str, Any]:
        user_data = await self._make_request("GET", f"/api/user/{telegram_id}")
        return await self._format_user_response(user_data)

    async def _format_user_response(self, user_data: Dict) -> Dict:
        domain = "instant-paris.space"
        vless_port = 8443
        return {
            "username": user_data["username"],
            "expire_date": datetime.fromtimestamp(user_data["expire"]).strftime("%Y-%m-%d"),
            "data_limit_gb": user_data["data_limit"] / 1073741824,
            "used_traffic_gb": user_data.get("used_traffic", 0) / 1073741824,
            "status": user_data["status"],
            "connection_link": self._generate_vless_link(
                uuid=user_data["proxies"]["vless"]["id"],
                domain=domain,
                port=vless_port,
                username=user_data["username"]
            )
        }

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()