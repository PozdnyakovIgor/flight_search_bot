from loader import bot
from states.popular_directions_states import PopularDirectionsState
from telebot.types import Message, CallbackQuery
from api_engine import get_city_iata_code, get_city_name_from_iata_code
from api_engine.api_aviasales_engine import (
    send_request_popular_directions,
    get_popular_directions,
)
from keyboards.inline.cities_keyboard import show_cities_keyboard
from keyboards.inline.departure_at_yes_no_keyboard import departure_at_yes_no_markup

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
        bot.send_message(message.from_user.id, f'В работе...')
        city_iata_code = get_city_iata_code(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data["origin"] = city_iata_code

        show_cities_keyboard(message, get_popular_directions(send_request_popular_directions(origin=city_iata_code)))

    else:
        bot.send_message(
            message.from_user.id,
            "В данном городе нет аэропорта, либо Вы ввели название города с "
            "ошибкой. Введите название города:",
        )


@bot.callback_query_handler(func=lambda call: len(call.data) == 3)
def city_iata_code_callback(call: CallbackQuery) -> None:
    """
    Пользователь выбрал город прибытия, нажав на кнопку.  Записываем IATA-код города и запрашиваем хочет ли он
    указать дату отправления.
    :param call: Получает IATA-код города
    :return: None
    """
    if call.data:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        with bot.retrieve_data(call.message.chat.id) as ticket_data:
            ticket_data['destination'] = call.data
            bot.send_message(call.message.chat.id, f"Выбран город прибытия: {get_city_name_from_iata_code(call.data)}")
    bot.set_state(call.message.chat.id, PopularDirectionsState.destination)
    # создать новую инлайн-клаву да-нет




@bot.message_handler(state=PopularDirectionsState.destination)
def get_destination(message: Message) -> None:
    pass




# url = f'http://api.travelpayouts.com/v1/city-directions?origin=VVO&currency=rub&token={AVIASALES_API_TOKEN}'
# response = requests.get(url=url).json()
# with open('popular.json', 'w', encoding='utf-8') as data:
#     json.dump(response, data, indent=4,  ensure_ascii=False)



