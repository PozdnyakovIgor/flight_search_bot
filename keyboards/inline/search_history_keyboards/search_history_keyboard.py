from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from database.db_core import History, Users, TicketsInfo, db
from loader import bot


# TODO дописать callback_data, чтобы выдавал найденные билеты
# TODO сделать сохранение в БД только последних 10 запросов
def show_request_history(message: Message):
    for history_entry in (
        History.select()
        .where(History.user == Users.get(Users.nickname == message.chat.username))
        .order_by(History.date_time.desc())
    ):
        history_entry_info = f"Команда: \\{history_entry.command};\nЗапрос: {history_entry.request_info};\nДата и время запроса: {history_entry.date_time}"
        one_ticket_info_str = ''
        for one_ticket_info in TicketsInfo.select().where(
            TicketsInfo.request_id == history_entry.id

        ):
            one_ticket_info_str = (
                f"{one_ticket_info.ticket_info}, {one_ticket_info.ticket_link}"
            )
            print(one_ticket_info_str)
        # bot.send_message(
        #     message.from_user.id,
        #     history_entry_info,
        #     reply_markup=InlineKeyboardMarkup().add(
        #         InlineKeyboardButton(
        #             text="вывести результат поиска", callback_data=one_ticket_info_str
        #         )
        #     ),
        # )


# for one_ticket_info in TicketsInfo.select().where(TicketsInfo.request_id == History.get()):
#     one_ticket_info = f"{one_ticket_info.ticket_info}"
#     print(one_ticket_info)
#

# print(History.get())  # сработало, когда прошел скрипт (выполнил команду в тг-боте)
