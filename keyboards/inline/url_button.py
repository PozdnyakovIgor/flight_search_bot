from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_url_button(url):
    """
    Вызов в чат url-кнопки со ссылкой на билет
    :param url: url
    :return: kb
    :rtype: InlineKeyboardMarkup
    """
    kb = InlineKeyboardMarkup()
    url_button = InlineKeyboardButton(text='Ссылка на билет', url=url)
    kb.add(url_button)
    return kb

