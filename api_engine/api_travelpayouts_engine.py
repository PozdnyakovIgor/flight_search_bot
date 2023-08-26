import requests

from config_data import TRAVELPAYOUTS_BASE_URL


def get_city_iata_code(city_name):
    url = f'{TRAVELPAYOUTS_BASE_URL}{city_name}'
    response = requests.get(url=url)

    if response.status_code == 200:
        for city_data in response.json():
            if city_data['name'] == city_name:
                city_iata_code = city_data['code']
                return city_iata_code
    return None


def get_city_name_from_iata_code(city_iata_code):
    url = f'{TRAVELPAYOUTS_BASE_URL}{city_iata_code}'
    response = requests.get(url=url)

    for city_data in response.json():
        city_name = city_data['name']
        return city_name


def get_airport_name_from_iata_code(airport_iata_code):
    url = f'{TRAVELPAYOUTS_BASE_URL}{airport_iata_code}'
    response = requests.get(url=url)

    for airport_data in response.json():
        if airport_data['type'] == 'city':
            airport_name = airport_data['main_airport_name']
        else:
            airport_name = airport_data['name']

        return airport_name
