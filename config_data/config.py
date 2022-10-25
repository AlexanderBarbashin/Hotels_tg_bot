import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

TOKEN = os.getenv('TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
RAPID_API_HOST = os.getenv('RAPID_API_HOST')

headers = {
    'X-RapidAPI-Key': RAPID_API_KEY,
    'X-RapidAPI-Host': RAPID_API_HOST
}

DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('hello_world', 'Вывести сообщение "Привет мир!"'),
    ('lowprice', 'Вывести топ самых дешевых отелей в городе'),
    ('highprice', 'Вывести топ самых дорогих отелей в городе'),
    ('bestdeal', 'Вывести топ отелей, наиболее подходящих по цене и расположению от центра города')
)
