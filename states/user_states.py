from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    """
    Класс Состояние пользователя. Родитель: StatesGroup

    Attributes:
        users_cities_dict (State): состояние пользователя, в котором ему необходимо ввести название города для поиска
                                   отеля
        choose_city (State): состояние пользователя, в котором ему необходимо выбрать наиболее подходящий город для
                             поиска отеля из предложенных вариантов
        hotels_amount (State): состояние пользователя, в котором ему необходимо ввести количество отелей, выводимых в
                               результате поиска
        photos_need (State): состояние пользователя, в котором ему необходимо выбрать, выводить ли на экран фото для
                             каждого найденного отеля
        photos_amount (State): состояние пользователя, в котором ему необходимо ввести количество фото, выводимых на
                               экран для каждого найденного отеля

    """

    users_cities_dict = State()
    choose_city = State()
    hotels_amount = State()
    photos_need = State()
    photos_amount = State()
