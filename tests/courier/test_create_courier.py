import pytest
import allure
from data.test_data import CourierData, ServerResponses

class TestCreateCourier:
    @allure.title("Успешное создание курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_success(self, courier_client):
        with allure.step("Подготовка тестовых данных"):
            data = CourierData.valid()

        with allure.step("Отправка запроса на создание курьера"):
            response = courier_client.create(data)

        with allure.step("Проверка ответа"):
            assert response.status_code == 201
            assert response.json() == ServerResponses.COURIER.CREATED

    @allure.title("Проверка обязательных полей")
    @pytest.mark.parametrize("field", ["login", "password"])
    def test_missing_field(self, courier_client, field):
        with allure.step(f"Подготовка данных без поля {field}"):
            data = CourierData.valid()
            del data[field]

        with allure.step("Отправка запроса"):
            response = courier_client.create(data)

        with allure.step("Проверка ошибки"):
            assert response.status_code == 400
            assert response.json()["message"] == ServerResponses.COURIER.NOT_ENOUGH_DATA_FOR_CREATE

    @allure.title("Проверка дублирования логина")
    def test_duplicate_login(self, courier_client, registered_courier):
        with allure.step("Подготовка данных с существующим логином"):
            data = CourierData.valid()
            data["login"] = registered_courier["login"]

        with allure.step("Отправка запроса"):
            response = courier_client.create(data)

        with allure.step("Проверка ошибки"):
            assert response.status_code == 409
            assert response.json()["message"] == ServerResponses.COURIER.LOGIN_ALREADY_EXISTS
