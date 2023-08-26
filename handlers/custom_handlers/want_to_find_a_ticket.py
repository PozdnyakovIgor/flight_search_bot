from loader import bot
from states.ticket_information import TicketInfoState
from telebot.types import Message
from api_engine.api_aviasales_engine import send_request, pretty_response
from api_engine.api_travelpayouts_engine import get_city_iata_code
from utils.check_date import check_date


@bot.message_handler(commands=['want_ticket'])
def want_to_find_a_ticket(message: Message) -> None:
    bot.set_state(message.from_user.id, TicketInfoState.origin, message.chat.id)  # message.from_user.username - никнейм
    bot.send_message(message.from_user.id, f'Отлично! Укажите, откуда Вы бы хотели полететь?')


# TODO подумать над последовательностью вопроса и записи ответа внутри функций (в начале with...., а потом следующий
#  вопрос)
@bot.message_handler(state=TicketInfoState.origin)
def get_origin(message: Message) -> None:
    if get_city_iata_code(message.text) is not None:
        bot.send_message(message.from_user.id, 'Теперь введите город назначения:')
        bot.set_state(message.from_user.id, TicketInfoState.destination, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data['origin'] = get_city_iata_code(message.text)

    else:
        bot.send_message(message.from_user.id, 'В данном городе нет аэропорта, либо Вы ввели название города с '
                                               'ошибкой. Введите название города:')


@bot.message_handler(state=TicketInfoState.destination)
def get_destination(message: Message) -> None:
    if get_city_iata_code(message.text) is not None:
        bot.send_message(message.from_user.id, 'Когда хотите полететь? Введите дату в формате YYYY-MM или YYYY-MM-DD')
        bot.set_state(message.from_user.id, TicketInfoState.departure_at, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:  # необходимо добавить проверку на
            # правильность введенной даты
            ticket_data['destination'] = get_city_iata_code(message.text)

    else:
        bot.send_message(message.from_user.id, 'В данном городе нет аэропорта, либо Вы ввели название города с '
                                               'ошибкой. Введите название города:')


@bot.message_handler(state=TicketInfoState.departure_at)
def get_departure_at(message: Message) -> None:

    if check_date(message.text):
        bot.send_message(message.from_user.id, 'Когда хотите вернуться? Введите дату в формате YYYY-MM или YYYY-MM-DD')
        bot.set_state(message.from_user.id, TicketInfoState.return_at, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data['departure_at'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Проверьте правильность введенной даты: формат даты должен быть '
                                               'YYYY-MM или YYYY-MM-DD, на прошедшие даты поиск не возможен.')


@bot.message_handler(state=TicketInfoState.return_at)
def get_return_at(message: Message) -> None:
    if check_date(message.text):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            if ticket_data['departure_at'] > message.text:
                bot.send_message(message.from_user.id, 'Дата возвращения не может быть раньше, чем дата отправления!')
            else:
                ticket_data['return_at'] = message.text
                bot.send_message(message.from_user.id, 'Сколько вариантов показать (не более 5) ?')
                bot.set_state(message.from_user.id, TicketInfoState.limit, message.chat.id)

    else:
        bot.send_message(message.from_user.id, 'Проверьте правильность введенной даты: формат даты должен быть '
                                               'YYYY-MM или YYYY-MM-DD, на прошедшие даты поиск не возможен.')


# @bot.message_handler(state=TicketInfoState.return_at)
# def get_return_at(message: Message) -> None:
#     if check_date(message.text):
#         bot.send_message(message.from_user.id, 'Сколько вариантов показать (не более 5) ?')
#         bot.set_state(message.from_user.id, TicketInfoState.limit, message.chat.id)
#
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
#             ticket_data['return_at'] = message.text
#
#     else:
#         bot.send_message(message.from_user.id, 'Проверьте правильность введенной даты: формат даты должен быть '
#                                                'YYYY-MM или YYYY-MM-DD, на прошедшие даты поиск не возможен.')


@bot.message_handler(state=TicketInfoState.limit)
def get_limit(message: Message) -> None:
    if message.text.isdigit() and 0 < int(message.text) <= 5:
        bot.send_message(message.from_user.id, 'Отлично! Вся информация есть, ищу билеты...')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data['limit'] = message.text

        tickets = send_request(ticket_data['origin'], ticket_data['destination'],
                               ticket_data['departure_at'], ticket_data['return_at'], ticket_data['limit'])

        # # Обработаем пустой ответ от АПИ
        # if not len(tickets['data']):  # работает, если запрос составлен верно; если в запросе были ошибки, то TypeError:
        #     # object of
        #     # type 'NoneType' has no len()
        #     bot.send_message(message.chat.id, 'В кэше не найдено таких билетов :(')
        #
        # else:
        bot.send_message(message.chat.id, pretty_response(tickets))
        bot.delete_state(message.from_user.id, message.chat.id)  # сбрасываем состояние после выполнения запроса

    else:
        bot.send_message(message.from_user.id, 'Проверьте правильность введенного количества вариантов, должно быть '
                                               'не более 5.')
