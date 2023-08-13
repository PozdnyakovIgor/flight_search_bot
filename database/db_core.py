from datetime import datetime

from peewee import *

db = SqliteDatabase('users_history.db')


class BaseModel(Model):
    class Meta:
        database = db


# создали модель таблицы
class Users(BaseModel):
    name = CharField()
    nickname = CharField()


# вторая таблица, связанная внешним ключом foreignkey
class History(BaseModel):
    user = ForeignKeyField(Users, related_name='')
    link = CharField()
    info = CharField()
    date = DateField()


# создаем реальную таблицу на основе модели, которая описана в классе
Users.create_table()
History.create_table()
admin = Users.create(name='admin', nickname='admin')


def add_user_to_database(name: str, nickname: str):
    if is_user_unique(nickname):
        new_user = Users.create(name=name, nickname=nickname)
        new_user.save(force_insert=True)
        print('Пользователь добавлен в базу')
        return new_user
    else:
        print('Пользователь уже есть базе')


def is_user_unique(nickname: str) -> bool:
    # TODO Плохо работает, надо проверять как-то по-другому. Смотреть ответ и проверять конкретное поле скорее всего
    return bool(Users.select().where(Users.nickname == nickname).get())


def add_tickets_search_to_history(nickname: str, link: str, info: str, date: str | datetime):
    History.create(user=Users.select().where(Users.nickname == nickname).get(),
                   link=link,
                   info=info,
                   date=date).save(force_insert=True)

# # создаем записи (строки)
# sergey = Users.create(name='Sergey', nickname='@creespy')
# igor = Users.create(name='Igor', nickname='@harry')
#
# link_1 = History.create(user=sergey, link='hilton.com')
# link_2 = History.create(user=igor, link='mariot.com')
# link_3 = History.create(user=igor, link='radison.com')
#
# # Сергей создал новый запрос
# link_4 = History.create(
#     user=Users.select().where(Users.name == 'Sergey').get(),
#     link='google.com')

