from loader import bot
from states.ticket_information import TicketInfoState
from telebot.types import Message
from api_engine.api_engine import send_request, pretty_response


@bot.message_handler(commands=['want_ticket'])
def want_to_find_a_ticket(message: Message) -> None:
    bot.set_state(message.from_user.id, TicketInfoState.origin, message.chat.id)  # message.from_user.username - никнейм
    bot.send_message(message.from_user.id, f'Отлично! Укажите, откуда Вы бы хотели полететь?')


@bot.message_handler(state=TicketInfoState.origin)
def get_origin(message: Message) -> None:
    if message.text.isalpha():  # проверка для примера
        bot.send_message(message.from_user.id, 'Теперь введите город назначения:')
        bot.set_state(message.from_user.id, TicketInfoState.destination, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
            ticket_data['origin'] = message.text

    else:
        bot.send_message(message.from_user.id, 'Название города может содержать только буквы.')


@bot.message_handler(state=TicketInfoState.destination)
def get_destination(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Когда хотите полететь?')
    bot.set_state(message.from_user.id, TicketInfoState.departure_at, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:  # необходимо добавить проверку на
        # правильность введенной даты
        ticket_data['destination'] = message.text


@bot.message_handler(state=TicketInfoState.departure_at)
def get_departure_at(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Когда хотите вернуться?')
    bot.set_state(message.from_user.id, TicketInfoState.return_at, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:  # необходимо добавить проверку на
        # правильность введенной даты
        ticket_data['departure_at'] = message.text


@bot.message_handler(state=TicketInfoState.return_at)
def get_return_at(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Отлично! Вся информация есть, ищу билеты...')

    # TODO необходимо добавить проверку на правильность введенной даты
    # TODO подумать, в какое состояние необходимо возвращаться, когда будет введена вся информация

    with bot.retrieve_data(message.from_user.id, message.chat.id) as ticket_data:
        ticket_data['return_at'] = message.text

    tickets = send_request(ticket_data['origin'], ticket_data['destination'],
                           ticket_data['departure_at'], ticket_data['return_at'])

    bot.send_message(message.chat.id, pretty_response(tickets))
