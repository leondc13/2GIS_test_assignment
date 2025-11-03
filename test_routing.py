import pytest
import allure
from routing_api import build_route

@allure.title("Позитивный тест — успешное построение маршрута в Москве")
def test_route_success():
    start = (37.617635, 55.755814)  # Москва, Кремль
    end = (37.588144, 55.733842)    # Парк Горького

    response = build_route(start, end)
    allure.attach(str(response.status_code), name="HTTP статус ответа", attachment_type=allure.attachment_type.TEXT)
    
    assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

    data = response.json()
    allure.attach(str(data), name="Ответ API", attachment_type=allure.attachment_type.JSON)

    assert data.get("status") == "OK", f"Статус API не OK: {data.get('status')}"
    assert "result" in data, "Нет поля 'result' в ответе"

    route = data["result"][0]
    assert route["total_distance"] > 0, "Длина маршрута равна 0"
    assert route["total_duration"] > 0, "Длительность маршрута равна 0"


@allure.title("Негативный тест — неправильные координаты")
def test_route_invalid_coordinates():
    start = (0.0, 0.0)
    end = (0.0, 0.0)

    response = build_route(start, end)
    data = response.json()
    allure.attach(str(response.status_code), name="HTTP статус ответа", attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(data), name="Ответ API", attachment_type=allure.attachment_type.JSON)

    # 2GIS возвращает status != OK или ошибку
    assert data.get("status") != "OK", "API неожиданно вернул OK для неверных координат"


@allure.title("Негативный тест — запрос без ключа API")
def test_route_no_api_key(monkeypatch):
    import settings
    monkeypatch.setattr(settings, "API_KEY", "")

    with pytest.raises(ValueError) as exc_info:
        build_route((37.6, 55.7), (37.5, 55.8))
    allure.attach(str(exc_info.value), name="Сообщение ошибки", attachment_type=allure.attachment_type.TEXT)
