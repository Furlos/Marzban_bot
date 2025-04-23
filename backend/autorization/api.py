from fastapi import APIRouter, Query
from fastapi.responses import Response
from service import AutorizationService

autorization_router = APIRouter(prefix="/autorization", tags=["Autorizations"])


@autorization_router.get("/")
async def autorization(
    self,
    username: str,
    password: str,
):
    return "Succes if 200 else Error"
