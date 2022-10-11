from loader import bot
from states.user_states import UserState
from telebot.types import CallbackQuery


@bot.callback_query_handler(func=None, state=UserState.choose_city)
def choose_city(callback_city_info: CallbackQuery) -> None:
    """
    Обработчик информации с клавиши, нажатой пользователем при выборе наиболее подходящего города из списка найденных
    в состоянии choose_city. Сохраняет id выбранного пользователем города, запрашивает у пользователя количество
    отелей, которые необходимо вывести в результате поиска и устанавливает состояние пользователя hotels_amount
    """

    with bot.retrieve_data(callback_city_info.message.chat.id) as data:
        data['users_city_id'] = callback_city_info.data
    bot.send_message(callback_city_info.message.chat.id,
                     'Введите количество отелей, которые необходимо вывести в результате (не более 40)')
    bot.set_state(callback_city_info.message.chat.id, UserState.hotels_amount)
