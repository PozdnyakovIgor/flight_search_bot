from datetime import datetime

from database import add_request_search_to_history
from database.db_core import add_tickets_info
from keyboards.inline.url_button import make_url_button
from loader import bot
from states.popular_directions_states import PopularDirectionsState
from telebot.types import Message, CallbackQuery
from api_engine import (
    get_city_iata_code,
    get_city_name_from_iata_code,
    get_airport_name_from_iata_code,
)
from api_engine.api_aviasales_engine import (
    send_request_popular_directions,
    get_popular_directions,
    send_request,
    one_ticket_pretty,
)
from keyboards.inline.popular_directions_keyboards.cities_keyboard import (
    show_cities_keyboard,
)
from keyboards.inline.popular_directions_keyboards.departure_at_yes_no_kb import (
    departure_at_yes_no_markup,
)
from keyboards.inline.popular_directions_keyboards.return_at_yes_no_kb import (
    return_at_yes_no_markup,
)
from utils.check_date import check_date, format_date


@bot.message_handler(state="*", commands=["popular_directions"])
def popular_directions(message: Message) -> None:
    """
    Команда для поиска популярных направлений из заданного города. При вводе города отправления появляется
    инлайн-клавиатура с названиями самых популярных городов прибытия. Выбираем город, указываем даты
    отправления/прибытия (по желанию) и получаем информацию о билетах. Здесь задается состояние origin.
    :param message: Message
    :return: None
    """

    bot.set_state(message.from_user.id, PopularDirectionsState.origin, message.chat.id)
    bot.send_message(
        message.from_user.id,
        f"Самые популярные направления из какого города Вам показать?",
    )


@bot.message_handler(state=PopularDirectionsState.origin)
def get_origin(message: Message) -> None:
    """
    Метод, в котором обрабатываем сообщение с городом отправления, если состояние пользователя
    PopularDirectionsState.origin. Также осуществляется проверка на корректность введенного города и появляется
    инлайн-клавиатура с названиями городов
    :param message: Message
    :return: None
    """
    if get_city_iata_code(message.text) is not None:
        bot.send_message(message.from_user.id, f"В работе...")
        city_iata_code = get_city_iata_code(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["origin"] = city_iata_code
        popular_directions_dict = get_popular_directions(
            send_request_popular_directions(origin=city_iata_code)
        )

        if popular_directions_dict is not None:
            show_cities_keyboard(
                message,
                popular_directions_dict,
            )
        else:
            bot.send_message(
                message.from_user.id,
                "Из данного города нет популярных направлений. Возможно, аэропорт "
                "этого города закрыт.",
            )
    else:
        bot.send_message(
            message.from_user.id,
            "В данном городе нет аэропорта, либо Вы ввели название города с "
            "ошибкой. Введите название города:",
        )


@bot.callback_query_handler(func=lambda call: len(call.data) == 3)
def city_iata_code_callback(call: CallbackQuery) -> None:
    """
    Пользователь выбрал город прибытия, нажав на кнопку.  Записываем IATA-код города, устанавливаем состояние
    PopularDirectionsState.destination и запрашиваем хочет ли он указать дату отправления.
    :param call: Получает IATA-код города
    :return: None
    """
    if call.data:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        with bot.retrieve_data(call.message.chat.id) as ticket_data:
            ticket_data["destination"] = call.data
            bot.send_message(
                call.message.chat.id,
                f"Выбран город прибытия: {get_city_name_from_iata_code(call.data)}",
            )
    bot.set_state(call.message.chat.id, PopularDirectionsState.destination)
    departure_at_yes_no_markup(call.message)


@bot.callback_query_handler(
    func=lambda call: call.data == "departure_yes" or call.data == "departure_no"
)
def enter_departure_at_callback(call: CallbackQuery) -> None:
    """
    Пользователь нажал кнопку "Да" или "Нет". В зависимости от ответа пользователь вводит дату отправления,
    либо получает инлайн-клавиатуру с предлложением ввести дату прибытия
    :param call: 'yes' or 'no'
    :return: None
    """

    if call.data == "departure_yes":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, PopularDirectionsState.departure_at)
        bot.send_message(
            call.message.chat.id,
            "Пожалуйста, введите дату отправления (в формате YYYY-MM или YYYY-MM-DD): ",
        )

    elif call.data == "departure_no":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        # bot.set_state(call.message.chat.id, PopularDirectionsState.departure_at)
        with bot.retrieve_data(call.message.chat.id) as ticket_data:
            ticket_data["departure_at"] = None
        return_at_yes_no_markup(call.message)


@bot.message_handler(state=PopularDirectionsState.departure_at)
def get_departure_at(message: Message) -> None:
    """
    Метод, в котором обрабатываем сообщение с датой вылета, если состояние PopularDirectionsState.departure_at,
    устанавливаем состояние PopularDirectionsState.return_at и выводим инлайн-клавиатуру с предложением ввести
    дату прилета
    :param message: Message
    :return: None
    """
    if check_date(message.text):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["departure_at"] = message.text
        bot.set_state(message.chat.id, PopularDirectionsState.return_at)
        return_at_yes_no_markup(message)

    else:
        bot.send_message(
            message.from_user.id,
            "Проверьте правильность введенной даты отправления: формат даты должен быть "
            "YYYY-MM или YYYY-MM-DD, на прошедшие даты поиск не возможен.",
        )


