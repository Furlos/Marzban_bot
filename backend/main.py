import uvicorn
from fastapi import FastAPI

from admin.api import admin_router
from backend.autorization.api import autorization_router
from user.api import user_router

app = FastAPI()
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(autorization_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
