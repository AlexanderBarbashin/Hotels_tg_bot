from loguru import logger
from telebot.custom_filters import StateFilter

import handlers
from loader import bot
from utils.set_bot_commands import set_default_commands

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    logger.add('logs\logger.log',
               format='{time} {level} {message}', level='DEBUG', rotation='1 week', compression='zip')
    logger.error('Error')
    logger.info('Info')
    logger.warning('Warning')
    bot.infinity_polling()
