from telebot.types import Message, CallbackQuery

from database.db_core import History, Users, TicketsInfo
from database.search_history_funcs import (
    show_request_history,
)

from database.search_history_funcs import show_tickets
from keyboards.inline.url_button import make_url_button
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


# @bot.callback_query_handler(func=lambda call: isinstance(call.data, str))
@bot.callback_query_handler(func=lambda call: len(call.data) == 19)
def show_tickets_info(call: CallbackQuery) -> None:
    bot.send_message(call.message.chat.id, "Результат по данному запросу:")
    show_tickets(call.message, call.data)


    # for history_entry in (
    #     History.select()
    #     .where(History.user == Users.get(Users.nickname == call.message.chat.username))
    #     .order_by(History.date_time.desc())
    # ):
    #     for one_ticket in TicketsInfo.select().where(
    #         (TicketsInfo.request_id == history_entry.id)
    #         & (call.data == str(history_entry.date_time))
    #     ):
    #         one_ticket_info = one_ticket.ticket_info
    #         one_ticket_link = one_ticket.ticket_link
    #
    #         bot.send_message(
    #             call.message.chat.id,
    #             one_ticket_info,
    #             reply_markup=make_url_button(one_ticket_link),
    #         )
