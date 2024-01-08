# AngerranTravelbot

Телеграм бот для подбора отелей. Анализирует текущие предложения по отелям и с учетом критериев, введенных пользователем, выдает наиболее подходящие.
В работе использует Rapid Api

## Особенности

* Возможность настройки выводимых результатов, например, количества искомых отелей, необходимость вывода фотографий отелей и их количества
* Сохранение поисковых запросов в базу данных и возможность вывода на экран истории поиска с разбивкой для каждого пользователя

## Доступные команды

* **/start** – запуск бота
* **/help** – вывод основных команд
* **/lowprice** – вывод топа самых дешевых отелей в городе
* **/highprice** – вывод топа самых дорогих отелей в городе
* **/bestdeal** – вывод топа отелей, находящихся в заданном диапазоне цен и расстояний от центра города
* **/history** – вывод истории поиска отелей

## Использованные технологии

* Python 3
* PyTelegramBotApi(telebot)

## Подготовка и запуск

1.	Установить интерпретатор Python версии 3.10 и пакеты, перечисленные в файле requirements.txt
2.	Создать своего бота с помощью бота @BotFather и сохранить свой токен
3.	Создать учетную запись на сайте rapidapi.com и сохранить X-RapidAPI-Key, X-RapidAPI-Host
4.	Создать файл .env в директории программы, сохранить туда токен, X-RapidAPI-Key, X-RapidAPI-Host по примеру в файле .env.template
5.	Запустить файл main.py в директории программы




