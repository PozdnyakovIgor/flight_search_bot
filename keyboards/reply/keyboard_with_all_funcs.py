from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def starting_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keys = [KeyboardButton('/Хочу найти билет!'),
            KeyboardButton('/Хочу отдохнуть, но не знаю где...'),
            KeyboardButton('/Ближайшие аэропорты'),
            KeyboardButton('/История'),
            KeyboardButton('/FAQ')
            ]
    markup.add(*keys)
    return markup
