from typing import Dict

def hotels_filter(hotel: Dict, min_distance: float, max_distance: float) -> Dict | None:
    """
    Функция для фильтрования отелей по расстоянию от центра города. Если расстояние, на котором находится отель от
    центра города, находится в пределах диапазона расстояний, введенного пользователем, функция возвращает отель; иначе
    возвращает None
    """

    distance_from_center_str = hotel['landmarks'][0]['distance'].split()[0]
    distance_from_center = float(distance_from_center_str.replace(',', '.'))
    if min_distance <= distance_from_center <= max_distance:
        return hotel
    return None

