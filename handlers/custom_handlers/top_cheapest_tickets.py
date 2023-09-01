from loader import bot
from states.top_cheapest_tickets_states import CheapestTicketsInfoState
from telebot.types import Message
from api_engine.api_aviasales_engine import (
    send_request_top_cheapest_tickets,
    pretty_response_top_cheapest_tickets,
    one_ticket_pretty,
)
from api_engine.api_travelpayouts_engine import (
    get_city_iata_code,
    get_city_name_from_iata_code,
    get_airport_name_from_iata_code,
)
from utils.check_date import check_date, format_date

from keyboards.inline.departure_at_yes_no_keyboard import departure_at_yes_no_markup
from keyboards.inline.return_at_yes_no_keyboard import return_at_yes_no_markup
from keyboards.inline.url_button import make_url_button

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


# TODO попробовать сделать каждый билет в отдельном сообщении, а ссылку сделать инлайн-кнопкой + увел-ть кол-во до 10
@bot.message_handler(state=CheapestTicketsInfoState.limit)
def get_limit(message: Message) -> None:
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

        else:
            bot.send_message(message.chat.id, "В кэше не найдено таких билетов :(")

    else:
        bot.send_message(
            message.from_user.id,
            "Проверьте правильность введенного количества вариантов, должно быть "
            "не более 10.",
        )


# tickets = send_request_top_cheapest_tickets(origin="GSV", limit=10)
# data = pretty_response_top_cheapest_tickets(tickets)
#
# with open("top_cheapest_tickets.json", "w", encoding="utf-8") as file:
#     json.dump(tickets, file, indent=4, ensure_ascii=False)
#
#
# with open("top_cheapest_tickets.txt", "w", encoding="utf-8") as file:
#     file.write(data)
