from datetime import datetime

from loguru import logger
from telebot.types import Message

from database.search_history import *
from loader import bot
from states.user_states import UserState


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def get_city(message: Message) -> None:
    """
    Обработчик команд /lowprice, /highprice и /bestdeal. Устанавливает состояние пользователя users_cities_dict,
    сбрасывает информацию пользователя, сохраняет введенную пользователем команду (из трех возможных вариантов),
    сохраняет пользователя, введенную им команду, дату и время ввода команды в историю поиска и запрашивает у
    пользователя название города, в котором будет происходить поиск отелей
    """

    logger.info('user input command: {command}'.format(
        command=message.text
    ))
    command_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    bot.set_state(message.chat.id, UserState.users_cities_dict)
    bot.reset_data(message.chat.id)
    with bot.retrieve_data(message.chat.id) as data:
        data['command'] = message.text[1:]
        with db:
            user = User.get_or_none(User.user_name == message.from_user.first_name,
                                    User.user_tg_id == message.from_user.id,
                                    is_relative=True)
            if not user:
                user = User.create(user_name=message.from_user.first_name, user_tg_id=message.from_user.id,
                                   is_relative=True)
            search_request = SearchRequest.create(author=user, command=message.text, command_datetime=command_datetime,
                                                  city='-', hotels_list='-')
            data['search_request_id'] = search_request.id
    bot.send_message(message.chat.id, 'Введите название города, в котором вы хотите выполнить поиск отеля')
