from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['help'])
def help_user(message: Message) -> None:
    """
    Команда-подсказка для вывода справки пользователю по основным командам

    """

    bot.reply_to(message, "/want_ticket - поиск билетов с конкретными датами вылета/прилета;\n"
                          "/top_cheapest_tickets - поиск самых дешевых билетов из заданного города;\n"
                          "/nearest_airports - вывод ближайших аэропортов;\n"
                          "/history - история поиска авиабилетов.")
    bot.delete_state(message.from_user.id, message.chat.id)
