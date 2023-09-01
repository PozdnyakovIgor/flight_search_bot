from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_url_button(url):
    kb = InlineKeyboardMarkup()
    url_button = InlineKeyboardButton(text='Ссылка на билет', url=url)
    kb.add(url_button)
    return kb

