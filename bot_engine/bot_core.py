from datetime import datetime

import telebot
from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from telebot.handler_backends import State, StatesGroup  # States
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.storage import StateMemoryStorage  # States storage
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config_data.config import BOT_TOKEN
from api_engine import send_request, pretty_response
from database import *


def starting_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keys = [KeyboardButton('Хочу найти билет!'),
            KeyboardButton('Хочу отдохнуть, но не знаю где...'),
            KeyboardButton('Ближайшие аэропорты'),
            KeyboardButton('История'),
            KeyboardButton('/FAQ')
            ]
    markup.add(*keys)
    return markup


# Возможно стоит сделать дополнительные клавиатуры в каких-то сложных местах
# def tickets_keyboard():
#     markup = ReplyKeyboardMarkup(row_width=2)
#     keys = [KeyboardButton('Хочу найти билет!'),
#             KeyboardButton('FAQ'),
#             # KeyboardButton('func_3'),
#             # KeyboardButton('func_4')
#             ]
#     markup.add(*keys)
#     return markup


# @bot.message_handler(commands=['start'])
# def starting_message(message):
#     # add_user_to_database(name=message.chat.first_name,
#     #                      nickname=message.chat.username)
#     bot.send_message(
#         message.chat.id,
#         'Привет, это бот по поиску авиабилетов из кэша авиасейлс',
#         reply_markup=starting_keyboard())
#
#
# @bot.message_handler(commands=['FAQ'])
# def help_user(message):
#     bot.reply_to(message, "'Хочу найти билет!' - поиск билетов с конкретными датами вылета/прилета;\n"
#                           "'Хочу отдохнуть, но не знаю где...' - поиск самых дешевых билетов из заданного города;\n"
#                           "'Ближайшие аэропорты' - вывод ближайших аэропортов;\n"
#                           "'История' - история поиска авиабилетов.")


# @bot.message_handler(func=lambda message: True, regexp='Хочу найти билет!')
# def initialize_ticket_searching(message):
#     bot.reply_to(message, 'Отлично! Укажите пожалуйста куда и когда вы бы хотели полететь')
#
#
# @bot.message_handler(func=lambda message: True, regexp=r'.*\d\d\d\d-\d\d.*')
# def initialize_ticket_searching(message):
#     bot.reply_to(message, 'Вас понял, сейчас поищем!')
#     # TODO делать для каждого параметра свой вопрос
#     origin, destination, departure_at = message.text.split(' ')
#     tickets = send_request(origin, destination, departure_at)['data']
#
#     # Обработаем пустой ответ от АПИ
#     if not len(tickets):
#         bot.send_message(message.chat.id, 'В кэше не найдено таких билетов :(')
#
#     # Возможно собирание инфу для БД стоит сделать отдельным методом для читабельности
#     # for ticket in tickets:
#     #     add_tickets_search_to_history(
#     #         nickname=message.chat.username,
#     #         link=f'https://www.aviasales.ru{ticket["link"]}',
#     #         info=f'{ticket["origin"]} -> {ticket["destination"]} '
#     #              f'at {ticket["departure_at"]}({ticket["duration_to"]}mins)',
#     #         date=datetime.now())
#
#     bot.send_message(message.chat.id, pretty_response(tickets))


# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message):  # Название функции не играет никакой роли
#     bot.send_message(message.chat.id, message.text)


# if __name__ == '__main__':
#     bot.add_custom_filter(StateFilter(bot))
#     set_default_commands(bot)
#     bot.infinity_polling()
