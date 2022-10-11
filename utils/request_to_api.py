from requests import get, codes, Response
from typing import Dict


def requests_to_api(url: str, headers: Dict, querystring: Dict) -> Response | str:
    """
    Функция для выполнения поискового запроса на веб-страницу. Посылает запрос, если ответ получен, возвращает его.
    Иначе возвращает None
    """

    try:
        answer = get(url, headers=headers, params=querystring, timeout=100)
        if answer.status_code == codes.ok:
            return answer
    except:
        return 'Ошибка! Ответ от веб-страницы не получен!'
