from datetime import datetime

from database import add_request_search_to_history
from database.db_core import add_tickets_info
from loader import bot
from states.top_cheapest_tickets_states import CheapestTicketsInfoState
from telebot.types import Message
from api_engine.api_aviasales_engine import (
    send_request_top_cheapest_tickets,
    one_ticket_pretty,
)
from api_engine.api_travelpayouts_engine import (
    get_city_iata_code,
    get_city_name_from_iata_code,
)
from utils.check_date import check_date, format_date

from keyboards.inline.departure_at_yes_no_keyboard import departure_at_yes_no_markup
from keyboards.inline.return_at_yes_no_keyboard import return_at_yes_no_markup
from keyboards.inline.url_button import make_url_button


@bot.message_handler(state="*", commands=["top_cheapest_tickets"])
def top_cheapest_tickets(message: Message) -> None:
    """
    Команда для поиска самых дешевых билетов из заданного города. Можно указать даты вылета и/или прилета.
    Здесь задается состояние origin
    :param message: Message
    :return: None
    """
 
    bot.set_state(
        message.from_user.id, CheapestTicketsInfoState.origin, message.chat.id
    )
    bot.send_message(
        message.from_user.id,
        f"Подскажите, из какого города будем искать самые дешевые авиабилеты?",
    )


@bot.message_handler(state=CheapestTicketsInfoState.origin)
def get_origin(message: Message) -> None:
    """
    Метод, в котором обрабатываем сообщение с городом отправления, если состояние пользователя
    CheapestTicketsInfoState.origin. Также осуществляется проверка на корректность введенного города и появляется
    инлайн-клавиатура с вопросом хочет ли пользователь ввести дату вылета
    :param message: Message
    :return: None
    """
    if get_city_iata_code(message.text) is not None:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["origin"] = get_city_iata_code(message.text)
        departure_at_yes_no_markup(message)

    else:
        bot.send_message(
            message.from_user.id,
            "В данном городе нет аэропорта, либо Вы ввели название города с "
            "ошибкой. Введите название города:",
        )


@bot.message_handler(state=CheapestTicketsInfoState.departure_at)
def get_departure_at(message: Message) -> None:
    """
    Метод, в котором обрабатываем сообщение с датой вылета (если она была указана), если состояние пользователя
    CheapestTicketsInfoState.departure_at. Также осуществляется проверка на корректность введенной даты вылета и
    появляется инлайн-клавиатура с вопросом хочет ли пользователь ввести дату возвращения
    :param message: Message
    :return: None
    """
    if check_date(message.text):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["departure_at"] = message.text
        return_at_yes_no_markup(message)

    else:
        bot.send_message(
            message.from_user.id,
            "Проверьте правильность введенной даты отправления: формат даты должен быть "
            "YYYY-MM или YYYY-MM-DD, на прошедшие даты поиск не возможен.",
        )


@bot.message_handler(state=CheapestTicketsInfoState.return_at)
def get_return_at(message: Message) -> None:
    """
    Метод, в котором обрабатываем сообщение с датой прилета (если она была указана), если состояние пользователя
    CheapestTicketsInfoState.return_at. Также осуществляется проверка на корректность введенной даты возвращения и
    задается вопрос о кол-ве билетов в ответе.
    :param message: Message
    :return: None
    """
    if check_date(message.text):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            if (
                ticket_data["departure_at"] is not None
                and ticket_data["departure_at"] > message.text
            ):
                bot.send_message(
                    message.from_user.id,
                    "Дата возвращения не может быть раньше, чем дата отправления!",
                )
            else:
                ticket_data["return_at"] = message.text
                bot.send_message(
                    message.from_user.id, "Сколько вариантов показать? (не более 10)"
                )
                bot.set_state(
                    message.from_user.id,
                    CheapestTicketsInfoState.limit,
                    message.chat.id,
                )

    else:
        bot.send_message(
            message.from_user.id,
            "Проверьте правильность введенной даты возвращения: формат даты должен быть "
            "YYYY-MM или YYYY-MM-DD, на прошедшие даты поиск не возможен.",
        )


@bot.message_handler(state=CheapestTicketsInfoState.limit)
def get_limit(message: Message) -> None:
    """
    Метод, в котором обрабатываем сообщение с кол-ом билетов, необходимым для вывода, если состояние пользователя
    CheapestTicketsInfoState.limit, выдаем ответ и сбрасываем состояние.
    :param message:
    :return:
    """
    if message.text.isdigit() and 0 < int(message.text) <= 10:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["limit"] = message.text
        bot.send_message(
            message.from_user.id, "Отлично! Вся информация есть, ищу билеты..."
        )

        tickets = send_request_top_cheapest_tickets(
            ticket_data["origin"],
            ticket_data["departure_at"],
            ticket_data["return_at"],
            ticket_data["limit"],
        )

        last_history_request_id = add_request_search_to_history(
            nickname=message.chat.username,
            command="top_cheapest_tickets",
            user_request=f'{get_city_name_from_iata_code(ticket_data["origin"])}({ticket_data["origin"]}), '
            f'отправление: {ticket_data["departure_at"]}, '
            f'прибытие: {ticket_data["return_at"]}, кол-во: {ticket_data["limit"]}',
            date=datetime.now().replace(microsecond=0),
        )

        if len(tickets["data"]):
            tickets = tickets["data"]
            for ticket in tickets:  # прочитать про for-else
                bot.send_message(
                    message.chat.id,
                    one_ticket_pretty(ticket),
                    reply_markup=make_url_button(
                        f"https://www.aviasales.ru" f'{ticket["link"]}'
                    ),
                )
                if 'return_at' in ticket:
                    add_tickets_info(request_id=last_history_request_id,
                                     ticket_info=f'{get_city_name_from_iata_code(ticket["origin"])} ({ticket["origin"]}) -> '
                                                 f'{get_city_name_from_iata_code(ticket["destination"])} ({ticket["destination"]}),\n '
                                                 f'Дата и время отправления: {format_date(ticket["departure_at"])},\n'
                                                 f'Дата и время обратного рейса: {format_date(ticket["return_at"])},\n'
                                                 f'Цена: {ticket["price"]} руб.',
                                     ticket_link=f'https://www.aviasales.ru{ticket["link"]}',)
                else:
                    add_tickets_info(request_id=last_history_request_id,
                                     ticket_info=f'{get_city_name_from_iata_code(ticket["origin"])} ({ticket["origin"]}) -> '
                                                 f'{get_city_name_from_iata_code(ticket["destination"])} ({ticket["destination"]}),\n '
                                                 f'Дата и время отправления: {format_date(ticket["departure_at"])},\n'
                                                 f'Цена: {ticket["price"]} руб.',
                                     ticket_link=f'https://www.aviasales.ru{ticket["link"]}',)
        else:
            add_tickets_info(
                request_id=last_history_request_id,
                ticket_info="Билеты по данному запросу не найдены.",
                ticket_link="Отсутствует.",
            )
            bot.send_message(message.chat.id, "В кэше не найдено таких билетов :(")

        bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(
            message.from_user.id,
            "Проверьте правильность введенного количества вариантов, должно быть "
            "не более 10.",
        )
