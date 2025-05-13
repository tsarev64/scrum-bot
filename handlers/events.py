# handlers/events.py

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

class EventStates(StatesGroup):
    waiting_for_event_name = State()
    waiting_for_event_date = State()
    waiting_for_event_time = State()
    waiting_for_event_repeat = State()
    waiting_for_weekdays = State()
    waiting_for_interval = State()  # Новое состояние

def register_event_handlers(dp):
    @dp.message_handler(lambda message: message.text == 'Добавить событие')
    async def add_event_start(message: types.Message):
        await EventStates.waiting_for_event_name.set()
        await message.reply("Введите название события:")

    @dp.message_handler(state=EventStates.waiting_for_event_name)
    async def process_event_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['name'] = message.text.strip()
        await message.reply("Введите дату события в формате ГГГГ-ММ-ДД:")
        await EventStates.next()

    @dp.message_handler(state=EventStates.waiting_for_event_date)
    async def process_event_date(message: types.Message, state: FSMContext):
        try:
            event_date = datetime.strptime(message.text.strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
            async with state.proxy() as data:
                data['date'] = event_date
            await message.reply("Введите время события в формате ЧЧ:ММ:")
            await EventStates.next()
        except ValueError:
            await message.reply("Неверный формат даты. Введите в формате ГГГГ-ММ-ДД:")

    @dp.message_handler(state=EventStates.waiting_for_event_time)
    async def process_event_time(message: types.Message, state: FSMContext):
        try:
            time_str = message.text.strip()
            datetime.strptime(time_str, "%H:%M")
            async with state.proxy() as data:
                data['time'] = time_str
            keyboard = InlineKeyboardMarkup()
            keyboard.add(
                InlineKeyboardButton("Однократное", callback_data="repeat_no"),
                InlineKeyboardButton("Ежедневное", callback_data="repeat_daily"),
                InlineKeyboardButton("По дням недели", callback_data="repeat_weekly")
            )
            await message.reply("Выберите тип события:", reply_markup=keyboard)
            await EventStates.next()
        except ValueError:
            await message.reply("Неверный формат времени. Введите в формате ЧЧ:ММ:")

    @dp.callback_query_handler(lambda c: c.data == "repeat_no", state=EventStates.waiting_for_event_repeat)
    async def process_repeat_no(callback_query: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            event = {
                'name': data['name'],
                'time': data['time'],
                'repeat': False,
                'date': data['date']
            }
            events_db.append(event)
            save_events()
        await state.finish()
        await bot.send_message(
            callback_query.from_user.id,
            f"Событие '{data['name']}' добавлено на {data['time']}!",
            reply_markup=get_main_keyboard()
        )
        await bot.answer_callback_query(callback_query.id)

    @dp.callback_query_handler(lambda c: c.data == "repeat_daily", state=EventStates.waiting_for_event_repeat)
    async def process_repeat_daily(callback_query: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            event = {
                'name': data['name'],
                'time': data['time'],
                'repeat': True,
                'repeat_type': 'daily'
            }
            events_db.append(event)
            save_events()
        await state.finish()
        await bot.send_message(
            callback_query.from_user.id,
            f"Событие '{data['name']}' добавлено ежедневно на {data['time']}!",
            reply_markup=get_main_keyboard()
        )
        await bot.answer_callback_query(callback_query.id)

    @dp.callback_query_handler(lambda c: c.data == "repeat_weekly", state=EventStates.waiting_for_event_repeat)
    async def process_repeat_weekly(callback_query: types.CallbackQuery, state: FSMContext):
        await EventStates.waiting_for_interval.set()
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("Еженедельно", callback_data="interval_weekly"),
            InlineKeyboardButton("Раз в две недели", callback_data="interval_biweekly")
        )
        await bot.send_message(
            callback_query.from_user.id,
            "Выберите интервал повторения:",
            reply_markup=keyboard
        )
        await bot.answer_callback_query(callback_query.id)

    @dp.callback_query_handler(lambda c: c.data.startswith('interval_'), state=EventStates.waiting_for_interval)
    async def select_interval(callback_query: types.CallbackQuery, state: FSMContext):
        interval = callback_query.data.replace("interval_", "")
        async with state.proxy() as data:
            data['interval'] = interval
        await EventStates.waiting_for_weekdays.set()
        await bot.send_message(
            callback_query.from_user.id,
            "Выберите дни недели для повторения:",
            reply_markup=get_weekdays_keyboard()
        )
        await bot.answer_callback_query(callback_query.id)

    @dp.callback_query_handler(lambda c: c.data.startswith('weekday_'), state=EventStates.waiting_for_weekdays)
    async def select_weekday(callback_query: types.CallbackQuery, state: FSMContext):
        weekday = int(callback_query.data.replace("weekday_", ""))
        async with state.proxy() as data:
            if 'weekdays' not in data:
                data['weekdays'] = []
            if weekday not in data['weekdays']:
                data['weekdays'].append(weekday)
        await bot.answer_callback_query(callback_query.id)

    @dp.callback_query_handler(lambda c: c.data == "confirm_weekdays", state=EventStates.waiting_for_weekdays)
    async def confirm_weekdays(callback_query: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            event = {
                'name': data['name'],
                'time': data['time'],
                'repeat': True,
                'repeat_type': 'weekly',
                'weekdays': data.get('weekdays', []),
                'interval': data.get('interval', 'weekly')
            }
            events_db.append(event)
            save_events()
        await state.finish()
        await bot.send_message(
            callback_query.from_user.id,
            f"Событие '{data['name']}' добавлено по дням недели на {data['time']}!",
            reply_markup=get_main_keyboard()
        )
        await bot.answer_callback_query(callback_query.id)
