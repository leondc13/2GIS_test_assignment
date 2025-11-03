import requests
import settings

def build_route(start, end):
    """
    Запрос к API 2GIS для построения маршрута на автомобиле
    между двумя точками (lon, lat)
    """
    if not settings.API_KEY:
        raise ValueError("API_KEY не задан в settings.py")

    payload = {
        "points": [
            {"type": "stop", "lon": start[0], "lat": start[1]},
            {"type": "stop", "lon": end[0], "lat": end[1]}
        ],
        "transport": "driving",
        "route_mode": "fastest"
    }

    params = {"key": settings.API_KEY}

    response = requests.post(settings.BASE_URL_ROUTE, params=params, json=payload)
    return response
