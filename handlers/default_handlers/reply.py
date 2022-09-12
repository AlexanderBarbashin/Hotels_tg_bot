from telebot.types import Message

from loader import bot


@bot.message_handler(state=None)
def bot_reply(message: Message) -> None:
    """Обработчик сообщений, не являющихся командами"""

    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет {user_name}!'.format(
            user_name = message.from_user.full_name
        ))
    else:
        bot.reply_to(message, 'Такой команды не существует')
