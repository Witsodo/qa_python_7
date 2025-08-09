import pytest
import allure
from data.test_data import ServerResponses

@allure.feature("API: Авторизация курьера")
class TestLoginCourier:
    @allure.title("Успешная авторизация")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_success(self, courier_client, registered_courier):
        with allure.step("Отправка запроса с валидными данными"):
            response = courier_client.login(
                registered_courier["login"],
                registered_courier["password"]
            )

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Неверные учетные данные")
    def test_invalid_credentials(self, courier_client, registered_courier):
        with allure.step("Отправка запроса с неверным паролем"):
            response = courier_client.login(
                login=registered_courier["login"],
                password="wrong_password"
            )

        with allure.step("Проверка ошибки"):
            assert response.status_code == 404
            assert response.json()["message"] == ServerResponses.COURIER.ACCOUNT_NOT_FOUND

    @allure.title("Проверка валидации полей")
    @pytest.mark.parametrize("login,password", [
        ("", "valid_pass"),
        ("valid_login", ""),
        ("", "")
    ])
    def test_missing_fields(self, courier_client, login, password):
        response = courier_client.login(login, password)
        assert response.status_code == 400
        assert response.json()["message"] == ServerResponses.COURIER.NOT_ENOUGH_DATA_FOR_LOGIN