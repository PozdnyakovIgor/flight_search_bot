from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def starting_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keys = [KeyboardButton('/want_ticket'),
            KeyboardButton('/fly_away'),
            KeyboardButton('/nearest_airports'),
            KeyboardButton('/history'),
            KeyboardButton('/help')
            ]
    markup.add(*keys)
    return markup
