from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '6219320706:AAE_W280MuVC1LGJ-nRW18tyzr4EJfSwUuU'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])  # Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message):

    # History.create(user=Person.select().
    #                where(Person.name == message.chat.full_name),
    #                link=message.text)

    # database_engine.core.create_new_hotel_history(message, text)

    custom_keys = [
        [
            KeyboardButton(text="Сможешь повторить это?"),
            KeyboardButton(text="А это?")
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=custom_keys)

    await message.reply("Привет!\nЯ Эхобот от Skillbox!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.", reply_markup=keyboard)
    # Так как код работает асинхронно, то обязательно пишем await.


link_keys = InlineKeyboardMarkup(row_width=1)
link_key_1 = InlineKeyboardButton(text='Перейти в блог Skillbox', url='https://skillbox.ru/media/code/')
link_key_2 = InlineKeyboardButton(text='Перейти к курсам Skillbox', url='https://skillbox.ru/code/')
link_keys.add(link_key_1, link_key_2)


@dp.message_handler(commands=['ссылки'])
async def url_command(message: types.Message):
    await message.answer('Полезные ссылки:', reply_markup=link_keys)


@dp.message_handler()  # Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message):  # Создаём функцию с простой задачей — отправить обратно тот же текст, что ввёл пользователь.
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
