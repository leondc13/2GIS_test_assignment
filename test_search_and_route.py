import pytest
import allure
import search_api
import routing_api

@allure.title("Интеграционный тест — поиск ближайшей АЗС и построение маршрута к ней")
def test_search_gas_station_and_build_route():
    # Имитация текущего положения пользователя
    user_location = (37.617635, 55.755814)  # Кремль

    # Поиск ближайшей АЗС
    with allure.step("Поиск ближайшей автозаправки"):
        response = search_api.search_places("АЗС", user_location[0], user_location[1], limit=1, fields="items.point", sort="distance")
        allure.attach(str(response.status_code), "HTTP статус поиска", allure.attachment_type.TEXT)
        assert response.status_code == 200, f"Ошибка при поиске АЗС: {response.status_code}"

        data = response.json()
        allure.attach(str(data), "Ответ поиска", allure.attachment_type.JSON)
        assert "result" in data, "Нет ключа 'result' в ответе поиска"
        assert len(data["result"]["items"]) > 0, "Не найдено ни одной АЗС поблизости"

        station = data["result"]["items"][0]
        station_name = station.get("name", "Без названия")
        station_point = station.get("point", {})
        lon, lat = station_point.get("lon"), station_point.get("lat")

        allure.attach(f"{station_name} ({lon}, {lat})", "Найденная АЗС", allure.attachment_type.TEXT)

    # Построение маршрута
    with allure.step(f"Построение маршрута до '{station_name}'"):
        response = routing_api.build_route(start=user_location, end=(lon, lat))
        allure.attach(str(response.status_code), "HTTP статус маршрута", allure.attachment_type.TEXT)
        assert response.status_code == 200, f"Ошибка при построении маршрута: {response.status_code}"

        data = response.json()
        allure.attach(str(data), "Ответ маршрута", allure.attachment_type.JSON)
        assert data.get("status") == "OK", f"Ошибка маршрутизации: {data.get('status')}"
        assert "result" in data, "Нет ключа 'result' в ответе маршрута"

        route = data["result"][0]
        assert route["total_distance"] > 0, "Маршрут имеет нулевую длину"
        assert route["total_duration"] > 0, "Маршрут имеет нулевую длительность"

    allure.dynamic.description(f"Маршрут построен от пользователя до ближайшей АЗС: {station_name}")
