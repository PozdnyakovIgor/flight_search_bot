import json
import requests

from config_data import AVIASALES_API_TOKEN, AVIASALES_BASE_URL
from typing import Optional

from api_engine.api_travelpayouts_engine import get_city_name_from_iata_code, get_airport_name_from_iata_code

from utils.check_date import format_date


def build_url_certain_dates(origin: str, destination: str,
                            departure_at: str = None, return_at: str = None,
                            one_way: bool = True, direct: bool = False,
                            limit: int = 3, sorting: str = 'price'):

    # Базовый запрос, в который включены неизменяемые параметры
    url = f'{AVIASALES_BASE_URL}v3/prices_for_dates?origin={origin}' \
          f'&destination={destination}&unique=false&cy=rub&page=1' \
          f'&token={AVIASALES_API_TOKEN}'

    # Расширяем запрос в зависимости от аргументов
    if departure_at:
        url += f'&departure_at={departure_at}'
    if return_at:
        url += f'&return_at={return_at}'
    if one_way:
        url += f'&one_way={one_way}'
    if direct:
        url += f'&direct={direct}'
    if limit:
        url += f'&limit={limit}'
    if sorting:
        url += f'&sorting={sorting}'

    return url


def send_request(origin: str, destination: str,
                 departure_at: str = None, return_at: str = None, limit: int = None,
                 save_to_file: Optional[str] = '../response_example.json'):
    response = requests.get(
        url=build_url_certain_dates(
            origin=origin,
            destination=destination,
            departure_at=departure_at,
            return_at=return_at,
            limit=limit
        ))

    with open('response_example.json', 'w', encoding='utf-8') as file:
        json.dump(response.json(), file, indent=4)

    return response.json()


def pretty_response(response):
    tickets = ''

    if len(response['data']):
        response = response['data']
        for ticket in response:
            tickets += (f'Город отправления: {get_city_name_from_iata_code(ticket["origin"])} ({ticket["origin"]})\n'
                        f'Аэропорт отправления: {get_airport_name_from_iata_code(ticket["origin_airport"])} ({ticket["origin_airport"]})\n'
                        f'Город прибытия: {get_city_name_from_iata_code(ticket["destination"])} ({ticket["destination"]})\n'
                        f'Аэропорт прибытия: {get_airport_name_from_iata_code(ticket["destination_airport"])} ({ticket["destination_airport"]})\n'
                        f'Дата и время вылета из пункта отправления: {format_date(ticket["departure_at"])}\n'
                        f'Дата и время обратного рейса: {format_date(ticket["return_at"])}\n'
                        f'Цена (руб): {ticket["price"]}\n'
                        f'Ссылка на билет: https://www.aviasales.ru' + ticket["link"] + '\n\n')
    else:
        tickets = 'В кэше не найдено таких билетов :('

    return tickets
