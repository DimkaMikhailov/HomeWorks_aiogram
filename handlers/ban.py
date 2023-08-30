from aiogram import types, Dispatcher
from config import bot

"""
    Homework#2
    1.0. Создать группу. 
    1.1. Сделать бота админом группы.
    2.0. Добавить логику удаления сообщений в группе которые содержат недопустимые слова.
    2.1. После удаления сообщения, отправить пользователю что он подозрителен и может быть забанен
"""


async def ban_scan_words(message: types.Message):
    words = ["damn", "fuck", 'bitch']

    for ban_word in words:
        if ban_word in message.text.lower().strip():

            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id)

            await bot.send_message(
                chat_id=message.chat.id,
                text=f"{message.from_user.username}: Вас могут забанить!")


def register_ban_handlers(dp: Dispatcher):
    dp.register_message_handler(ban_scan_words)

