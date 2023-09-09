from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from database.db_core import History, Users
from loader import bot


def show_request_history(message: Message):

    for history_entry in (
        History.select()
        .where(History.user == Users.get(Users.nickname == message.chat.username))
        .order_by(History.date_time.desc())
    ):
        history_entry = f"Команда: \\{history_entry.command};\nЗапрос: {history_entry.request_info};\nДата и время запроса: {history_entry.date_time}"
        bot.send_message(
            message.from_user.id,
            history_entry,
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    text="вывести результат поиска", callback_data="дописать"
                )
            ),
        )
