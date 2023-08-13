import json
import requests

from config_data.config import AVIASALES_API_TOKEN


# from travelpayouts import Client
# import stun


# current_ip = stun.get_ip_info()[1]

# aviasales_client = Client(AVIASALES_API_TOKEN, '468793')
# print(aviasales_client.whereami(current_ip))


# TODO  можно поставить библу, которая переводит координаты в город (скорей всего так делать не буду)
# print(aviasales_client.search(segments={'origin': 'PAR', 'destination': 'BER', 'date': '2023-10-21'},
#                               passengers={'adults': '2'},
#                               host='https://t.me/EASY_BREEZE_BOT',
#                               user_ip=current_ip))


# сделал переменную AVIASALES_BASE_URL в config_data.config: https://api.travelpayouts.com/aviasales/
def build_url(origin, destination, departure_at, return_at, token=AVIASALES_API_TOKEN):
    url = f'https://api.travelpayouts.com/aviasales/v3/prices_for_dates?' \
          f'origin={origin}&' \
          f'destination={destination}&' \
          f'departure_at={departure_at}&' \
          f'return_at={return_at}&unique=false&sorting=price&direct=false&cy=rub&limit=10&page=1&one_way=true&' \
          f'token={token}'
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
        # origin = f'Город отправления: {i_data["origin"]}\n'
        # origin_airport = f'Аэропорт отправления: {i_data["origin_airport"]\n}'
        # destination = f'Город прибытия: {i_data["destination"]}\n'
        # destination_airport = f'Аэропорт прибытия: {i_data["destination_airport"]}'
        # departure_at = f'Дата вылета из пункта отправления: {i_data["departure_at"]}\n'
        # return_at = f'Дата возвращения: {i_data["return_at"]}\n'
        # price = f'Цена (руб): {i_data["price"]}\n'
        # transfers = f'Количество пересадок на пути "туда": {i_data["transfers"]}\n'
        # return_transfers = f'Количество пересадок на пути "обратно": {i_data["return_transfers"]}\n'
        # duration = f'Общая продолжительность полета туда-обратно (мин): {i_data["duration"]}\n'
        # duration_to = f'Продолжительность перелёта до места назначения (мин): {i_data["duration_to"]}\n'
        # duration_back = f'Продолжительность перелёта обратно в минутах (мин): {i_data["duration_back"]}\n'
        # link = 'https://www.aviasales.ru' + f'{i_data["link"]}\n\n'


#  Поменял значение limit (было 30)

# origin = input('Введите пункт отправления: ')
# destination = input('Введите пункт назначения: ')
# departure_at = input('Введите дату вылета из пункта отправления: ')
# return_at = input('Введите дату возвращения: ')

response = requests.get(url=build_url(
    origin='MOW',
    destination="GSV",
    departure_at='2023-08-10',
    return_at='2023-08-14'
))
# При таких датах отправления и прибытия ничего не находит, хотя на авиасейлз билеты есть. Находит билеты, если 2023-10-11 и 2023-11-01, аэропорт прибытия LED


print(response.json())
data = json.loads(response.text)
print_response(data)

with open('../../response_example.json', 'w', encoding='utf-8') as file:
    json.dump(response.json(), file, indent=4)

# print(response.json())
# TODO придумать 3-4 метода по аналогии с ТЗ, вынести основные методы в отдельные файлы,
#  подумать про обязательные\необязательные параметры, аргументы и тд


# url_2 = 'http://api.travelpayouts.com/v2/prices/nearest-places-matrix?currency=rub&origin=LED&destination=HKT
# &show_to_affiliates=true&distance=1000&limit=2&token=019dc8a46e98bf61e6be2ff530bc09d0' response_2 = requests.get(
# url_2) with open('resp_ex_2.json', 'w', encoding='utf-8') as file: json.dump(response_2.json(), file, indent=4)

# url_3 = 'https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin=MOW&departure_at=2023-08&return_at=2023
# -09&unique=false&sorting=price&direct=false&cy=rub&limit=30&page=1&one_way=true&token
# =019dc8a46e98bf61e6be2ff530bc09d0' response_3 = requests.get(url_3) with open('resp_ex_3.json', 'w',
# encoding='utf-8') as file: json.dump(response_3.json(), file, indent=4)
