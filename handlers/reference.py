import binascii
import os

from aiogram import types, Dispatcher
from aiogram.utils.deep_linking import _create_link

from config import bot

from database.DataBase import DataBase
import keyboards.kb as kb

"""
    Homework#5
    1.0. Добавить реферальную программу в старт меню
    1.1. По переходу в реферальную программу добавить две кнопки
    1.1.0. Первая кнопка -> Реферальная ссылка 
           по ней выдавать реферальную ссылку, и если она есть выдавать существующую ссылку
    1.1.1. Вторая кнопка -> Список Рефералов
           Список должен содержать только список рефералов который привел пользователь, если нету пользователей, 
           так и писать пользователю
    2.0. Создать таблицу reference_users
    2.1. Дополнить таблицу telegram_users полем reference_link

"""


async def reference_statr_reference(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='реферальная программа:',
        reply_markup=await kb.two_button_inline_markup(
            text=['Реферальная ссылка', 'Спаисок рефералов'],
            callback=['refer_link', 'refer_list']))


async def reference_set_link(call: types.CallbackQuery):
    user = await DataBase().async_select_user_for_id(user_id=call.from_user.id)
    if user[-1]:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=f'reference link:`{user[-1]}`',
            parse_mode=types.ParseMode.MARKDOWN_V2)
    else:
        token = binascii.hexlify(os.urandom(4)).decode()
        link = await _create_link(link_type='start', payload=token)
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=f'reference link: `{link}`',
            parse_mode=types.ParseMode.MARKDOWN_V2)
        await DataBase().async_update_user_ref_link(user_id=call.from_user.id, link=link)


async def reference_list(call: types.CallbackQuery):
    _reference_list = await DataBase.async_get_reference_list(user_id=call.from_user.id)
    if reference_list:
        text = '\n'.join([i['username'] for i in _reference_list])
    else:
        text = 'У вас нет референтов!'
    await bot.send_message(
        text=text,
        chat_id=call.message.chat.id)


def register_reference_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(reference_statr_reference, lambda call: call.data == 'start_btn_refer')
    dp.register_callback_query_handler(reference_set_link, lambda call: call.data == 'refer_link')
    dp.register_callback_query_handler(reference_list, lambda call: call.data == 'refer_list')
