from telebot.types import Message
from loader import bot
from states.user_states import UserState

@bot.message_handler(commands=['lowprice'])
def get_city(message: Message) -> None:
    """
    Обработчик команды /lowprice. Запрашивает у пользователя название города, в котором будет происходить поиск
    отелей и устанавливает состояние пользователя users_cities_dict
    """

    bot.send_message(message.chat.id, 'Введите название города, в котором вы хотите выполнить поиск отеля')
    bot.set_state(message.chat.id, UserState.users_cities_dict)
