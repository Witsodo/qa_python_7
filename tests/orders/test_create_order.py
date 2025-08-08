import pytest
import allure
from tests.test_data import OrderData

@allure.feature("API: Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа с разными вариантами цветов")
    @pytest.mark.parametrize("colors,expected_colors", [
        (["BLACK"], ["BLACK"]),
        (["GREY"], ["GREY"]),
        (["BLACK", "GREY"], ["BLACK", "GREY"]),
        ([], []),
        (None, ["BLACK"])  # Дефолтное значение при отсутствии цвета
    ], ids=[
        "black_color",
        "grey_color",
        "both_colors",
        "empty_array",
        "no_color_specified"
    ])
    def test_create_order_with_colors(self, order_client, colors, expected_colors):
        with allure.step("Подготовка тестовых данных"):
            order_data = OrderData.valid()
            if colors is not None:
                order_data["color"] = colors

        with allure.step("Отправка запроса на создание заказа"):
            response = order_client.create(order_data)

        with allure.step("Проверка ответа"):
            assert response.status_code == 201
            assert isinstance(response.json()["track"], int)

        with allure.step("Проверка сохранения цветов"):
            order_response = order_client.get_by_track(response.json()["track"])
            assert set(order_response.json()["order"]["color"]) == set(expected_colors)

    @allure.title("Проверка наличия track номера")
    def test_response_contains_track(self, order_client):
        with allure.step("Создание тестового заказа"):
            order_data = OrderData.valid()
            response = order_client.create(order_data)

        with allure.step("Проверка ответа"):
            assert "track" in response.json()
            assert isinstance(response.json()["track"], int)