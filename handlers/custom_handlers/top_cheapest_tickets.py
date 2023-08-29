# можно указать страну в следующих методах:
# 1) Цены на авиабилеты за период http://api.travelpayouts.com/v2/prices/latest
# 2) Цены на авиабилеты по альтернативным направлениям http://api.travelpayouts.com/v2/prices/nearest-places-matrix


# можно не указывать пункт прибытия
# 1) Самые дешевые авиабилеты http://api.travelpayouts.com/v1/prices/cheap
# 2) Билет без пересадок http://api.travelpayouts.com/v1/prices/direct
# 3) Самые дешевые авиабилеты на определённые даты https://api.travelpayouts.com/aviasales/v3/prices_for_dates

import json
from config_data import AVIASALES_API_TOKEN
import requests
from api_engine.api_aviasales_engine import send_request_top_cheapest_tickets, pretty_response_top_cheapest_tickets

# url = (f'https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin=MOW&departure_at=2023-09'
#        '&unique=true&sorting=price&return_at=2023-09&direct=false&cy=rub&limit=10&page=1&one_way=true&token'
#        f'={AVIASALES_API_TOKEN}')
#
# response = requests.get(url=url)

# tickets = send_request_top_cheapest_tickets(origin='MOW', departure_at='2023-09-01', return_at='2023-09-14', limit=10)
# tickets = send_request_top_cheapest_tickets(origin='MOW', departure_at='2023-09-01', limit=10)
tickets = send_request_top_cheapest_tickets(origin='GSV', limit=10)
data = pretty_response_top_cheapest_tickets(tickets)

with open('top_cheapest_tickets.json', 'w', encoding='utf-8') as file:
    json.dump(tickets, file, indent=4, ensure_ascii=False)


with open('top_cheapest_tickets.txt', 'w', encoding='utf-8') as file:
    file.write(data)

