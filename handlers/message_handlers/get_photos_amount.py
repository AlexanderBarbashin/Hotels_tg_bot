from loguru import logger
from telebot.types import Message

from loader import bot
from states.user_states import UserState
from utils.misc.send_hotels_info import send_hotels_info


@bot.message_handler(state=UserState.photos_amount)
def get_photos_amount(message: Message) -> None:
    """
    Обработчик введенного пользователем количества фото, которые необходимо вывести для каждого найденного отеля (не
    более 10), в состоянии пользователя photos_amount. Если сообщение пользователя не является числом или не больше 0,
    пользователю отправляется соответствующее сообщение. Если сообщение пользователя больше 10, обработчик сохраняет
    максимальное количество фото (10), иначе обработчик сохраняет количество фото, введенное пользователем, вызывает
    функцию send_hotels_info и сбрасывает состояние пользователя
    """

    with bot.retrieve_data(message.chat.id) as data:
        if not message.text.isdigit() or int(message.text) <= 0:
            bot.send_message(message.chat.id,
                             'Ошибка! Количество фотографий, которые необходимо вывести для каждого найденного отеля '
                             'должно быть числом больше 0,\nПовторите ввод')
        else:
            logger.info('user input photos amount: {photos_amount}'.format(
                photos_amount=message.text
            ))
            if int(message.text) > 10:
                data['users_photos_amount'] = 10
            else:
                data['users_photos_amount'] = int(message.text)
            send_hotels_info(data)
    bot.delete_state(message.chat.id)