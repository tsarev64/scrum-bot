# jobs/scheduler_jobs.py

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
from services.event_notifier import notify_event
from database.events_db import get_all_events, clear_old_events

TIMEZONE = pytz.timezone("Europe/Moscow")

def should_notify_event(event, current_datetime):
    if not event.get('repeat'):
        event_date = datetime.strptime(event['date'], "%Y-%m-%d").date()
        return event_date == current_datetime.date()

    repeat_type = event.get('repeat_type', 'none')
    interval = event.get('interval', 'weekly')

    if repeat_type == 'daily':
        return True
    elif repeat_type == 'weekly':
        weekday_match = current_datetime.weekday() in event.get('weekdays', [])
        if interval == 'biweekly':
            week_number = current_datetime.isocalendar().week
            return weekday_match and (week_number % 2 == 0)
        return weekday_match

    return False

async def send_event_notifications(bot):
    now = datetime.now(TIMEZONE)
    for event in get_all_events():
        if event['time'] == now.strftime("%H:%M") and should_notify_event(event, now):
            await notify_event(bot, event)

async def cleanup_old_events_task():
    clear_old_events()
