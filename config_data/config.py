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
    ("help", "Вывести справку")
)  # надо ли добавлять сюда все команды: /ticket_prices_on_certain_dates, /ticket_prices_on_uncertain_dates и тд?

AVIASALES_BASE_URL = 'https://api.travelpayouts.com/aviasales/'