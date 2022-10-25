from telebot.types import Message

from database.search_history import *
from loader import bot


@bot.message_handler(commands=['history'])
def send_history(message: Message) -> None:
    """
    Обработчик команды /history. Отправляет пользователю сообщения с историей поиска отелей для каждого пользователя
    """

    with db:
        if User.select():
            bot.send_message(message.from_user.id, 'Вывожу историю поиска отелей:')
            for user in User.select():
                bot.send_message(message.from_user.id, '*' * 50 + '\nДля пользователя {user_name}\n'.format(
                    user_name=user.user_name) + '*' * 50)
                for search_request in user.requests:
                    message_text = 'Команда, введенная пользователем: {command}\nДата и время ввода команды: ' \
                                    '{command_datetime}\nГород, в котором производился поиск отелей: {city}\nОтели, ' \
                                    'которые были найдены в результате:\n{hotels_names}'.format(
                        command=search_request.command,
                        command_datetime=search_request.command_datetime,
                        city=search_request.city,
                        hotels_names=search_request.hotels_list
                    )
                    bot.send_message(message.from_user.id, message_text)
        else:
            bot.send_message(message.from_user.id, 'История поиска отелей пуста')