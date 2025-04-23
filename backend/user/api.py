from fastapi import APIRouter, Query
from fastapi.responses import Response
from service import UserService

user_router = APIRouter(prefix="/user", tags=["Users"])

service = UserService(username="что", password="what")


@user_router.post("/create")
async def create_user(
    username: str,
):
    return service.create(username)


@user_router.post("/create")
async def restart_sub(
    username: str,
):
    return service.restart_sub(username)
