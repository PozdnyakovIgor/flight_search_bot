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
    user = ForeignKeyField(Users, related_name="")
    link = CharField()
    info = CharField()
    date = DateField()


Users.create_table()
History.create_table()


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


def add_tickets_search_to_history(
    nickname: str, link: str, info: str, date: str | datetime
) -> None:
    """
    Функция для добавления билета в историю поиска
    :param nickname: никнейм пользователя
    :param link: ссылка на билет
    :param info: краткая информация о билете
    :param date: дата поиска
    """
    History.create(
        user=Users.select().where(Users.nickname == nickname).get(),
        link=link,
        info=info,
        date=date,
    ).save()
