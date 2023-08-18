from telebot.types import Message
from loader import bot
from keyboards.reply.keyboard_with_all_funcs import starting_keyboard


# TODO сделать так, чтобы отображались как ссылки на функции, а не как просто текст
@bot.message_handler(commands=['help'])
def help_user(message):
    bot.reply_to(message, "'Хочу найти билет!' - поиск билетов с конкретными датами вылета/прилета;\n"
                          "'Хочу отдохнуть, но не знаю где...' - поиск самых дешевых билетов из заданного города;\n"
                          "'Ближайшие аэропорты' - вывод ближайших аэропортов;\n"
                          "'История' - история поиска авиабилетов.")
