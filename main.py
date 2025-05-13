import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config.settings import API_TOKEN, TIMEZONE
from database.events_db import load_events
from handlers.basic import register_basic_handlers
from handlers.events import register_event_handlers
from handlers.list_delete import register_list_delete_handlers
from jobs.scheduler_jobs import send_event_notifications, cleanup_old_events

# Настройка логирования
logging.basicConfig(level=logging.INFO)
os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/bot.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_handler)

async def main():
    bot = Bot(token=API_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)

    load_events()

    register_basic_handlers(dp)
    register_event_handlers(dp)
    register_list_delete_handlers(dp)

    scheduler.add_job(lambda: send_event_notifications(bot), trigger="cron", minute="*")
    scheduler.add_job(cleanup_old_events, trigger="cron", hour=0, minute=0)
    scheduler.start()

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await bot.session.close()
        scheduler.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
