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
    ("top_cheapest_tickets", "поиск самых дешевых билетов из заданного города"),
    ("popular_directions", "самые популярные направления из города"),
    ("history", "история поиска авиабилетов"),
)

AVIASALES_BASE_URL = "https://api.travelpayouts.com/aviasales/"

TRAVELPAYOUTS_BASE_URL = "https://autocomplete.travelpayouts.com/places2?locale=ru&types[]=airport&types[]=city&term="
