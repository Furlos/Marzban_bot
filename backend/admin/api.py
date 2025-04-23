from fastapi import APIRouter, Query
from fastapi.responses import Response
from service import AdminService


service = AdminService(username="что", password="what")
admin_router = APIRouter(prefix="/admin", tags=["admins"])


@admin_router.post("/create")
async def create_admin(
    self,
    username: str,
    password: str,
):
    return service.create(username, password)
