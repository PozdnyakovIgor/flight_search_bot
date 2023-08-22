import json
import requests

from config_data import TRAVELPAYOUTS_BASE_URL


# def get_city_name

def get_city_iata_code(city_name):
    url = f'{TRAVELPAYOUTS_BASE_URL}{city_name}'
    response = requests.get(url=url)

    for city_data in response.json():
        if city_data['name'] == city_name:
            city_iata_code = city_data['code']
            return city_iata_code


print(get_city_iata_code('Москва'))
print(get_city_iata_code('Саратов'))





# origin = 'Москва'
# destination = 'Саратов'
#
#
# url = f'{TRAVELPAYOUTS_BASE_URL}Из%20{origin}%20в%20{destination}'
#
# response = requests.get(url=url)
# print(response.text)

# url_2 = f'{TRAVELPAYOUTS_BASE_URL}Москва'
# response_2 = requests.get(url=url_2)
# with open('city_iata_code.json', 'w', encoding='utf-8') as file:
#     json.dump(response_2.json(), file, indent=4, ensure_ascii=False)
#
# with open('city_iata_code.json', 'r', encoding='utf-8') as file:
#     for i_city in file:
#         print(i_city)
# print(response_2.text)
