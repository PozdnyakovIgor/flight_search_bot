from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def yes_no_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Да', callback_data='yes'),
               InlineKeyboardButton('Нет', callback_data='no'))
    return markup

