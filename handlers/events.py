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
            data['name'] =
