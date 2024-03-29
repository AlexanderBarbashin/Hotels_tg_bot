from loguru import logger
from telebot.types import CallbackQuery

from database.search_history import *
from loader import bot
from states.user_states import UserState


@bot.callback_query_handler(func=None, state=UserState.choose_city)
def choose_city(callback_city_info: CallbackQuery) -> None:
    """
    Обработчик информации с клавиши, нажатой пользователем при выборе наиболее подходящего города из списка найденных
    в состоянии choose_city. Сохраняет id выбранного пользователем города. Сохраняет название города, в котором
    выполнялся поиск отелей, в историю поиска. Если пользователь вводил команду /bestdeal,
    запрашивает у пользователя минимальную цену проживания в отеле за сутки в рублях и устанавливает состояние
    пользователя price_range. Если пользователь вводил команду /lowprice или /highprice, запрашивает у пользователя
    количество отелей, которые необходимо вывести в результате поиска и устанавливает состояние пользователя
    hotels_amount
    """

    logger.info('user choose city: {city}'.format(
        city=callback_city_info.data
    ))
    with bot.retrieve_data(callback_city_info.message.chat.id) as data:
        data['users_city_id'] = callback_city_info.data
        with db:
            search_request = SearchRequest.get(id=data['search_request_id'])
            search_request.city = data['cities_dict'][callback_city_info.data]
            search_request.save()
        if data['command'] == 'bestdeal':
            bot.send_message(callback_city_info.message.chat.id,
                             'Введите минимальную цену проживания в отеле за сутки в рублях')
            bot.set_state(callback_city_info.message.chat.id, UserState.price_range)
        else:
            bot.send_message(callback_city_info.message.chat.id,
                             'Введите количество отелей, которые необходимо вывести в результате (не более 40)')
            bot.set_state(callback_city_info.message.chat.id, UserState.hotels_amount)
