from telebot.handler_backends import State, StatesGroup


class TicketInfoState(StatesGroup):
    """
    Класс с состояниями для команды want_to_find_a_ticket
    """
    origin = State()
    destination = State()
    departure_at = State()
    return_at = State()
    limit = State()
