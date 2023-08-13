import json
import requests

from config_data import AVIASALES_API_TOKEN, AVIASALES_BASE_URL
from typing import Optional


def build_url_certain_dates(origin: str, destination: str,
                            departure_at: str = None, return_at: str = None,
                            one_way: bool = True, direct: bool = False,
                            limit: int = 10, sorting: str = 'price'):
    # Базовый запрос, в который включены неизменяемые параметры
    url = f'{AVIASALES_BASE_URL}v3/prices_for_dates?origin={origin}' \
          f'&destination={destination}&unique=false&cy=rub&page=1' \
          f'&token={AVIASALES_API_TOKEN}'

    # Разширяем запрос в зависимости от аргументов
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
                 departure_at: str = None, return_at: str = None,
                 save_to_file: Optional[str] = '../response_example.json'):
    response = requests.get(
        url=build_url_certain_dates(
            origin=origin,  # 'MOW',
            destination=destination,  # "GSV",
            departure_at=departure_at,  # '2023-08-10',
            return_at=return_at  # '2023-08-14'
        ))

    with open(save_to_file, 'w', encoding='utf-8') as file:
        json.dump(response.json(), file, indent=4)
        
    return response


def pretty_response(response):
    for ticket in response["data"]:
        print(f'Город отправления: {ticket["origin"]}\n'
              f'Аэропорт отправления: {ticket["origin_airport"]}\n'
              f'Город прибытия: {ticket["destination"]}\n'
              f'Аэропорт прибытия: {ticket["destination_airport"]}\n'
              f'Дата и время вылета из пункта отправления: {ticket["departure_at"]}\n'
              f'Дата и время обратного рейса: {ticket["return_at"]}\n'
              f'Цена (руб): {ticket["price"]}\n'
              f'Количество пересадок на пути "туда": {ticket["transfers"]}\n'
              f'Количество пересадок на пути "обратно": {ticket["return_transfers"]}\n'
              f'Общая продолжительность полета туда-обратно (мин): {ticket["duration"]}\n'
              f'Продолжительность перелёта до места назначения (мин): {ticket["duration_to"]}\n'
              f'Продолжительность перелёта обратно в минутах (мин): {ticket["duration_back"]}\n'
              f'Ссылка на билет: https://www.aviasales.ru' + ticket["link"] + '\n\n')


# origin = input('Введите пункт отправления: ')
# destination = input('Введите пункт назначения: ')
# departure_at = input('Введите дату вылета из пункта отправления: ')
# return_at = input('Введите дату возвращения: ')