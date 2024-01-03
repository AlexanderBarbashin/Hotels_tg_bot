from datetime import datetime, timedelta

from loguru import logger
from telebot.types import CallbackQuery
from telegram_bot_calendar import LSTEP, DetailedTelegramCalendar

from keyboards.inline.photos_need_markup import photos_need_markup
from loader import bot
from states.user_states import UserState


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def choose_users_dates(callback_date_info: CallbackQuery) -> None:
    """
    Обработчик информации с клавиш, нажатых пользователем при выборе дат заселения в отель и выселения из отеля.
    Сохраняет дату заселения в отель, введенную пользователем с клавиатуры, запрашивает у пользователя дату выселения из
    отеля, отправляет пользователю клавиатуру в виде календаря, сохраняет дату выселения из отеля, запрашивает у
    пользователя необходимость вывода фото для каждого найденного отеля и устанавливает состояние пользователя
    photos_need
    """

    current_date = datetime.now().date()
    with bot.retrieve_data(callback_date_info.message.chat.id) as data:
        if 'check_in_date' in data:
            current_date = data['check_in_date'] + timedelta(days=1)
    result, key, step = DetailedTelegramCalendar(min_date=current_date).process(callback_date_info.data)
    if not result and key:
        bot.edit_message_text('Выберите {step}'.format(step=LSTEP[step]),
                              callback_date_info.message.chat.id,
                              callback_date_info.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text('Вы выбрали {result}'.format(result=result),
                              callback_date_info.message.chat.id,
                              callback_date_info.message.message_id)
        with bot.retrieve_data(callback_date_info.message.chat.id) as data:
            if 'check_in_date' not in data:
                logger.info('user input check in date: {check_in_date}'.format(
                    check_in_date=result
                ))
                data['check_in_date'] = result
                calendar, step = DetailedTelegramCalendar(locale='ru', min_date=current_date).build()
                bot.send_message(callback_date_info.message.chat.id, 'Введите дату выселения из отеля',
                                 reply_markup=calendar)
            else:
                logger.info('user input check out date: {check_out_date}'.format(
                    check_out_date=result
                ))
                data['check_out_date'] = result
                bot.send_message(callback_date_info.message.chat.id,
                                 'Вы хотите вывести на экран фотографии для каждого найденного отеля ?',
                                 reply_markup=photos_need_markup())
                bot.set_state(callback_date_info.message.chat.id, UserState.photos_need)
