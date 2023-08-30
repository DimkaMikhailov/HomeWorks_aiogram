from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def three_button_inline_markup(text: list, callback: list):
    if len(text) == 3 == len(callback):
        button1 = InlineKeyboardButton(text[0], callback_data=callback[0])
        button2 = InlineKeyboardButton(text[1], callback_data=callback[1])
        button3 = InlineKeyboardButton(text[2], callback_data=callback[2])
        markup = InlineKeyboardMarkup()
        markup.add(button1).add(button2).add(button3)
        return markup


async def two_button_inline_markup(text: list, callback: list):
    if len(text) == 2 and len(callback) == 2:
        button1 = InlineKeyboardButton(text[0], callback_data=callback[0])
        button2 = InlineKeyboardButton(text[1], callback_data=callback[1])
        markup = InlineKeyboardMarkup()
        markup.add(button1, button2)
        return markup


async def one_button_inline_markup(text: str, callback: str):
    button1 = InlineKeyboardButton(text, callback_data=callback)
    markup = InlineKeyboardMarkup()
    markup.add(button1)
    return markup


async def four_button_inline_markup(text: list, callback: list):
    if len(text) == 4 and len(callback) == 4:
        button1 = InlineKeyboardButton(text[0], callback_data=callback[0])
        button2 = InlineKeyboardButton(text[1], callback_data=callback[1])
        button3 = InlineKeyboardButton(text[2], callback_data=callback[2])
        button4 = InlineKeyboardButton(text[3], callback_data=callback[3])
        markup = InlineKeyboardMarkup()
        markup.add(button1, button2)
        markup.add(button3, button4)
        return markup


async def delete_articles_inline_markup(article_list: list):
    markup = InlineKeyboardMarkup()
    for article in article_list:
        text = f" ❌  {article['title']}"
        callback = f'delete_article_btn_{article["id"]}'
        markup.add(InlineKeyboardButton(
            text=text, callback_data=callback))

    return markup
