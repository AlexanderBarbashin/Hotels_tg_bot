from loguru import logger
from telebot.types import Message

from loader import bot
from states.user_states import UserState


@bot.message_handler(state=UserState.price_range)
def get_price_range(message: Message) -> None:
    """
    Обработчик введенных пользователем в состоянии пользователя price_range минимальной и максимальной цен проживания
    в отеле за сутки в рублях. Если сообщение пользователя не является числом или меньше 0, пользователю отправляется
    соответствующее сообщение. Если минимальная цена не сохранена в информации пользователя, обработчик сохраняет
    введенное пользователем сообщение как минимальную цену и запрашивает максимальную цену; иначе если максимальная цена
    меньше минимальной, пользователю отправляется соответствующее сообщение; иначе обработчик сохраняет введенное
    пользователем сообщение как максимальную цену, запрашивает минимальное расстояние, на котором находится отель от
    центра города, в километрах и устанавливает состояние пользователя distance_range
    """

    try:
        price = int(message.text)
        if price < 0:
            bot.send_message(message.chat.id, 'Цена не может быть меньше 0! Повторите ввод!')
        else:
            with bot.retrieve_data(message.chat.id) as data:
                if 'min_price' not in data:
                    logger.info('user input min price: {min_price}'.format(
                        min_price=price
                    ))
                    data['min_price'] = price
                    bot.send_message(message.chat.id, 'Введите максимальную цену проживания в отеле за сутки в рублях')
                else:
                    if price >= data['min_price']:
                        logger.info('user input max price: {max_price}'.format(
                            max_price=price
                        ))
                        data['max_price'] = price
                        bot.send_message(message.chat.id, 'Введите минимальное расстояние, на котором находится отель '
                                                          'от центра города, в километрах')
                        bot.set_state(message.chat.id, UserState.distance_range)
                    else:
                        bot.send_message(message.chat.id, 'Максимальная цена проживания в отеле за сутки в рублях '
                                                          'должна быть не меньше минимальной! Повторите ввод!')
    except ValueError:
        bot.send_message(message.chat.id, 'Цена должна быть числом! Повторите ввод!')