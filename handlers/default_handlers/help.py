from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    """Обработчик команды /help. Выводит на экран список основных команд"""

    text = ['/{command} - {desk}'.format(
        command=command,
        desk=desk
    ) for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.from_user.id, '\n'.join(text))
