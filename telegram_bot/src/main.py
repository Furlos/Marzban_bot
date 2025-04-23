from aiogram import Bot
import asyncio
from config import token
from handlers.handlers import dp


bot = Bot(token=token)

# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())