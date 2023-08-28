# можно указать страну в следующих методах:
# 1) Цены на авиабилеты за период http://api.travelpayouts.com/v2/prices/latest
# 2) Цены на авиабилеты по альтернативным направлениям http://api.travelpayouts.com/v2/prices/nearest-places-matrix

# можно не указывать пункт прибытия
# 1) Самые дешевые авиабилеты http://api.travelpayouts.com/v1/prices/cheap
# 2) Билет без пересадок http://api.travelpayouts.com/v1/prices/direct
# 3) Самые дешевые авиабилеты на определённые даты https://api.travelpayouts.com/aviasales/v3/prices_for_dates

from config_data import AVIASALES_API_TOKEN
import requests

url = (f'https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin=MOW&departure_at=2023-09'
       '&unique=true&sorting=price&direct=false&cy=rub&limit=10&page=1&one_way=true&token'
       f'={AVIASALES_API_TOKEN}')

response = requests.get(url=url)

# TODO сохранить в файл дляя наглядности
with open('top_cheapest_tickets.json', 'w', encoding='utf-8') as file:
    pass

print(response.json())
