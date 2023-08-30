from loader import bot
from telebot.types import CallbackQuery
from states.top_cheapest_tickets_states import CheapestTicketsInfoState


@bot.callback_query_handler(func=lambda call: True)
def need_departure_at_callback(call: CallbackQuery) -> None:
    """
    Пользователь нажал кнопку "Да" или "Нет"
    :param call: 'yes' or 'no'
    :return: None
    """

    if call.data == "departure_at_yes":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, CheapestTicketsInfoState.departure_at)
        bot.send_message(
            call.message.chat.id,
            "Введите дату отправления (в формате YYYY-MM или YYYY-MM-DD): ",
        )
    elif call.data == "departure_at_no":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        pass
    elif call.data == "return_at_yes":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, CheapestTicketsInfoState.return_at)
        bot.send_message(
            call.message.chat.id,
            "Когда хотите вернуться? (укажите дату в формате YYYY-MM или YYYY-MM-DD): ",
        )
    elif call.data == "return_at_no":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        pass
