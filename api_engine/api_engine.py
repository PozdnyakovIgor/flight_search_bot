import json
import requests

from config_data import AVIASALES_API_TOKEN, AVIASALES_BASE_URL


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




def print_response(data):
    for i_data in data["data"]:
        print(f'Город отправления: {i_data["origin"]}\n'
              f'Аэропорт отправления: {i_data["origin_airport"]}\n'
              f'Город прибытия: {i_data["destination"]}\n'
              f'Аэропорт прибытия: {i_data["destination_airport"]}\n'
              f'Дата и время вылета из пункта отправления: {i_data["departure_at"]}\n'
              f'Дата и время обратного рейса: {i_data["return_at"]}\n'
              f'Цена (руб): {i_data["price"]}\n'
              f'Количество пересадок на пути "туда": {i_data["transfers"]}\n'
              f'Количество пересадок на пути "обратно": {i_data["return_transfers"]}\n'
              f'Общая продолжительность полета туда-обратно (мин): {i_data["duration"]}\n'
              f'Продолжительность перелёта до места назначения (мин): {i_data["duration_to"]}\n'
              f'Продолжительность перелёта обратно в минутах (мин): {i_data["duration_back"]}\n'
              f'Ссылка на билет: https://www.aviasales.ru' + i_data["link"] + '\n\n')


# origin = input('Введите пункт отправления: ')
# destination = input('Введите пункт назначения: ')
# departure_at = input('Введите дату вылета из пункта отправления: ')
# return_at = input('Введите дату возвращения: ')
#
# response = requests.get(url=build_url(
#     origin='MOW',
#     destination="GSV",
#     departure_at='2023-08-10',
#     return_at='2023-08-14'
# ))

# with open('../response_example.json', 'w', encoding='utf-8') as file:
#     json.dump(response.json(), file, indent=4)
