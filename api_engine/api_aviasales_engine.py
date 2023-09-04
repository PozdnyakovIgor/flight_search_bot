import json
from typing import Any

import requests

from config_data import AVIASALES_API_TOKEN, AVIASALES_BASE_URL

from api_engine.api_travelpayouts_engine import (
    get_city_name_from_iata_code,
    get_airport_name_from_iata_code,
)

from utils.check_date import format_date


def build_url_certain_dates(
    origin: str,
    destination: str,
    departure_at: str = None,
    return_at: str = None,
    one_way: bool = True,
    direct: bool = False,
    limit: int = 3,
    sorting: str = "price",
) -> str:
    """
    Конструктор запроса для ф-ии want_ticket

    :param origin: город отправления
    :param destination: город назначения
    :param departure_at: дата вылета
    :param return_at: дата возвращения
    :param one_way: билет в одну сторону
    :param direct: рейсы без пересадок
    :param limit: количество записей в ответе
    :param sorting: сортировка билетов по цене/популярности маршрута
    :return: url
    :rtype: str
    """

    url = (
        f"{AVIASALES_BASE_URL}v3/prices_for_dates?origin={origin}"
        f"&destination={destination}&unique=false&cy=rub&page=1"
        f"&token={AVIASALES_API_TOKEN}"
    )

    if departure_at:
        url += f"&departure_at={departure_at}"
    if return_at:
        url += f"&return_at={return_at}"
    if one_way:
        url += f"&one_way={one_way}"
    if direct:
        url += f"&direct={direct}"
    if limit:
        url += f"&limit={limit}"
    if sorting:
        url += f"&sorting={sorting}"

    return url


def send_request(
    origin: str,
    destination: str,
    departure_at: str = None,
    return_at: str = None,
    limit: int = None,
) -> json:
    """
    Метод для отправки запроса и получения информации о билетах для ф-ии want_ticket

    :param origin: город отправления
    :param destination: город назначения
    :param departure_at: дата вылета
    :param return_at: дата возвращения
    :param limit: количество записей в ответе
    :return: response
    :rtype: json
    """
    response = requests.get(
        url=build_url_certain_dates(
            origin=origin,
            destination=destination,
            departure_at=departure_at,
            return_at=return_at,
            limit=limit,
        )
    )

    return response.json()


def pretty_response(response: json) -> str:
    """
    Конструктор ответа для вывода пользователю для функции want_ticket

    :param response: json-объект с информацией о билетах
    :return: tickets
    :rtype: str
    """

    tickets = ""

    if len(response["data"]):
        response = response["data"]
        for ticket in response:
            tickets += (
                f"Город отправления: "
                f'{get_city_name_from_iata_code(ticket["origin"])} ({ticket["origin"]})\n'
                f"Аэропорт отправления: "
                f'{get_airport_name_from_iata_code(ticket["origin_airport"])} ({ticket["origin_airport"]})\n'
                f"Город прибытия: "
                f'{get_city_name_from_iata_code(ticket["destination"])} ({ticket["destination"]})\n'
                f"Аэропорт прибытия: "
                f'{get_airport_name_from_iata_code(ticket["destination_airport"])} '
                f'({ticket["destination_airport"]})\n'
                f"Дата и время вылета из пункта отправления: "
                f'{format_date(ticket["departure_at"])}\n'
                f"Дата и время обратного рейса: "
                f'{format_date(ticket["return_at"])}\n'
                f'Цена (руб): {ticket["price"]}\n'
                f"Ссылка на билет: https://www.aviasales.ru" + ticket["link"] + "\n\n"
            )
    else:
        tickets = "В кэше не найдено таких билетов :("

    return tickets


def build_url_top_cheapest_tickets(
    origin: str, departure_at: str = None, return_at: str = None, limit: int = 5
) -> str:
    """
    Конструктор запроса для ф-ии top_cheapest_tickets
    :param origin: город отправления
    :param departure_at: дата отправления
    :param return_at: дата обратного рейса
    :param limit: кол-во записей в ответе
    :return: url
    :rtype: str
    """
    url = (
        f"{AVIASALES_BASE_URL}v3/prices_for_dates?origin={origin}"
        f"&unique=true&sorting=price&direct=false&cy=rub&page=1"
        f"&one_way=true&token={AVIASALES_API_TOKEN}"
    )

    if departure_at:
        url += f"&departure_at={departure_at}"
    if return_at:
        url += f"&return_at={return_at}"
    if limit:
        url += f"&limit={limit}"

    return url


def send_request_top_cheapest_tickets(
    origin: str, departure_at: str = None, return_at: str = None, limit: int = 5
) -> json:
    """
    Метод для отправки запроса и получения информации о билетах для ф-ии top_cheapest_tickets
    :param origin: город отправления
    :param departure_at: дата отправления
    :param return_at: дата обратного рейса
    :param limit: кол-во записей в ответе
    :return: response
    :rtype: json
    """
    response = requests.get(
        url=build_url_top_cheapest_tickets(
            origin=origin, departure_at=departure_at, return_at=return_at, limit=limit
        )
    )

    return response.json()


def one_ticket_pretty(ticket):
    """
    Конструктор ответа (для одного билета) для вывода пользователю функции top_cheapest_tickets
    :param ticket: словарь с информацией о билете
    :return: one_ticket
    :rtype: str
    """

    one_ticket = ""
    one_ticket += (
        f"Город отправления: "
        f'{get_city_name_from_iata_code(ticket["origin"])} ({ticket["origin"]})\n'
        f"Аэропорт отправления: "
        f'{get_airport_name_from_iata_code(ticket["origin_airport"])} ({ticket["origin_airport"]})\n'
        f"Город прибытия: "
        f'{get_city_name_from_iata_code(ticket["destination"])} ({ticket["destination"]})\n'
        f"Аэропорт прибытия: "
        f'{get_airport_name_from_iata_code(ticket["destination_airport"])} '
        f'({ticket["destination_airport"]})\n'
        f"Дата и время вылета из пункта отправления: "
        f'{format_date(ticket["departure_at"])}\n'
    )
    if "return_at" in ticket:
        one_ticket += (
            f"Дата и время обратного рейса: " f'{format_date(ticket["return_at"])}\n'
        )
    one_ticket += f'Цена (руб): {ticket["price"]}\n'
    return one_ticket


def build_url_popular_directions(origin: str) -> str:
    """
    Конструктор запроса для функции popular_directions
    :param origin: город отправления
    :return: url
    :rtype: str
    """
    url = f"http://api.travelpayouts.com/v1/city-directions?origin={origin}&currency=rub&token={AVIASALES_API_TOKEN}"
    return url


def send_request_popular_directions(origin: str) -> json:
    """
    Метод для отправки запроса и получения информации о популярных направлениях из города для ф-ии popular_directions
    :param origin: город отправления
    :return: response
    :rtype: json
    """
    response = requests.get(url=build_url_popular_directions(origin)).json()
    return response


# TODO взять города из response. Подумать, что возвращать, если выбран, например, закрытый аэропорт
def get_popular_directions(response: json) -> Any:
    if len(response["data"]):
        cities = list()
        response = response["data"]
        for city in response:
            cities.append(city)

    else:
        tickets = "Из данного города нет популярных направлений. Возможно, аэропорт этого города закрыт."
