import asyncio
import logging as log
import os
import threading

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from database import db
from handlers import register, start
from sheets import sync
from handlers.start import load_m

load_dotenv()
BOT_TOKEN = os.getenv("BOT_T")

log.basicConfig(level=log.INFO)
logger = log.getLogger(__name__)

b = Bot(token=BOT_TOKEN, parse_mode="HTML")
d = Dispatcher(storage=MemoryStorage())

async def main():
    logger.info("  Запуск")
    d.include_router(start.router)
    d.include_router(register.router)
    await d.start_polling(b)

def run_sync():
    sync.main()

if __name__ == "__main__":
		db.init_db()

		load_m()

		thread = threading.Thread(target=run_sync, daemon=True)
		thread.start()

		asyncio.run(main())
