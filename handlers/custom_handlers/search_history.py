from telebot.types import Message, CallbackQuery

from database.db_core import History, Users
from keyboards.inline.search_history_keyboards.search_history_keyboard import (
    show_request_history,
    show_tickets,
)
from loader import bot


@bot.message_handler(commands=["history"])
def get_history(message: Message) -> None:
    """
    Метод для получения истории. При вызове команды выдается история последних 10 запросов с инлайн-кнопкой,
    которая выводит информацию о найденных билетах
    :param message: Message
    :return: None
    """
    bot.send_message(message.from_user.id, "Выберите один из недавних запросов:")
    show_request_history(message)


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def show_tickets_info(call: CallbackQuery) -> None:
    if call.data:
        # show_tickets(call.message)
        bot.send_message(call.message.chat.id, call.data)
