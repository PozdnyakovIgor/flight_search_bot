from keyboards.inline.cities_keyboard import show_cities_keyboard
from loader import bot
from telebot.types import CallbackQuery
from states.popular_directions_states import PopularDirectionsState
from handlers.custom_handlers import popular_directions
from keyboards.inline.departure_at_yes_no_keyboard import departure_at_yes_no_markup


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
        bot.set_state(call.message.chat.id, PopularDirectionsState.destination)
        with bot.retrieve_data(call.message.chat.id) as ticket_data:
            ticket_data['destination'] = call.data

        bot.send_message(call.message.chat.id, '?')


