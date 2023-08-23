import json
import requests

from config_data import TRAVELPAYOUTS_BASE_URL


# TODO попробовать оптимизировать получение response в 3ех функциях
def get_city_iata_code(city_name):
    url = f'{TRAVELPAYOUTS_BASE_URL}{city_name}'
    response = requests.get(url=url)
    # print(response)
    # with open('city_and_airport_iata_code.json', 'w', encoding='utf-8') as file:
    #     json.dump(response.json(), file, indent=4, ensure_ascii=False)
    #     file.write('\n')
    if response.status_code == 200:
        for city_data in response.json():
            if city_data['name'] == city_name:
                city_iata_code = city_data['code']
                return city_iata_code
    return None


def get_city_name_from_iata_code(city_iata_code):
    url = f'{TRAVELPAYOUTS_BASE_URL}{city_iata_code}'
    response = requests.get(url=url)
    # with open('get_name.json', 'a', encoding='utf-8') as file:
    #     json.dump(response.json(), file, indent=4, ensure_ascii=False)
    #     file.write('\n')

    for city_data in response.json():
        city_name = city_data['name']
        return city_name
    # return city_data['main_airport_name']


def get_airport_name_from_iata_code(airport_iata_code):
    url = f'{TRAVELPAYOUTS_BASE_URL}{airport_iata_code}'
    response = requests.get(url=url)
    # with open('get_name.json', 'a', encoding='utf-8') as file:
    #     json.dump(response.json(), file, indent=4, ensure_ascii=False)
    #     file.write('\n')

    for airport_data in response.json():
        if airport_data['type'] == 'city':
            airport_name = airport_data['main_airport_name']
        else:
            airport_name = airport_data['name']

        return airport_name

    # return city_data['main_airport_name']



# print(get_city_name_from_iata_code('LED'))
# print(get_city_name_from_iata_code('LED'))
# print(get_city_iata_code('1'))
# print(get_city_iata_code('Санкт-Петербург'))
# print(get_city_iata_code('Сергиев Посад'))
# print(get_city_iata_code('Внуково'))
# print(get_city_iata_code('Гагарин'))
# print(get_city_iata_code('Внуково'))
