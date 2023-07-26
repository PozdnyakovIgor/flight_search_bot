"""
Айдишник города можно получить через /locations/v3/search по ключу в ответе sr -> 0,1,2,... -> cityId
Прокидываем полученный айди в запрос для поиска цен /properties/v2/list. Список всех варинатов находится по ключу data -> propertySearch -> properties.
TODO Отрезать заданное количество вариантов
    название отеля ['data']['propertySearch']['properties'][0]['name']
    адрес (скорей всего получить вместе с фотками)
    цена за ночь ['data']['propertySearch']['properties'][0]['price']['options'][0]['strikeOut']['formatted']
    цена за весь период ['data']['propertySearch']['properties'][0]['price']['displayMessages'][1]['lineItems'][0]['value']
    фотки: в данном запросе только фотка на заставку ['data']['propertySearch']['properties'][0]['propertyImage']['image']['url'], возможно отдельный запрос на большее кол-во фоток
    ссылка на отель: спросить у куратора как формируется ссылка, в резальте не нашел
    подставлять через дейттайм заезд и выезд в пейлоад
    расстояние до центра (в милях) (предположительно) ['data']['propertySearch']['properties'][0]['destinationInfo']['distanceFromDestination']['value']
"""

import requests
from typing import Tuple


class HotelsAPI:
    host = 'hotels4.p.rapidapi.com'
    key = 'cac61176admshdc45e796d9ea71dp12c786jsn576dc567ee3d'

    def __init__(self):
        # self.client = requests.Session()
        self.default_headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": self.host
        }

    def build_url(self, endpoint: str):
        return 'https://' + self.host + '/' + endpoint

    # TODO Возможно обойдется без метода начала сессии
    # def start_session(self):
    #     pass

    def get_low_price(self, location: str, hotels_amount: int, show_photos: bool, photos_amount: int = None):
        """
        После ввода команды у пользователя запрашивается:
        1. Город, где будет проводиться поиск.
        2. Количество отелей, которые необходимо вывести в результате (не больше
        заранее определённого максимума).
        3. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
            a. При положительном ответе пользователь также вводит количество необходимых фотографий (не больше заранее определённого максимума)
        """
        endpoint = 'properties/v2/list'
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            # "destination": {"regionId": "6054439"},
            "destination": {"regionId": "2621"},
            "checkInDate": {
                "day": 10,
                "month": 6,
                "year": 2023
            },
            "checkOutDate": {
                "day": 21,
                "month": 6,
                "year": 2023
            },
            "rooms": [
                {
                    "adults": 1,
                    "children": []
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": 200,
            "sort": "PRICE_LOW_TO_HIGH",
            "filters": {"price": {
                "max": 500,
                "min": 10
            }}
        }

        headers = self.default_headers.copy()
        headers.update({"content-type": "application/json"})

        res = requests.request("POST", url=self.build_url(endpoint), json=payload,
                               headers=headers)
        return res

    def get_high_price(self, location: str, hotels_amount: int, show_photos: bool, photos_amount: int):
        """
        После ввода команды у пользователя запрашивается:
        1. Город, где будет проводиться поиск.
        2. Количество отелей, которые необходимо вывести в результате (не больше
        заранее определённого максимума).
        3. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
            a. При положительном ответе пользователь также вводит количество необходимых фотографий (не больше заранее определённого максимума)
        """
        pass

    def get_best_deal(self,
                      location: str, price_range: Tuple[int], distance_range: Tuple[int | float],
                      hotels_amount: int, show_photos: bool, photos_amount: int):
        """
        После ввода команды у пользователя запрашивается:
        1. Город, где будет проводиться поиск.
        2. Количество отелей, которые необходимо вывести в результате (не больше
        заранее определённого максимума).
        3. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
            a. При положительном ответе пользователь также вводит количество необходимых фотографий (не больше заранее определённого максимума)
        """
        pass


if __name__ == '__main__':
    hotels_api = HotelsAPI()
    res = hotels_api.get_low_price(location='2621', hotels_amount=5, show_photos=False)
    print(res)
