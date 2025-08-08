import pytest
import allure

@allure.feature("API: Получение списка заказов")
class TestGetOrders:
    @allure.title("Получение списка заказов")
    def test_get_orders_returns_list(self, order_client):
        with allure.step("Отправка запроса на получение списка заказов"):
            response = order_client.get_list()

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert isinstance(response.json()["orders"], list)
            assert len(response.json()["orders"]) > 0

        with allure.step("Проверка структуры заказа"):
            first_order = response.json()["orders"][0]
            assert "id" in first_order
            assert "firstName" in first_order
            assert "lastName" in first_order
            assert "address" in first_order
            assert "phone" in first_order

    @allure.title("Проверка параметра limit")
    @pytest.mark.parametrize("limit", [1, 5, 10])
    def test_limit_parameter(self, order_client, limit):
        with allure.step(f"Отправка запроса с limit={limit}"):
            response = order_client.get_list(limit=limit)

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert len(response.json()["orders"]) <= limit
            assert response.json()["pageInfo"]["limit"] == limit

    @allure.title("Проверка пагинации")
    def test_pagination(self, order_client):
        with allure.step("Получение первой страницы"):
            first_page = order_client.get_list(limit=1, page=0)

        with allure.step("Получение второй страницы"):
            second_page = order_client.get_list(limit=1, page=1)

        with allure.step("Проверка различий в результатах"):
            assert first_page.status_code == 200
            assert second_page.status_code == 200
            assert first_page.json()["orders"][0]["id"] != second_page.json()["orders"][0]["id"]