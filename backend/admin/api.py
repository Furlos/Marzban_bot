from fastapi import APIRouter, Query
from fastapi.responses import Response
from service import AdminService

qr_router = APIRouter(prefix="/admin", tags=["admins"])

