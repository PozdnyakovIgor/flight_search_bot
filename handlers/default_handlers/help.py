from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['help'])
def help_user(message: Message) -> None:
    bot.reply_to(message, "/want_ticket - поиск билетов с конкретными датами вылета/прилета;\n"
                          "/fly_away - поиск самых дешевых билетов из заданного города;\n"
                          "/nearest_airports - вывод ближайших аэропортов;\n"
                          "/history - история поиска авиабилетов.")