@bot.callback_query_handler(
    func=lambda call: call.data == "return_yes" or call.data == "return_no"
)
def enter_return_at_callback(call: CallbackQuery) -> None:
    """
    Пользователь нажал кнопку "Да" или "Нет". В зависимости от ответа пользователь вводит дату отправления, либо вводит
    число билетов, которое необходимо показать
    :param call: CallbackQuery
    :return: None
    """
    if call.data == "return_yes":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, PopularDirectionsState.return_at)
        bot.send_message(
            call.message.chat.id,
            "Введите дату возвращения (в формате YYYY-MM или YYYY-MM-DD): ",
        )
    elif call.data == "return_no":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, PopularDirectionsState.limit)
        with bot.retrieve_data(call.message.chat.id) as ticket_data:
            ticket_data["return_at"] = None
        bot.send_message(
            call.message.chat.id, "Сколько вариантов Вам показать? (не более 10)"
        )


@bot.message_handler(state=PopularDirectionsState.return_at)
def get_return_at(message: Message) -> None:
    """
    Метод, в котором обрабатываем сообщение с датой прилета, если состояние PopularDirectionsState.return_at,
    запрашиваем кол-во билетов, необходимое для вывода и устанавливаем состояние PopularDirectionsState.limit
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
                    PopularDirectionsState.limit,
                    message.chat.id,
                )

    else:
        bot.send_message(
            message.from_user.id,
            "Проверьте правильность введенной даты возвращения: формат даты должен быть "
            "YYYY-MM или YYYY-MM-DD, на прошедшие даты поиск не возможен.",
        )


@bot.message_handler(state=PopularDirectionsState.limit)
def get_limit(message: Message) -> None:
    """
    Обрабатываем введенное пользователем кол-во билетов, если состояние PopularDirectionsState.limit,
    отправляем запрос, выводим ответ и сбрасываем состояние
    :param message:
    :return:
    """
    if message.text.isdigit() and 0 < int(message.text) <= 10:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["limit"] = message.text
            requested_tickets_number = ticket_data["limit"]
        bot.send_message(
            message.from_user.id, "Отлично! Вся информация есть, ищу билеты..."
        )

        tickets = send_request(
            ticket_data["origin"],
            ticket_data["destination"],
            ticket_data["departure_at"],
            ticket_data["return_at"],
            ticket_data["limit"],
        )
        if ticket_data["departure_at"] is None:
            ticket_data["departure_at"] = "не указано"
        if ticket_data["return_at"] is None:
            ticket_data["return_at"] = "не указано"

        last_history_request_id = add_request_search_to_history(
            nickname=message.chat.username,
            command="popular_directions",
            user_request=f'{get_city_name_from_iata_code(ticket_data["origin"])}({ticket_data["origin"]}) -> '
            f'{get_city_name_from_iata_code(ticket_data["destination"])}({ticket_data["destination"]}), '
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
                if "return_at" in ticket:
                    add_tickets_info(
                        request_id=last_history_request_id,
                        ticket_info=f'{get_city_name_from_iata_code(ticket["origin"])} '
                                    f'({ticket["origin"]}), '
                                    f'аэропорт {get_airport_name_from_iata_code(ticket["origin_airport"])} '
                                    f'({ticket["origin_airport"]}) -> '
                                    f'{get_city_name_from_iata_code(ticket["destination"])} '
                                    f'({ticket["destination"]}),'
                                    f'аэропорт {get_airport_name_from_iata_code(ticket["destination_airport"])}'
                                    f'({ticket["destination_airport"]})\n'
                                    f'Дата и время отправления: {format_date(ticket["departure_at"])},\n'
                                    f'Дата и время обратного рейса: {format_date(ticket["return_at"])},\n'
                                    f'Цена: {ticket["price"]} руб.',
                        ticket_link=f'https://www.aviasales.ru{ticket["link"]}',
                    )
                else:
                    add_tickets_info(
                        request_id=last_history_request_id,
                        ticket_info=f'{get_city_name_from_iata_code(ticket["origin"])} ({ticket["origin"]}), '
                                    f'аэропорт {get_airport_name_from_iata_code(ticket["origin_airport"])} '
                                    f'({ticket["origin_airport"]}) -> '
                                    f'{get_city_name_from_iata_code(ticket["destination"])} ({ticket["destination"]}), '
                                    f'аэропорт {get_airport_name_from_iata_code(ticket["destination_airport"])}'
                                    f'({ticket["destination_airport"]})\n'
                                    f'Дата и время отправления: {format_date(ticket["departure_at"])},\n'
                                    f'Цена: {ticket["price"]} руб.',
                        ticket_link=f'https://www.aviasales.ru{ticket["link"]}',
                    )
            if len(tickets) < int(requested_tickets_number):
                bot.send_message(
                    message.from_user.id,
                    f"К сожалению, количество найденных билетов оказалось меньше запрашиваемого :(",
                )

        else:
            bot.send_message(message.chat.id, "В кэше не оказалось таких билетов :(")

        bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(
            message.from_user.id,
            "Проверьте правильность введенного количества вариантов, должно быть "
            "не более 10.",
        )
