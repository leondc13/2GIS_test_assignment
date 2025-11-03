import requests
import settings

def search_places(query, lon, lat, limit=3, type=None, fields=None, sort=None):
    """
    Выполняет запрос к API поиска 2GIS.
    :param query: строка поиска, например "кафе"
    :param lon: долгота
    :param lat: широта
    :param limit: количество результатов
    :param type: тип объекта, например "branch"
    :param fields: дополнительные поля (строка через запятую)
    """
    if not settings.API_KEY:
        raise ValueError("Отсутствует API ключ")

    params = {
        "q": query,
        "point": f"{lon},{lat}",
        "radius": 3000,
        "limit": limit,
        "key": settings.API_KEY,
    }

    if type:
        params["type"] = type
    if fields:
        params["fields"] = fields

    response = requests.get(settings.BASE_URL_SEARCH, params=params)
    return response
