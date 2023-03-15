from peewee import *

db = SqliteDatabase('users_history.db')


# создали модель таблицы
class Users(Model):
    name = CharField()
    nickname = CharField()

    class Meta:
        database = db


# вторая таблица, связанная внешним ключом foreignkey
class History(Model):
    user = ForeignKeyField(Users, related_name='')
    link = CharField()

    class Meta:
        database = db


# # создаем реальную таблицу на основе модели, которая описана в классе
# Users.create_table()
# History.create_table()
#
# # создаем записи (строки)
# sergey = Users.create(name='Sergey', nickname='@creespy')
# igor = Users.create(name='Igor', nickname='@harry')
#
# link_1 = History.create(user=sergey, link='hilton.com')
# link_2 = History.create(user=igor, link='mariot.com')
# link_3 = History.create(user=igor, link='radison.com')

# Сергей создал новый запрос
link_4 = History.create(
    user=Users.select().where(Users.name == 'Sergey').get(),
    link='google.com')
# TODO добавить проверку на существование юзера в БД, чтобы не было дублей
# TODO добавить методы добавления истории и новых юзеров, чтобы в боте было минимум действий с БД и все выполнялось одной строкой

