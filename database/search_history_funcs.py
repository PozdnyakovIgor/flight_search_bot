from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
)

from database.db_core import History, Users, TicketsInfo
from keyboards.inline.url_button import make_url_button
from loader import bot


def show_request_history(message: Message) -> None:
    """
    Метод, который отправляет в ТГ-чат последние 10 запросов пользователя. Под каждым запросом есть инлайн-кнопка для
    вывода информации о найденных билетах
    :param message: Message
    :return: None
    """
    for history_entry in (
        History.select()
        .where(History.user == Users.get(Users.nickname == message.chat.username))
        .limit(10)
        .order_by(History.date_time.desc())
    ):
        history_entry_info = (
            f"Команда: \\{history_entry.command};\n"
            f"Запрос: {history_entry.request_info};\n"
            f"Дата и время запроса: {history_entry.date_time}"
        )
        entry_date_time = str(history_entry.date_time)
        bot.send_message(
            message.from_user.id,
            history_entry_info,
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    text="вывести результат поиска", callback_data=entry_date_time
                )
            ),
        )


def show_tickets(message: Message, entry_date_time: str):
    """
    Метод, который выводит информацию о найденных билетах при нажатии на инлайн-кнопку под сообщением с запросом
    :param message: Message
    :param entry_date_time: callback_data из ф-ии show_request_history - дата и время ввода команды
    :return: None
    """
    for history_entry in (
        History.select()
        .where(History.user == Users.get(Users.nickname == message.chat.username))
        .order_by(History.date_time.desc())
    ):
        for one_ticket in TicketsInfo.select().where(
            (TicketsInfo.request_id == history_entry.id)
            & (entry_date_time == str(history_entry.date_time))
        ):
            if one_ticket.ticket_info != "Билеты по данному запросу не найдены.":
                one_ticket_info = one_ticket.ticket_info
                one_ticket_link = one_ticket.ticket_link

                bot.send_message(
                    message.chat.id,
                    one_ticket_info,
                    reply_markup=make_url_button(one_ticket_link),
                )
            else:
                bot.send_message(message.chat.id, one_ticket.ticket_info)
