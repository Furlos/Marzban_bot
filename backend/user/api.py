from fastapi import APIRouter, Query
from fastapi.responses import Response
from service import UserService

qr_router = APIRouter(prefix="/user", tags=["Users"])

