from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import bot

from database.DataBase import DataBase
import keyboards.kb as kb

"""
    Homework#4
    1.0. Добавить возможность жаловаться на пользователей с помощью username или first_name
    1.1. Написать обработку на случай если такого пользователя нету в базе данных 
         (также относится к неправильному написанию его username или first_name)
    1.2. Проверять наличие такого пользователя по таблице пользователей из ДЗ номер 1.
    2.0. Когда кто-то пожаловался на пользователя тогда отправить ему сообщение
    2.1. В сообщений написать что на него пожаловались и он в учете за возможные нарушения

"""

class ReportState(StatesGroup):
    report_user = State()


async def report_start_report(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Вы хотите пожаловаться на участника группы?',
        reply_markup=await kb.two_button_inline_markup(
            text=['Да', 'Нет я передумал'],
            callback=['report_yes', 'report_no']))


async def report_send_message(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Напишите username или first_name участника:')
    await ReportState.report_user.set()


async def report_not_report(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Ок, до встречи!')


async def report_load_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        report = message.text
        if report:
            username = await DataBase().async_select_user_for_username(username=report.replace('@', ''))
            if username:
                await bot.send_message(
                    chat_id=username[1],
                    text='На вас поступила жалоба!')
            first_name = await DataBase().async_select_user_for_first_name(first_name=report)
            if first_name:
                await bot.send_message(
                    chat_id=username[1],
                    text='На вас поступила жалоба!')
            if not username and not first_name:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text='Пользователь не найден!')

    await state.finish()


def register_report_handlers(dp: Dispatcher):
    dp.register_message_handler(report_start_report, commands=['report'])
    dp.register_callback_query_handler(report_send_message, lambda call: call.data == 'report_yes')
    dp.register_callback_query_handler(report_not_report, lambda call: call.data == 'report_no')
    dp.register_message_handler(report_load_message, state=ReportState.report_user)
