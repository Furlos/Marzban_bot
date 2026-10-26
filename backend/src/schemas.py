"""Request validation for the internal backend."""
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    expire_days: int = Field(ge=1, le=365)
    data_limit_gb: int = Field(ge=1, le=10000)


class UserUpdate(BaseModel):
    traffic_gb: int | None = Field(default=None, ge=0, le=10000)
    expire_days: int | None = Field(default=None, ge=1, le=365)
