from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def found_cities_markup(cities_list: list) -> InlineKeyboardMarkup:
    """
    Клавиатура с названиями городов, найденных в результате поискового запроса. При нажатии клавиши передает id
    соответствующего города
    """

    cities = {}
    for i_city in cities_list:
        caption = i_city['caption'].split(', ')
        country_name = caption[-1]
        cities[i_city['destinationId']] = '{city_name}, {country_name}'.format(
            city_name=i_city['name'],
            country_name=country_name
        )
    buttons = InlineKeyboardMarkup()
    for i_id, i_city in cities.items():
        buttons.add(InlineKeyboardButton(text=i_city,
                                         callback_data=i_id))
    return buttons
