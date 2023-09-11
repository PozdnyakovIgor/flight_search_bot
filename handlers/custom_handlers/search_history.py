from telebot.types import Message, CallbackQuery
from database.search_history_funcs import (
    show_request_history,
)
from database.search_history_funcs import show_tickets
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


@bot.callback_query_handler(func=lambda call: len(call.data) == 19)
def show_tickets_info(call: CallbackQuery) -> None:
    """
    Метод для получения информации о найденных билетах
    :param call: CallbackQuery
    :return: None
    """
    bot.send_message(call.message.chat.id, "Результат по данному запросу:")
    show_tickets(call.message, call.data)
