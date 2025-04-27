from typing import Optional

from pydantic import BaseModel


# Модели запросов
class UserCreate(BaseModel):
    username: str
    expire_days: int
    data_limit_gb: int


class UserUpdate(BaseModel):
    traffic_gb: Optional[int] = None
    expire_days: Optional[int] = None
    reset_usage: bool = False  # Всегда Тру, в этом нет смысла
