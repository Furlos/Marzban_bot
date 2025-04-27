from fastapi import APIRouter
from schemas import UserCreate, UserUpdate

from config import api_token, api_url
from user_service import UserService

user_router = APIRouter(tags=["Users"], prefix="/users")

marzban = UserService(api_url=api_url, api_token=api_token)


@user_router.post("/")
async def create_user(user: UserCreate):
    return await marzban.create_user(
        telegram_id=user.username,
        expire_days=user.expire_days,
        limit_traffic_gb=user.data_limit_gb,
    )


@user_router.put("/{user_id}")
async def update_user(username: str, update: UserUpdate):
    return marzban.update_user(
        telegram_id=username,
        limit_traffic_gb=update.traffic_gb,
        expire_days=update.expire_days,
    )


@user_router.get("/{user_id}")
async def get_user(username: str):
    return marzban.get_user(telegram_id=username)
