"""Authenticated internal API for Marzban user management."""
import hmac
import os
from functools import lru_cache

from fastapi import APIRouter, Depends, Header, HTTPException

from .config import api_token, api_url
from .schemas import UserCreate, UserUpdate
from .user_service import MarzbanAPIError, UserService


async def require_internal_token(x_internal_token: str | None = Header(default=None)) -> None:
    expected = os.getenv("INTERNAL_API_KEY")
    if not expected:
        raise HTTPException(status_code=503, detail="Internal API authentication is not configured.")
    if not x_internal_token or not hmac.compare_digest(x_internal_token, expected):
        raise HTTPException(status_code=401, detail="Invalid internal API token.")


@lru_cache(maxsize=1)
def get_service() -> UserService:
    if not api_token or not api_url:
        raise HTTPException(status_code=503, detail="Marzban API is not configured.")
    return UserService(api_url=api_url, api_token=api_token)


user_router = APIRouter(
    tags=["Users"],
    prefix="/users",
    dependencies=[Depends(require_internal_token)],
)


@user_router.post("/")
async def create_user(user: UserCreate, service: UserService = Depends(get_service)):
    try:
        return await service.create_user(
            telegram_id=user.username,
            expire_days=user.expire_days,
            limit_traffic_gb=user.data_limit_gb,
        )
    except MarzbanAPIError as exc:
        raise HTTPException(status_code=502, detail="Marzban service unavailable.") from exc


@user_router.put("/{user_id}")
async def update_user(
    user_id: str, update: UserUpdate, service: UserService = Depends(get_service)
):
    try:
        return await service.update_user(
            telegram_id=user_id,
            limit_traffic_gb=update.traffic_gb,
            expire_days=update.expire_days,
        )
    except MarzbanAPIError as exc:
        raise HTTPException(status_code=502, detail="Marzban service unavailable.") from exc


@user_router.get("/{user_id}")
async def get_user(user_id: str, service: UserService = Depends(get_service)):
    try:
        return await service.get_user(telegram_id=user_id)
    except MarzbanAPIError as exc:
        # Preserve a 404 distinction for Telegram's first-time user flow.
        if "status: 404" in str(exc):
            raise HTTPException(status_code=404, detail="User not found.") from exc
        raise HTTPException(status_code=502, detail="Marzban service unavailable.") from exc
