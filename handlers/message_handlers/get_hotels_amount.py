from loader import bot
from states.user_states import UserState
from telebot.types import Message
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import datetime

@bot.message_handler(state=UserState.hotels_amount)
def get_hotels_amount(message: Message) -> None:
    """
    Обработчик введенного пользователем количества отелей, которые необходимо вывести в результате поиска (не более 40),
    в состоянии пользователя hotels_amount. Если сообщение пользователя не является числом или не больше 0, пользователю
    отправляется соответствующее сообщение. Если сообщение пользователя больше 40, обработчик сохраняет максимальное
    количество отелей (40), иначе обработчик сохраняет количество отелей, введенное пользователем, запрашивает у
    пользователя дату заселения в отель и выводит на экран клавиатуру в виде календаря
    """
    with bot.retrieve_data(message.chat.id) as data:
        if not message.text.isdigit() or int(message.text) <= 0:
            bot.send_message(
                'Ошибка! Количество отелей, которые необходимо вывести в результате, должно быть числом больше 0!'
                ' Повторите ввод')
        else:
            if int(message.text) > 40:
                data['users_hotels_amount'] = 40
            else:
                data['users_hotels_amount'] = int(message.text)
            current_date = datetime.now().date()
            calendar, step = DetailedTelegramCalendar(locale='ru', min_date=current_date).build()
            bot.send_message(message.chat.id, 'Введите дату заселения в отель', reply_markup=calendar)