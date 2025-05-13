# handlers/basic.py

from aiogram import types
from aiogram.dispatcher import Dispatcher

def register_basic_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):
        await message.reply(
            "Привет! Я Scrum-бот. Вот что я умею:",
            reply_markup=get_main_keyboard()
        )

    @dp.message_handler(lambda message: message.text == 'Добавить событие')
    async def add_event_start(message: types.Message):
        await EventStates.waiting_for_event_name.set()
        await message.reply("Введите название события:")

    @dp.message_handler(commands=['sprint_status'])
    async def sprint_status(message: types.Message):
        now = datetime.now(TIMEZONE)
        try:
            current_sprint_day = calculate_sprint_day(now)
            await message.reply(f"Сегодня {current_sprint_day}-й день спринта.")
        except Exception as e:
            await message.reply(f"Произошла ошибка: {str(e)}")
