# config/settings.py

import os

# Telegram API
API_TOKEN = 'ВАШ_ТОКЕН'  # Замените на ваш токен

# Чаты
TEAM_CHAT_ID = -1002563451675  # Командный чат (супергруппа)
SERVICE_CHAT_ID = -1002563451675  # Служебный чат
ADMIN_USER_ID = 123456789  # Ваш Telegram ID для уведомлений

# Часовой пояс
TIMEZONE = "Europe/Moscow"

# Файлы
EVENTS_FILE = "events.json"
CONFIG_FILE = "config.json"

# Праздники
HOLIDAYS = [
    "2025-01-01", "2025-01-02", "2025-01-07", "2025-02-23",
    "2025-03-08", "2025-05-01", "2025-06-12", "2025-06-13",
    "2025-11-04"
]

# Начало спринта
SPRINT_START_DATE = "2025-04-23"
