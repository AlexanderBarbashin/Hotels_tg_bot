from typing import Dict

from loguru import logger
from requests import Response, codes, get


def requests_to_api(url: str, headers: Dict, querystring: Dict) -> Response | str:
    """
    Функция для выполнения поискового запроса на веб-страницу. Посылает запрос, если ответ получен, возвращает его.
    Иначе возвращает сообщение об ошибке
    """

    try:
        answer = get(url, headers=headers, params=querystring, timeout=100)
        logger.info('get answer from request: {answer}'.format(
            answer=answer
        ))
        if answer.status_code == codes.ok:
            return answer
    except Exception as exc:
        logger.exception(exc)
        return 'Ошибка! Ответ от веб-страницы не получен!'
