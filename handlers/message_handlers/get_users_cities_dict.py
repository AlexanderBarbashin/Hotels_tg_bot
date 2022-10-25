import json
import re

from loguru import logger
from telebot.types import Message

from config_data import config
from keyboards.inline.found_cities_markup import found_cities_markup
from loader import bot
from states.user_states import UserState
from utils.request_to_api import requests_to_api


@bot.message_handler(state=UserState.users_cities_dict)
def get_users_cities_dict(message: Message) -> None:
    """
    Обработчик введенного пользователем названия города. Обрабатывает сообщение в состоянии пользователя
    users_cities_dict. Если в сообщении пользователя присутствуют цифры, отправляет пользователю соответствующее
    сообщение. Выполняет поисковый запрос на веб-страницу по названию города. Если поисковый запрос успешно выполнен,
    отправляет пользователю клавиатуру с названиями найденых городов и устанавливает состояние пользователя
    choose_city, иначе отправляет пользователю соответствующее сообщение
    """

    logger.info('user input city name: {city_name}'.format(
        city_name=message.text
    ))
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
        try:
            find = re.search(pattern, city_request.text)
            cities_list = json.loads(find[0])
            if cities_list:
                cities_dict = {}
                for i_city in cities_list:
                    caption = i_city['caption'].split(', ')
                    country_name = caption[-1]
                    cities_dict[i_city['destinationId']] = '{city_name}, {country_name}'.format(
                        city_name=i_city['name'],
                        country_name=country_name
                    )
                with bot.retrieve_data(message.chat.id) as data:
                    data['cities_dict'] = cities_dict
                bot.send_message(message.chat.id,
                                 'По вашему запросу найдено городов: {cities_amount}\nВыберите наиболее '
                                 'подходящий:'.format(
                                     cities_amount=len(cities_dict)
                                 ),
                                 reply_markup=found_cities_markup(cities_dict))
                bot.set_state(message.chat.id, UserState.choose_city)
            else:
                bot.send_message(message.chat.id, 'По вашему запросу не найдено ни одного города. Повторите ввод')
        except Exception as exc:
            logger.exception(exc)
            bot.send_message(message.chat.id, 'По вашему запросу ничего не найдено. Попробуйте еще раз')
