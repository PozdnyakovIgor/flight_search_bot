from telebot.types import Message

from keyboards.inline.search_history_keyboards.search_history_keyboard import (
    show_request_history,
)
from loader import bot


@bot.message_handler(commands=["history"])
def get_history(message: Message) -> None:
    """

    :param message: Message
    :return: None
    """
    bot.send_message(message.from_user.id, "Выберите один из недавних запросов:")
    show_request_history(message)
