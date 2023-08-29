from telebot.handler_backends import State, StatesGroup


class CheapestTicketsInfoState(StatesGroup):
    """
    Класс с состояниями для команды top_cheapest_tickets
    """
    origin = State()
    departure_at = State()
    return_at = State()
    limit = State()
    ask_departure = State()
    ask_return = State()
