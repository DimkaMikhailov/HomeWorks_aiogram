from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import bot


"""
    Homework#3
    1.0. Создать FSM для информации об анкете пользователя
    2.0. При успешном прохождении отправлять форму обратно пользователю.
"""


class UserState(StatesGroup):
    month = State()
    options = State()
    photo = State()


async def user_fsm_start(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text='Какой у вас месяц обучения?')
    await UserState.month.set()


async def user_fsm_month(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit():
            data['month'] = message.text
        else:
            await state.finish()
            await bot.send_message(
                chat_id=message.chat.id,
                text='Используйте только цифры!')

    await UserState.next()
    await message.answer(
        text='Какое у тебя направление?')


async def user_fsm_options(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['options'] = message.text
    await UserState.next()
    await message.answer(
        text='Скинь свою любимую фотку!')


async def load_user_fsm_photo(message: types.Message, state: FSMContext):
                                                            # Путь до вашей папке media
    path = await message.photo[-1].download(destination_dir=r"E:\MY\telegram_bot\media")
    async with state.proxy() as data:
        data['photo'] = path.name
        if data:
            with open(data['photo'], "rb") as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption=f"*Твой месяц:* {data['month']}\n"
                            f"*Твой профиль:* {data['options']}\n",
                    parse_mode=types.ParseMode.MARKDOWN)

                await state.finish()


def register_user_fsm_handlers(dp: Dispatcher):
    dp.register_message_handler(user_fsm_start, commands=['anketa'])
    dp.register_message_handler(user_fsm_month, content_types=["text"], state=UserState.month)
    dp.register_message_handler(user_fsm_options, content_types=["text"], state=UserState.options)
    dp.register_message_handler(load_user_fsm_photo, content_types=["text"], state=UserState.photo)
