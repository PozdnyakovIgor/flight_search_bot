from telebot.types import Message

from keyboards.inline.search_history_keyboards.search_history_keyboard import search_history_markup
from loader import bot


@bot.message_handler(commands=["history"])
def get_history(message: Message) -> None:
    """

    :param message: Message
    :return: None
    """

    search_history_markup(message)
