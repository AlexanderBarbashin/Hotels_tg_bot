from peewee import *

db = SqliteDatabase('database/search_history.db')


class BaseModel(Model):
    """
    Класс базовая модель. Родитель: Model

    Attributes:
        id (PrimaryKeyField): поле с уникальными id пользователей, которые присваиваются автоматически
    """

    id = PrimaryKeyField(unique=True)

    class Meta:
        """
        Класс Meta. Содержит единые метаданные для каждой таблицы класса

        Attributes:
            database (db): база данных
            order_by (str): поле для сортировки по умолчанию
        """

        database = db
        order_by = 'id'


class User(BaseModel):
    """
    Класс пользователь. Родитель: BaseModel

    Attributes:
        user_name (CharField): поле с именами пользователей
        user_tg_id (IntegerField): поле с id Telegram пользователей
        is_relative (BooleanField): поле со значениями параметра is_relative пользователей

    """
    user_name = CharField()
    user_tg_id = IntegerField()
    is_relative = BooleanField()

    class Meta:
        """
        Класс Meta. Содержит единые метаданные для каждой таблицы класса

        Attributes:
            db_table (str): название таблицы
        """

        db_table = 'users'


class SearchRequest(BaseModel):
    """
    Класс поисковый запрос. Родитель: BaseModel

    Attributes:
        author (ForeignKeyField): поле с id пользователей, создавших поисковые запросы
        command (CharField): поле с командами, которые вводили пользователи
        command_datetime (DateTimeField): поле с датами и временами поисковых запросов пользователей
        city (CharField): поле с названиями городов, в которых пользователи выполняли поиск отелей
        hotels_list (TextField): поле с названиями отелей, найденных в результате выполнения поисковых запросов
    """

    author = ForeignKeyField(User, related_name='requests')
    command = CharField()
    command_datetime = DateTimeField()
    city = CharField()
    hotels_list = TextField()

    class Meta:
        """
        Класс Meta. Содержит единые метаданные для каждой таблицы класса

        Attributes:
            db_table (str): название таблицы
        """

        db_table = 'search_requests'

User.create_table()
SearchRequest.create_table()