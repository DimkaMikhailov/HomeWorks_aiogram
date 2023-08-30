from aiogram import types, Dispatcher
from aiogram.utils.deep_linking import _create_link

from config import bot
from database.DataBase import DataBase
import keyboards.kb as kb

""" Homework#1
    1.0. Создать своего бота. Открыть как новый проект с чистого листа.
    1.1. Разделить всю логику на модули и не хранить токен бота в файле с кодом.
    2.0. Создать таблицу для пользователей телеграмм (пример есть на репозиторий урока)
    2.1. Записывать пользователя в таблицу базы данных, если он выполнил команду /start
"""


async def start_command_start(message: types.Message):
    await DataBase().async_insert_into_users((
          None,
          message.from_user.id,
          message.from_user.first_name,
          message.from_user.last_name,
          message.from_user.username,
          None))

    _, token = message.get_full_command()
    if token:
        link = await _create_link(link_type='start', payload=token)
        referral = await DataBase.async_get_referral(by_link=link)
        if referral:
            in_base = await DataBase().async_references_in_pair(_from=referral[1],
                                                                to=message.from_user.id)
            if not in_base:
                await DataBase.async_set_reference_pair(_from=referral[1], to=message.from_user.id)

    await bot.send_message(
        chat_id=message.chat.id,
        text='Привет!',
        reply_markup=await kb.one_button_inline_markup(
            text='Reference', callback='start_btn_refer'))


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command_start, commands=['start'])
