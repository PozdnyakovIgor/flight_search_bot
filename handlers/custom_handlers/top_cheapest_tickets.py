from loader import bot
from states.top_cheapest_tickets_states import CheapestTicketsInfoState
from telebot.types import Message
from api_engine.api_aviasales_engine import (
    send_request_top_cheapest_tickets,
    pretty_response_top_cheapest_tickets,
)
from api_engine.api_travelpayouts_engine import get_city_iata_code
from utils.check_date import check_date

from keyboards.inline.yes_no_keyboard import yes_no_markup

import json
import requests

# tickets = send_request_top_cheapest_tickets(origin='MOW', departure_at='2023-09-01', return_at='2023-09-14', limit=10)
# tickets = send_request_top_cheapest_tickets(origin='MOW', departure_at='2023-09-01', limit=10)


@bot.message_handler(commands=["top_cheapest_tickets"])
def top_cheapest_tickets(message: Message) -> None:
    """
    Команда для поиска самых дешевых билетов из заданного города. Можно указать даты вылета и/или прилета.


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
    CheapestTicketsInfoState.origin. Также осуществляется проверка на корректность введенного города
    """
    if get_city_iata_code(message.text) is not None:
        bot.send_message(
            message.from_user.id,
            "Хотите указать дату отправления?",
            reply_markup=yes_no_markup(),
        )
        bot.set_state(
            message.from_user.id,
            CheapestTicketsInfoState.ask_departure,
            message.chat.id,
        )

        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["origin"] = get_city_iata_code(message.text)

    else:
        bot.send_message(
            message.from_user.id,
            "В данном городе нет аэропорта, либо Вы ввели название города с "
            "ошибкой. Введите название города:",
        )


@bot.callback_query_handler(func=lambda call: call.data == "yes")
@bot.message_handler(state=CheapestTicketsInfoState.ask_departure)
def set_state_departure_at(message: Message) -> None:
    bot.send_message(
        message.from_user.id,
        "Введите дату отправления (в формате YYYY-MM или YYYY-MM-DD): ",
    )
    bot.set_state(message.from_user.id, CheapestTicketsInfoState.ask_return)


@bot.message_handler(state=CheapestTicketsInfoState.ask_return)
def get_departure_at(message: Message) -> None:
    if check_date(message.text):
        bot.send_message(
            message.from_user.id,
            "Хотите указать дату возвращения?",
            reply_markup=yes_no_markup(),
        )
        # TODO надо разобраться со состояниями и call.data, при нажатии "да" бот спрашивает дату отправления,
        #  а не возвращения

        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["departure_at"] = message.text

    else:
        bot.send_message(
            message.from_user.id,
            "Проверьте правильность введенной даты: формат даты должен быть "
            "YYYY-MM или YYYY-MM-DD, на прошедшие даты поиск не возможен.",
        )


@bot.callback_query_handler(func=lambda call: call.data == "yes")
@bot.message_handler(state=CheapestTicketsInfoState.ask_return)
def set_state_return_at(message: Message) -> None:
    bot.send_message(
        message.from_user.id,
        "Когда хотите вернуться? (укажите дату в формате YYYY-MM или YYYY-MM-DD): ",
    )
    bot.set_state(message.from_user.id, CheapestTicketsInfoState.return_at)


# TODO добавить проверки, чтобы дата возвращения была позже даты вылета, обратить внимание, что дата возвращения или
#  вылета может быть не указана
@bot.message_handler(state=CheapestTicketsInfoState.return_at)
def get_return_at(message: Message) -> None:
    if check_date(message.text):
        bot.send_message(message.from_user.id, "Сколько вариантов показать?")
        bot.set_state(
            message.from_user.id, CheapestTicketsInfoState.limit, message.chat.id
        )

        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["return_at"] = message.text

    else:
        bot.send_message(
            message.from_user.id,
            "Проверьте правильность введенной даты: формат даты должен быть "
            "YYYY-MM или YYYY-MM-DD, на прошедшие даты поиск не возможен.",
        )


@bot.message_handler(state=CheapestTicketsInfoState.limit)
def get_limit(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(
            message.from_user.id, "Отлично! Вся информация есть, ищу билеты..."
        )

        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["limit"] = message.text

        tickets = send_request_top_cheapest_tickets(
            ticket_data["origin"],
            ticket_data["departure_at"],
            ticket_data["return_at"],
            ticket_data["limit"],
        )

        bot.send_message(message.chat.id, pretty_response_top_cheapest_tickets(tickets))
        bot.delete_state(message.from_user.id, message.chat.id)


# tickets = send_request_top_cheapest_tickets(origin="GSV", limit=10)
# data = pretty_response_top_cheapest_tickets(tickets)
#
# with open("top_cheapest_tickets.json", "w", encoding="utf-8") as file:
#     json.dump(tickets, file, indent=4, ensure_ascii=False)
#
#
# with open("top_cheapest_tickets.txt", "w", encoding="utf-8") as file:
#     file.write(data)
