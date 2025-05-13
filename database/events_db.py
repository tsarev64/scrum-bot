# database/events_db.py

import json
import os
from config.settings import EVENTS_FILE

_events_db = []

def load_events():
    global _events_db
    if os.path.exists(EVENTS_FILE):
        try:
            with open(EVENTS_FILE, "r", encoding="utf-8") as f:
                _events_db = json.load(f)
        except json.JSONDecodeError:
            _events_db = []
    else:
        _events_db = []

def save_events(events):
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=4)

def get_all_events():
    return _events_db

def add_event(event):
    _events_db.append(event)
    save_events(_events_db)

def delete_event(index):
    if 0 <= index < len(_events_db):
        del _events_db[index]
        save_events(_events_db)

def clear_old_events():
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d")
    filtered = [e for e in _events_db if e.get('repeat') or e.get('date', '') >= now]
    if len(filtered) != len(_events_db):
        _events_db[:] = filtered
        save_events(_events_db)
