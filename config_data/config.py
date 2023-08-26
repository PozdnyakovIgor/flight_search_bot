import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
AVIASALES_API_TOKEN = os.getenv("AVIASALES_API_TOKEN")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("want_ticket", "поиск билетов с конкретными датами вылета/прилета"),
    ("fly_away", "поиск самых дешевых билетов из заданного города"),
    ("nearest_airports", "вывод ближайших аэропортов"),
    ("history", "история поиска авиабилетов")
)

AVIASALES_BASE_URL = 'https://api.travelpayouts.com/aviasales/'
# TRAVELPAYOUTS_BASE_URL = 'https://autocomplete.travelpayouts.com/places2?locale=ru&types[]=city&term='  # тут поиск
# только по городам
TRAVELPAYOUTS_BASE_URL = 'https://autocomplete.travelpayouts.com/places2?locale=ru&types[]=airport&types[]=city&term='
# показывает город и все аэропорты в городе
