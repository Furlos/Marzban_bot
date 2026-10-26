"""ASGI entry point with lifecycle cleanup."""
import uvicorn
from fastapi import FastAPI

from .api import get_service, user_router

app = FastAPI(title="Marzban Telegram control plane")


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}


app.include_router(user_router)


@app.on_event("shutdown")
async def close_client():
    if get_service.cache_info().currsize:
        await get_service().close()
        get_service.cache_clear()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
