from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def photos_need_markup() -> InlineKeyboardMarkup:
    """
    Клавиатура с клавишами Да и Нет для получения от пользователя ответа на запрос о необходимости вывода фото для
    каждого найденного отеля. При нажатии клавиши передает соответствующий ответ
    """

    answers = ['Да', 'Нет']
    buttons = InlineKeyboardMarkup()
    for answer in answers:
        buttons.add(InlineKeyboardButton(text=answer,
                                         callback_data=answer))
    return buttons
