from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from loader import bot


def departure_at_yes_no_markup(message: Message) -> None:
    """
    Вызов в чат инлайн-кнопки с вопросом хочет ли пользователь указать дату отправления
    :param message: Message
    :return: None
    """
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Да', callback_data='departure_yes'),
               InlineKeyboardButton('Нет', callback_data='departure_no'))
    bot.send_message(message.chat.id, "Хотите указать дату отправления?", reply_markup=markup)
