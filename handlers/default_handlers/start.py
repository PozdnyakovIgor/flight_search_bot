from telebot.types import Message
from loader import bot
from keyboards.reply.keyboard_with_all_funcs import starting_keyboard


@bot.message_handler(commands=['start'])
def starting_message(message: Message) -> None:
    # add_user_to_database(name=message.chat.first_name,
    #                      nickname=message.chat.username)
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.full_name}, это бот по поиску авиабилетов из кэша Авиасейлз',
        reply_markup=starting_keyboard())
