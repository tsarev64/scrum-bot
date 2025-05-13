# utils/chat_migrations.py

from aiogram.utils.exceptions import MigrateToChat
from config.settings import ADMIN_USER_ID
import json
import os

async def handle_chat_migration(bot, old_id, new_id):
    """
    Обрабатывает миграцию чата в супергруппу.
    Обновляет TEAM_CHAT_ID и уведомляет администратора.
    """
    from config.settings import CONFIG_FILE

    # Загрузка текущего конфига
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)

    # Обновление ID чата
    if config.get("TEAM_CHAT_ID") == old_id:
        config["TEAM_CHAT_ID"] = new_id
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

    # Уведомление администратора
    try:
        await bot.send_message(
            ADMIN_USER_ID,
            f"⚠️ Чат был перемещён в супергруппу!\n"
            f"Старый ID: `{old_id}`\n"
            f"Новый ID: `{new_id}`\n"
            f"ID сохранён в файл конфигурации.",
            parse_mode="Markdown"
        )
    except Exception as e:
        from logging import getLogger
        logger = getLogger(__name__)
        logger.error(f"Не удалось отправить уведомление админу: {e}")
