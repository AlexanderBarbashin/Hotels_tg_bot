from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """Обработчик команды /start. Выводит на экран приветственное сообщение"""

    bot.send_message(message.from_user.id, '''
Привет, {user_name}! Меня зовут AngerranTravelbot, я бот компании Too Easy Travel, созданный для подбора отелей.
Чтобы узнать, что я умею, введите "/help"
'''.format(
        user_name=message.from_user.full_name
    ))

