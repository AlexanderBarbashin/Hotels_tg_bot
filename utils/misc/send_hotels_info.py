from utils.request_to_api import requests_to_api
from config_data.config import headers
from re import search
from json import loads
from loader import bot
from typing import Dict
from telebot.types import InputMediaPhoto


def send_hotels_info(data: Dict) -> None:
    """
    Функция для вывода на экран основной информации о каждом отеле, найденном в результате поиска, и фото для каждого
    отеля (в случае положительного ответа пользователя на соответствующий запрос). После вывода информации очищает
    данные пользователя для возможности последующих поисков
    """
    users_hotels_list = []
    for num in range(data['users_hotels_amount'] // 25 + 1):
        current_page_size = 25 if data['users_hotels_amount'] - 25 * num > 25 else data['users_hotels_amount'] - \
                                                                                   25 * num
        hotels_url = "https://hotels4.p.rapidapi.com/properties/list"
        hotels_querystring = {'destinationId': '{city_id}'.format(city_id=data['users_city_id']),
                              'pageNumber': '{page_num}'.format(page_num=num + 1),
                              'pageSize': '{page_size}'.format(page_size=current_page_size),
                              'checkIn': '{check_in_date}'.format(check_in_date=data['check_in_date']),
                              'checkOut': '{check_out_date}'.format(check_out_date=data['check_out_date']),
                              'adults1': '1', 'sortOrder': 'PRICE', 'locale': 'ru_RU', 'currency': 'RUB'}
        hotels_request = requests_to_api(hotels_url, headers, hotels_querystring)
        pattern = r'(?<=,"results":).+?(?=,"pagination)'
        find = search(pattern, hotels_request.text)
        if find:
            hotels_list = loads(find[0])
            users_hotels_list.extend(hotels_list)
        else:
            bot.send_message(data['users_chat_id'], 'По вашему запросу ничего не найдено. Попробуйте еще раз')
    for i_hotel in users_hotels_list:
        hotel_info = ['=' * 50]
        price = i_hotel.get('ratePlan', {}).get('price', {}).get('exactCurrent', 'Информация не найдена')
        total_price = round(price * (data['check_out_date'] - data['check_in_date']).days) \
            if type(price) in (int, float) \
            else 'Информация не найдена'
        hotel_info.extend(['Название отеля: {name}'.format(name=i_hotel.get('name', 'Информация не найдена')),
                           'Количество звезд: {rate}'.format(rate=i_hotel.get('starRating', 'Информация не найдена')),
                           'Адрес отеля: {address}'.format(address=i_hotel.get('address', {}).get(
                               'streetAddress', 'Информация не найдена')),
                           'Расстояние от центра: {distance_from_center}'.format(
                               distance_from_center=i_hotel.get('landmarks', {})[0].get(
                                   'distance', 'Информация не найдена'),
                           ),
                           'Цена за сутки: {price} RUB'.format(price=price),
                           'Итоговая цена: {total_price} RUB'.format(
                               total_price=total_price),
                           'Веб-сайт отеля: https://hotels.com/ho{hotel_id}'.format(hotel_id=i_hotel['id'])]
                          )
        bot.send_message(data['users_chat_id'], ('\n').join(hotel_info), disable_web_page_preview=True)
        if 'users_photos_amount' in data:
            photos_url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
            photos_querystring = {'id': '{hotel_id}'.format(hotel_id=i_hotel['id'])}
            photos_request = requests_to_api(photos_url, headers, photos_querystring)
            pattern = r'(?<=,"hotelImages":).+?(?=,"roomImages)'
            find = search(pattern, photos_request.text)
            if find:
                photos_list = loads(find[0])
                photos_group = []
                for num in range(data['users_photos_amount']):
                    photo_url = photos_list[num]['baseUrl'].format(size=photos_list[num]['sizes'][0]['suffix'])
                    photos_group.append(InputMediaPhoto(photo_url))
                bot.send_media_group(data['users_chat_id'], photos_group)
            else:
                bot.send_message(data['users_chat_id'], 'По вашему запросу ничего не найдено. Попробуйте еще раз')
    data.clear()
