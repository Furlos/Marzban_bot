from fastapi import APIRouter, Depends, HTTPException
from .schemas import UserCreate, UserUpdate
from .user_service import UserService

router = APIRouter(tags=["Users"], prefix="/users")

async def get_user_service():
    """Dependency для получения UserService"""
    async with UserService() as service:
        yield service

@router.post("/", status_code=201, summary="Создать нового пользователя")
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    try:
        return await service.create_user(
            telegram_id=user_data.username,
            expire_days=user_data.expire_days,
            limit_traffic_gb=user_data.data_limit_gb
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{username}", summary="Обновить данные пользователя")
async def update_user(
    username: str,
    update_data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    try:
        return await service.update_user(
            telegram_id=username,
            limit_traffic_gb=update_data.traffic_gb,
            expire_days=update_data.expire_days
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{username}", summary="Получить информацию о пользователе")
async def get_user(
    username: str,
    service: UserService = Depends(get_user_service)
):
    try:
        return await service.get_user(username)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

