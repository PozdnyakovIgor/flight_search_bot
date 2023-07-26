import telebot
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup  # States
from telebot.storage import StateMemoryStorage  # States storage
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN

# Now, you can pass storage to bot.
state_storage = StateMemoryStorage()  # you can init here another storage

bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)


#   Закомментил, т к проверяю ReplyKeyboard
# States group.
# class MyStates(StatesGroup):
#     # Just name variables differently
#     name = State()  # creating instances of State class is enough from now
#     surname = State()
#     age = State()
#
#
# @bot.message_handler(commands=['start'])
# def welcome(message):
#     """
#     Start command. Here we are starting state
#     """
#     bot.set_state(message.from_user.id, MyStates.name, message.chat.id)
#     bot.send_message(message.chat.id, 'Hi, write me a name')
#
#
# @bot.message_handler(state='*', commands=['cancel'])
# def any_state(message):
#     """
#     Cancel state
#     """
#     bot.send_message(message.chat.id, 'Your state was cancelled')
#     bot.delete_state(message.from_user.id, message.chat.id)
#
#
# @bot.message_handler(state=MyStates.name)
# def name_get(message):
#     """
#     State 1. Will process when user's state is MyStates.name.
#     """
#     bot.send_message(message.chat.id, 'Now write me a surname')
#     bot.set_state(message.from_user.id, MyStates.surname, message.chat.id)
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['name'] = message.text
#
#
# @bot.message_handler(state=MyStates.surname)
# def ask_age(message):
#     """
#     State 2. Will process when user's state is MyStates.surname.
#     """
#     bot.send_message(message.chat.id, 'What is your age?')
#     bot.set_state(message.from_user.id, MyStates.age, message.chat.id)
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['surname'] = message.text
#
#
# # result
# @bot.message_handler(state=MyStates.age, is_digit=True)
# def ready_for_answer(message):
#     """
#     State 3. Will process when user's state is MyStates.age.
#     """
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         msg = ("Ready, take a look:\n<b>"
#                f"Name: {data['name']}\n"
#                f"Surname: {data['surname']}\n"
#                f"Age: {message.text}</b>")
#         bot.send_message(message.chat.id, msg, parse_mode="html")
#     bot.delete_state(message.from_user.id, message.chat.id)
#
#
# # incorrect number
# @bot.message_handler(state=MyStates.age, is_digit=False)
# def age_incorrect(message):
#     """
#     Wrong response for MyStates.age
#     """
#     bot.send_message(message.chat.id, 'Looks like you are submitting a string in the field age. Please enter a number')

# InlineKeyboard
# def gen_markup():
#     markup = InlineKeyboardMarkup()
#     markup.row_width = 2
#     markup.add(InlineKeyboardButton("Yes", callback_data='cb_yes'),
#                InlineKeyboardButton("No", callback_data='cb_no'))
#     return markup


# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     if call.data == 'cb_yes':
#         bot.answer_callback_query(call.id, 'Answer is Yes')
#     elif call.data == 'cb_no':
#         bot.answer_callback_query(call.id, 'Answer is No')


# @bot.message_handler(func=lambda message: True)
# def message_handler(message):
#     bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())

def keyboard():
    markup = ReplyKeyboardMarkup(row_width=2)
    kb = [KeyboardButton('func_1'), KeyboardButton('func_2'), KeyboardButton('func_3'), KeyboardButton('func_4')]
    markup.add(*kb)
    return markup


@bot.message_handler(commands=['start'])
def run_keyboard(message):
    bot.send_message(message.chat.id, 'You can use the keyboard', reply_markup=keyboard())


# @bot.message_handler(commands=['hello', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, "Hello world!")


# def test(message):
#     name = message.text
#     bot.send_message(message.chat.id, f'Ваше имя: {name}')


# def send_mssg(message):
#     bot.send_message(message.chat.id, 'Новое сообщение!')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


# register filters
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

if __name__ == '__main__':
    bot.infinity_polling()
