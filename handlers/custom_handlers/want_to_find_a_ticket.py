from datetime import datetime

from database import add_request_search_to_history
from database.db_core import add_tickets_info, History
from loader import bot
from states.ticket_information import TicketInfoState
from telebot.types import Message
from api_engine.api_aviasales_engine import send_request, pretty_response
from api_engine.api_travelpayouts_engine import (
    get_city_iata_code,
    get_city_name_from_iata_code,
    get_airport_name_from_iata_code,
)
from utils.check_date import check_date, format_date


@bot.message_handler(state="*", commands=["want_ticket"])
def want_to_find_a_ticket(message: Message) -> None:
    """
    Команда для поиска билетов с заданными городами отправления и прибытия, с заданными датами отправления и прибытия.
    Здесь задается состояние origin

    """
    bot.set_state(message.from_user.id, TicketInfoState.origin, message.chat.id)
    bot.send_message(
        message.from_user.id, f"Отлично! Укажите, откуда Вы бы хотели полететь?"
    )


@bot.message_handler(state=TicketInfoState.origin)
def get_origin(message: Message) -> None:
    """
    Метод, в котором обрабатываем сообщение с городом отправления, если состояние пользователя TicketInfoState.origin.
    Также осуществляется проверка на корректность введенного города

    """

    if get_city_iata_code(message.text) is not None:
        bot.send_message(message.from_user.id, "Теперь введите город назначения:")
        bot.set_state(
            message.from_user.id, TicketInfoState.destination, message.chat.id
        )

        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["origin"] = get_city_iata_code(message.text)

    else:
        bot.send_message(
            message.from_user.id,
            "В данном городе нет аэропорта, либо Вы ввели название города с "
            "ошибкой. Введите название города:",
        )


@bot.message_handler(state=TicketInfoState.destination)
def get_destination(message: Message) -> None:
    """
    Метод, в котором обрабатываем сообщение с городом прибытия, если состояние пользователя TicketInfoState.destination
    Также осуществляется проверка на корректность введенного города
    """

    if get_city_iata_code(message.text) is not None:
        bot.send_message(
            message.from_user.id,
            "Когда хотите полететь? Введите дату в формате YYYY-MM или YYYY-MM-DD",
        )
        bot.set_state(
            message.from_user.id, TicketInfoState.departure_at, message.chat.id
        )

        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["destination"] = get_city_iata_code(message.text)

    else:
        bot.send_message(
            message.from_user.id,
            "В данном городе нет аэропорта, либо Вы ввели название города с "
            "ошибкой. Введите название города:",
        )


@bot.message_handler(state=TicketInfoState.departure_at)
def get_departure_at(message: Message) -> None:
    """
    Метод, в котором обрабатываем сообщение с датой отправления, если состояние пользователя TicketInfoState.departure_at
    Также осуществляется проверка на корректность введенной даты
    """

    if check_date(message.text):
        bot.send_message(
            message.from_user.id,
            "Когда хотите вернуться? Введите дату в формате YYYY-MM или YYYY-MM-DD",
        )
        bot.set_state(message.from_user.id, TicketInfoState.return_at, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["departure_at"] = message.text
    else:
        bot.send_message(
            message.from_user.id,
            "Проверьте правильность введенной даты: формат даты должен быть "
            "YYYY-MM или YYYY-MM-DD, на прошедшие даты поиск не возможен.",
        )


@bot.message_handler(state=TicketInfoState.return_at)
def get_return_at(message: Message) -> None:
    """
    Метод, в котором обрабатываем сообщение с датой прибытия, если состояние пользователя TicketInfoState.return_at
    Также осуществляется проверка на корректность введенной даты
    """

    if check_date(message.text):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            if ticket_data["departure_at"] > message.text:
                bot.send_message(
                    message.from_user.id,
                    "Дата возвращения не может быть раньше, чем дата отправления!",
                )
            else:
                ticket_data["return_at"] = message.text
                bot.send_message(
                    message.from_user.id, "Сколько вариантов показать (не более 5) ?"
                )
                bot.set_state(
                    message.from_user.id, TicketInfoState.limit, message.chat.id
                )

    else:
        bot.send_message(
            message.from_user.id,
            "Проверьте правильность введенной даты: формат даты должен быть "
            "YYYY-MM или YYYY-MM-DD, на прошедшие даты поиск не возможен.",
        )


@bot.message_handler(state=TicketInfoState.limit)
def get_limit(message: Message) -> None:
    """
    Метод, в котором обрабатываем сообщение с числом вариантов, выдаем ответ и сбрасываем состояние, если состояние
    пользователя TicketInfoState.limit

    """

    if message.text.isdigit() and 0 < int(message.text) <= 5:
        bot.send_message(
            message.from_user.id, "Отлично! Вся информация есть, ищу билеты..."
        )

        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["limit"] = message.text

        tickets = send_request(
            ticket_data["origin"],
            ticket_data["destination"],
            ticket_data["departure_at"],
            ticket_data["return_at"],
            ticket_data["limit"],
        )

        last_history_request_id = add_request_search_to_history(
            nickname=message.chat.username,
            command="want_ticket",
            user_request=f'{get_city_name_from_iata_code(ticket_data["origin"])}({ticket_data["origin"]}) -> '
                         f'{get_city_name_from_iata_code(ticket_data["destination"])}({ticket_data["destination"]}), '
            f'отправление: {ticket_data["departure_at"]}, '
            f'прибытие: {ticket_data["return_at"]}, кол-во: {ticket_data["limit"]}',
            date=datetime.now().replace(microsecond=0),
        )

        bot.send_message(message.chat.id, pretty_response(tickets))

        if len(tickets["data"]):
            for ticket in tickets["data"]:
                add_tickets_info(
                    request_id=last_history_request_id,
                    ticket_info=f'{get_city_name_from_iata_code(ticket["origin"])} ({ticket["origin"]}) -> '
                    f'{get_city_name_from_iata_code(ticket["destination"])} ({ticket["destination"]}),\n '
                    f'Дата и время отправления: {format_date(ticket["departure_at"])},\n'
                    f'Дата и время обратного рейса: {format_date(ticket["return_at"])},\n'
                    f'Цена: {ticket["price"]} руб.',
                    ticket_link=f'https://www.aviasales.ru{ticket["link"]}',
                )
        else:
            add_tickets_info(
                request_id=last_history_request_id,
                ticket_info="Билеты по данному запросу не найдены.",
                ticket_link="Отсутствует.",
            )

        bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(
            message.from_user.id,
            "Проверьте правильность введенного количества вариантов, должно быть "
            "не более 5.",
        )
