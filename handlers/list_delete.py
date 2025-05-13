# handlers/list_delete.py

from aiogram import types
from aiogram.dispatcher import FSMContext

def register_list_delete_handlers(dp):
    @dp.message_handler(lambda message: message.text == 'Список событий')
    async def list_events(message: types.Message):
        if not events_db:
            await message.reply("Нет активных событий.")
            return
        events_list = []
        for i, event in enumerate(events_db, 1):
            event_type = ""
            if not event.get('repeat'):
                event_type = "🔁 Одноразовое"
            elif event.get('repeat_type') == 'daily':
                event_type = "📅 Ежедневное"
            elif event.get('repeat_type') == 'weekly':
                interval = event.get('interval', 'weekly')
                if interval == 'biweekly':
                    event_type = "🗓️ Раз в две недели"
                else:
                    event_type = "🔄 Еженедельное"
            date_info = f" ({event['date']})" if 'date' in event else ""
            events_list.append(f"{i}. {event['name']} в {event['time']}{date_info} - {event_type}")
        await message.reply("Список событий:\n" + "\n".join(events_list))

    @dp.message_handler(lambda message: message.text == 'Удалить событие')
    async def delete_event_start(message: types.Message):
        if not events_db:
            await message.reply("Нет событий для удаления.")
            return
        keyboard = InlineKeyboardMarkup()
        for i, event in enumerate(events_db, 1):
            keyboard.add(InlineKeyboardButton(
                text=f"{i}. {event['name']} ({event['time']})",
                callback_data=f"delete_{i-1}"
            ))
        await message.reply("Выберите событие для удаления:", reply_markup=keyboard)

    @dp.callback_query_handler(lambda c: c.data.startswith('delete_'))
    async def process_delete(callback_query: types.CallbackQuery):
        event_index = int(callback_query.data.replace('delete_', ''))
        if 0 <= event_index < len(events_db):
            deleted_event = events_db.pop(event_index)
            save_events()
            await bot.send_message(
                callback_query.from_user.id,
                f"Событие '{deleted_event['name']}' удалено!",
                reply_markup=get_main_keyboard()
            )
        else:
            await bot.send_message(callback_query.from_user.id, "Ошибка: событие не найдено.")
        await bot.answer_callback_query(callback_query.id)
