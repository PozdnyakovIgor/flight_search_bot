from loader import bot
from telebot import types
from telebot.types import Message, Dict


def show_cities_keyboard(message: Message, cities: Dict) -> None:
    """
    Формирует из словаря городов инлайн-клавиатуру и посылает её в чат.
    :param message: Message
    :param cities: dict
    :return: None
    """
    cities_keyboard = types.InlineKeyboardMarkup()
    for iata_code, city in cities.items():
        cities_keyboard.add(types. InlineKeyboardButton(text=city, callback_data=iata_code))
    bot.send_message(message.from_user.id, "Вот самые популярные направления из данного города. Выберите, куда хотите "
                                           "полететь: ", reply_markup=cities_keyboard)
