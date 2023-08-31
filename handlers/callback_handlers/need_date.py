from keyboards.inline.return_at_yes_no_keyboard import return_at_yes_no_markup
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
        bot.set_state(call.message.chat.id, CheapestTicketsInfoState.departure_at)
        # что-то сделать с  ticket_data["departure_at"]
        with bot.retrieve_data(call.message.chat.id) as ticket_data:
            ticket_data["departure_at"] = None
        return_at_yes_no_markup(call.message)

    elif call.data == "return_at_yes":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, CheapestTicketsInfoState.return_at)
        bot.send_message(
            call.message.chat.id,
            "Когда хотите вернуться? (укажите дату в формате YYYY-MM или YYYY-MM-DD): ",
        )

    elif call.data == "return_at_no":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, CheapestTicketsInfoState.limit)
        with bot.retrieve_data(call.message.chat.id) as ticket_data:
            ticket_data["return_at"] = None
        bot.send_message(
            call.message.chat.id, "Сколько вариантов Вам показать? (не более 5)"
        )
