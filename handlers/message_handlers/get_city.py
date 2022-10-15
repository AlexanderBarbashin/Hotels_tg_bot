from telebot.types import Message
from loader import bot
from states.user_states import UserState

@bot.message_handler(commands=['lowprice', 'highprice'])
def get_city(message: Message) -> None:
    """
    Обработчик команд /lowprice и /highprice. Устанавливает состояние пользователя users_cities_dict, сбрасывает
    информацию пользователя, сохраняет метод поиска отелей для пользователя (по возрастанию или убыванию цены) и
    запрашивает у пользователя название города, в котором будет происходить поиск отелей
    """

    bot.set_state(message.chat.id, UserState.users_cities_dict)
    bot.reset_data(message.chat.id)
    with bot.retrieve_data(message.chat.id) as data:
        if message.text == '/lowprice':
            data['sort_order'] = 'PRICE'
        else:
            data['sort_order'] = 'PRICE_HIGHEST_FIRST'
    bot.send_message(message.chat.id, 'Введите название города, в котором вы хотите выполнить поиск отеля')