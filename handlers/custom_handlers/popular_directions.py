from loader import bot
from states.popular_directions_states import PopularDirectionsState
from telebot.types import Message
from api_engine import get_city_iata_code
from api_engine.api_aviasales_engine import send_request_popular_directions

from config_data.config import AVIASALES_API_TOKEN
import requests
import json


@bot.message_handler(commands=['popular_directions'])
def popular_directions(message: Message) -> None:
    """
    Команда для поиска популярных направлений из заданного города. При вводе города отправления появляется
    инлайн-клавиатура с названиями самых популярных городов прибытия. Здесь задается состояние origin.
    :param message: Message
    :return: None
    """
    bot.set_state(message.from_user.id, PopularDirectionsState.origin, message.chat.id)
    bot.send_message(message.from_user.id, f'Самые популярные направления из какого города Вам показать?')


@bot.message_handler(state=PopularDirectionsState.origin)
def get_origin(message: Message) -> None:
    """
    Метод, в котором обрабатываем сообщение с городом отправления, если состояние пользователя
    PopularDirectionsState.origin. Также осуществляется проверка на корректность введенного города и появляется
    инлайн-клавиатура с названиями городов
    :param message: Message
    :return: None
    """
    if get_city_iata_code(message.text) is not None:
        city_iata_code = get_city_iata_code(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["origin"] = city_iata_code
        send_request_popular_directions(origin=city_iata_code)

    else:
        bot.send_message(
            message.from_user.id,
            "В данном городе нет аэропорта, либо Вы ввели название города с "
            "ошибкой. Введите название города:",
        )



# url = f'http://api.travelpayouts.com/v1/city-directions?origin=VVO&currency=rub&token={AVIASALES_API_TOKEN}'
# response = requests.get(url=url).json()
# with open('popular.json', 'w', encoding='utf-8') as data:
#     json.dump(response, data, indent=4,  ensure_ascii=False)



