from telebot.handler_backends import State, StatesGroup


class PopularDirectionsState(StatesGroup):
    """
    Класс с состояниями для команды popular_directions
    """
    origin = State()
    destination = State()
    departure_at = State()
    return_at = State()
    limit = State()
