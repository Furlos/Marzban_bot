import uvicorn
from fastapi import FastAPI

from admin.api import admin_router
from user.api import user_router

app = FastAPI()
app.include_router(marzban_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)