from telebot.types import Message
from loader import bot
from states.user_states import UserState

@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def get_city(message: Message) -> None:
    """
    Обработчик команд /lowprice, /highprice и /bestdeal. Устанавливает состояние пользователя users_cities_dict,
    сбрасывает информацию пользователя, сохраняет введенную пользователем команду (из трех возможных вариантов) и
    запрашивает у пользователя название города, в котором будет происходить поиск отелей
    """

    bot.set_state(message.chat.id, UserState.users_cities_dict)
    bot.reset_data(message.chat.id)
    with bot.retrieve_data(message.chat.id) as data:
        data['command'] = message.text[1:]
    bot.send_message(message.chat.id, 'Введите название города, в котором вы хотите выполнить поиск отеля')