from loguru import logger
from telebot.types import CallbackQuery

from loader import bot
from states.user_states import UserState
from utils.misc.send_hotels_info import send_hotels_info


@bot.callback_query_handler(func=None, state=UserState.photos_need)
def choose_photos_need(photos_need_callback: CallbackQuery) -> None:
    """
    Обработчик информации с клавиш, нажатых пользователем при выборе необходимости вывода фото для каждого найденного
    отеля. Сохраняет id чата с пользователем. В случае положительного ответа пользователя запрашивает у него количество
    фото, которые необходимо вывести для каждого найденного отеля (не более 10), и устанавливает состояние пользователя
    photos_amount, иначе вызывает функцию send_hotels_info и сбрасывает состояние пользователя
    """

    logger.info('user choose photos need: {photos_need}'.format(
        photos_need=photos_need_callback.data
    ))
    with bot.retrieve_data(photos_need_callback.message.chat.id) as data:
        data['users_chat_id'] = photos_need_callback.message.chat.id
    result = photos_need_callback.data
    if result == 'Да':
        bot.send_message(photos_need_callback.message.chat.id,
                         'Введите количество фотографий для каждого найденного отеля, которое необходимо вывести'
                         ' (не более 10)')
        bot.set_state(photos_need_callback.message.chat.id, UserState.photos_amount)
    else:
        send_hotels_info(data)
        bot.delete_state(photos_need_callback.message.chat.id)
