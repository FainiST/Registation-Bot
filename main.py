from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start, register
from database.db import init_db
from dotenv import load_dotenv
import asyncio
import logging as log
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_T")

log.basicConfig(level=log.INFO)
logger = log.getLogger(__name__)

b = Bot(token=BOT_TOKEN, parse_mode="HTML")
d = Dispatcher(storage=MemoryStorage())

async def main():
    init_db()
    logger.info("  Запуск")

    d.include_router(start.router)
    d.include_router(register.router)

    await d.start_polling(b)

if __name__ == "__main__":
    asyncio.run(main())
