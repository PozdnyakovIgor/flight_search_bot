from contextlib import suppress
from datetime import datetime

from peewee import *

db = SqliteDatabase("users_history.db")


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    name = CharField()
    nickname = CharField(unique=True)


class History(BaseModel):
    user = ForeignKeyField(Users, db_column='user')
    command = CharField()
    request_info = CharField()
    date_time = DateTimeField()


class TicketsInfo(BaseModel):
    request_id = ForeignKeyField(History)  # to_field - не знаю, правильно или нет
    ticket_info = CharField()
    ticket_link = CharField()


Users.create_table()
History.create_table()
TicketsInfo.create_table()


def add_user_to_database(name: str, nickname: str) -> Model:
    """
    Функция для добавления нового пользователя в бд
    :param name: имя пользователя
    :param nickname: уникальный никнейм
    :return: new_user
    :rtype: Model
    """

    with suppress(IntegrityError):
        new_user = Users.create(name=name, nickname=nickname)
        new_user.save()
        return new_user


def add_request_search_to_history(
    nickname: str, command: str, user_request: str, date: str | datetime
) -> None:
    """
    Функция для добавления введенной команды и найденных билетов в историю поиска
    :param command: команда, которую ввел пользователь
    :param nickname: никнейм пользователя
    :param user_request: запрос пользователя
    :param date: дата поиска
    """
    new_entry = History.create(
        user=Users.select().where(Users.nickname == nickname).get(),
        command=command,
        request_info=user_request,
        date_time=date,
    ).save()
    return new_entry

# было
#     History.create(
#         user=Users.select().where(Users.nickname == nickname).get(),
#         command=command,
#         request_info=user_request,
#         date_time=date,
#     ).save()
#
