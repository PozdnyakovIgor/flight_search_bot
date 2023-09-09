from telebot.types import Message

from keyboards.inline.search_history_keyboards.search_history_keyboard import (
    show_request_history,
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
