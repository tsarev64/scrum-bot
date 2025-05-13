# services/event_notifier.py

from aiogram.utils.exceptions import MigrateToChat
from aiogram import Bot
from config.settings import TEAM_CHAT_ID

async def notify_event(bot: Bot, event):
    global TEAM_CHAT_ID
    try:
        await bot.send_message(TEAM_CHAT_ID, f"{event['name']}")
    except MigrateToChat as e:
        new_chat_id = e.migrate_to_chat_id
        from utils.chat_migrations import handle_chat_migration
        await handle_chat_migration(bot, TEAM_CHAT_ID, new_chat_id)
