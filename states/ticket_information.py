from telebot.handler_backends import State, StatesGroup


# 1. origin
# 2. destination
# 3. departure_at   #пункты 1-3 - обязательно, остальные на усмотрение
# 4. return_at
# 5. one_way
# 6. direct
# 7. limit
# 8. sorting

class TicketInfoState(StatesGroup):
    origin = State()
    destination = State()
    departure_at = State()
    return_at = State()
    limit = State()
