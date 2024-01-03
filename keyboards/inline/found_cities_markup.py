from typing import Dict

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def found_cities_markup(cities_dict: Dict) -> InlineKeyboardMarkup:
    """
    Клавиатура с названиями городов, найденных в результате поискового запроса. При нажатии клавиши передает текст с id
    соответствующего города
    """

    buttons = InlineKeyboardMarkup()
    for i_id, i_city in cities_dict.items():
        buttons.add(InlineKeyboardButton(text=i_city,
                                         callback_data=i_id))
    return buttons
