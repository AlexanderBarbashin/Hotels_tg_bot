from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['hello_world'])
def bot_hello_world(message: Message) -> None:
    """Обработчик команды /hello-world. Выводит на экран сообщение 'Привет мир!'"""

    bot.send_message(message.from_user.id, 'Привет мир!')

