from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from loader import bot


def return_at_yes_no_markup(message: Message) -> None:
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Да', callback_data='return_at_yes'),
               InlineKeyboardButton('Нет', callback_data='return_at_no'))
    bot.send_message(message.chat.id, "Хотите указать дату возвращения?", reply_markup=markup)
