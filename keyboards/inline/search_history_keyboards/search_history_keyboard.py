from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from database.db_core import History, Users
from loader import bot


def search_history_markup(message: Message):
    history_markup = InlineKeyboardMarkup()
    for history_entry in (
        History.select()
        .where(History.user == Users.get(Users.nickname == message.chat.username))
        .order_by(History.date_time.desc())
    ):

        history_markup.add(
            InlineKeyboardButton(
                text=f"команда: {history_entry.command}\n"
                f"запрос: {history_entry.request_info}\n"
                f"дата и время запроса: {history_entry.date_time}",
                callback_data="test",
            )
        )

    bot.send_message(
        message.from_user.id,
        "Выберите один из недавних запросов:",
        reply_markup=history_markup,
    )
