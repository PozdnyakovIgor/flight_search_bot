from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def starting_keyboard() -> ReplyKeyboardMarkup:
    """
    Функция для создания reply-клавиатуры
    :return: markup
    :rtype: ReplyKeyboardMarkup
    """

    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keys = [KeyboardButton('/want_ticket'),
            KeyboardButton('/top_cheapest_tickets'),
            KeyboardButton('/nearest_airports'),
            KeyboardButton('/history'),
            KeyboardButton('/help')
            ]
    markup.add(*keys)
    return markup
