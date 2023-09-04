import requests

from config_data import TRAVELPAYOUTS_BASE_URL
from typing import Optional


def get_city_iata_code(city_name: str) -> Optional[str]:
    """
    Метод для определения IATA-кода города
    :param city_name: название города
    :return: city_iata_code
    :rtype: Optional[str]
    """

    url = f"{TRAVELPAYOUTS_BASE_URL}{city_name}"
    response = requests.get(url=url)

    if response.status_code == 200:
        for city_data in response.json():
            if city_data["name"] == city_name:
                city_iata_code = city_data["code"]
                return city_iata_code
    return None


def get_city_name_from_iata_code(city_iata_code: str) -> str:
    """
    Метод для определения города по IATA-коду
    :param city_iata_code: IATA-код города
    :return: city_name
    :rtype: str
    """

    url = f"{TRAVELPAYOUTS_BASE_URL}{city_iata_code}"
    response = requests.get(url=url)

    for city_data in response.json():
        city_name = city_data["name"]
        return city_name


def get_airport_name_from_iata_code(airport_iata_code: str) -> str:
    """
    Метод для определения аэропорта по IATA-коду
    :param airport_iata_code: IATA-код аэропорта
    :return: airport_name
    :rtype: str
    """

    url = f"{TRAVELPAYOUTS_BASE_URL}{airport_iata_code}"
    response = requests.get(url=url)

    for airport_data in response.json():
        if airport_data["type"] == "city" and airport_data["main_airport_name"] is not None:
            airport_name = airport_data["main_airport_name"]
        else:
            airport_name = airport_data["name"]

        return airport_name
