from loader import bot
from states.user_states import UserState
from config_data import config
from utils.request_to_api import requests_to_api
import json
import re
from keyboards.inline.found_cities_markup import found_cities_markup
from telebot.types import Message


@bot.message_handler(state=UserState.users_cities_dict)
def get_users_cities_dict(message: Message) -> None:
    """
    Обработчик введенного пользователем названия города. Обрабатывает сообщение в состоянии пользователя
    users_cities_dict. Если в сообщении пользователя присутствуют цифры, отправляет пользователю соответствующее
    сообщение. Выполняет поисковый запрос на веб-страницу по названию города. Если поисковый запрос успешно выполнен,
    отправляет пользователю клавиатуру с названиями найденых городов и устанавливает состояние пользователя
    choose_city, иначе отправляет пользователю соответствующее сообщение
    """

    for i_sym in message.text:
        if i_sym.isdigit():
            bot.send_message(message.chat.id,
                             'Ошибка! В названии города не может быть цифр! Повторите ввод')
            break
    else:
        cities_url = 'https://hotels4.p.rapidapi.com/locations/v2/search'
        cities_querystring = {'query': '{city}'.format(city=message.text), 'locale': 'ru_RU', 'currency': 'RUB'}
        city_request = requests_to_api(cities_url, config.headers, cities_querystring)
        pattern = r'(?<="CITY_GROUP","entities":).+?[\]]'
        find = re.search(pattern, city_request.text)
        if find:
            cities_list = json.loads(find[0])
            bot.send_message(message.chat.id,
                             'По вашему запросу найдено городов: {cities_amount}\nВыберите наиболее подходящий:'.format(
                                 cities_amount=len(cities_list)
                             ),
                             reply_markup=found_cities_markup(cities_list))
            bot.set_state(message.chat.id, UserState.choose_city)
        else:
            bot.send_message(message.chat.id, 'По вашему запросу ничего не найдено. Попробуйте еще раз')
