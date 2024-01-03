from loguru import logger
from telebot.types import Message

from loader import bot
from states.user_states import UserState


@bot.message_handler(state=UserState.distance_range)
def get_distance_range(message: Message) -> None:
    """
    Обработчик введенных пользователем в состоянии пользователя distance_range минимального и максимального расстояния,
    на котором находится отель от центра города, в километрах. Если сообщение пользователя не является числом или меньше
    0, пользователю отправляется соответствующее сообщение. Если минимальное расстояние не сохранено в информации
    пользователя, обработчик сохраняет введенное пользователем сообщение как минимальное расстояние и запрашивает
    максимальное расстояние; иначе если максимальное расстояние меньше минимального, пользователю отправляется
    соответствующее сообщение; иначе обработчик сохраняет введенное пользователем сообщение как максимальное расстояние,
    запрашивает количество отелей, которые необходимо вывести в результате поиска и устанавливает состояние
    пользователя hotels_amount
    """

    try:
        distance_str = message.text.replace(',', '.')
        distance = round(float(distance_str), 1)
        if distance < 0:
            bot.send_message(message.chat.id, 'Расстояние не может быть меньше 0! Повторите ввод!')
        else:
            with bot.retrieve_data(message.chat.id) as data:
                if 'min_distance' not in data:
                    logger.info('user input min distance: {min_distance}'.format(
                        min_distance=distance
                    ))
                    data['min_distance'] = distance
                    bot.send_message(message.chat.id, 'Введите максимальное расстояние, на котором находится отель от '
                                                      'центра города, в километрах')
                else:
                    if distance >= data['min_distance']:
                        logger.info('user input max distance: {max_distance}'.format(
                            max_distance=distance
                        ))
                        data['max_distance'] = distance
                        bot.send_message(message.chat.id, 'Введите количество отелей, которые необходимо вывести в '
                                                          'результате поиска (не более 40)')
                        bot.set_state(message.chat.id, UserState.hotels_amount)
                    else:
                        bot.send_message(message.chat.id, 'Максимальное расстояние, на котором находится отель от '
                                                          'центра города, должно быть не меньше минимального! '
                                                          'Повторите ввод!')
    except ValueError:
        bot.send_message(message.chat.id, 'Расстояние должно быть числом! Повторите ввод!')