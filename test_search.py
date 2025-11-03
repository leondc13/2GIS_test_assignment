import pytest
import allure
import settings
from search_api import search_places

@allure.title("Позитивный тест — поиск кафе (тип branch) рядом с Кремлем")
def test_search_places_success():
    lon, lat = 37.617635, 55.755814
    response = search_places("кафе", lon, lat, type="branch")

    allure.attach(str(response.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
    assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

    data = response.json()
    allure.attach(str(data), name="Ответ API", attachment_type=allure.attachment_type.JSON)

    assert "result" in data and "items" in data["result"], "Нет поля result.items"
    items = data["result"]["items"]
    assert len(items) > 0, "Ответ не содержит объектов"

    first_item = items[0]
    assert "id" in first_item, "Нет поля id"
    assert "type" in first_item, "Нет поля type"
    assert first_item["type"] == "branch", "Тип объекта не branch"
    assert "name" in first_item, "Нет поля name"


@allure.title("Позитивный тест — поиск с дополнительными полями fields")
def test_search_places_with_fields():
    lon, lat = 37.617635, 55.755814
    fields = (
        "items.org,items.rubrics,items.name_ex,"
        "items.locale,items.schedule,items.schedule_special"
    )

    response = search_places("кафе", lon, lat, type="branch", fields=fields)

    allure.attach(str(response.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
    assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

    data = response.json()
    allure.attach(str(data), name="Ответ API", attachment_type=allure.attachment_type.JSON)
    items = data["result"]["items"]
    assert len(items) > 0, "Ответ не содержит объектов"

    first_item = items[0]
    assert first_item["type"] == "branch", "Тип объекта не branch"

    # Проверка обязательных полей для branch
    for field in ["org", "rubrics", "name_ex", "locale"]:
        assert field in first_item, f"Нет поля {field} в ответе для branch"

    # Проверка расписания
    assert "schedule" in first_item or "schedule_special" in first_item, \
        "Нет поля расписания (schedule или schedule_special)"

@allure.title("Негативный тест — запрос без ключа API")
def test_search_places_no_api_key(monkeypatch):
    monkeypatch.setattr(settings, "API_KEY", "")
    with pytest.raises(ValueError):
        search_places("кафе", 37.617635, 55.755814)
