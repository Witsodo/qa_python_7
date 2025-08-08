import pytest
import allure
from tests.test_data import CourierData

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
            assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Проверка валидации полей")
    @pytest.mark.parametrize("login,password,expected_msg", [
        ("", "valid_pass", "Недостаточно данных для входа"),     # Пустой логин
        ("valid_login", "", "Недостаточно данных для входа"),    # Пустой пароль
        ("", "", "Недостаточно данных для входа")               # Все поля пустые
    ])
    def test_missing_or_empty_fields(self, courier_client, login, password, expected_msg):
        with allure.step(f"Отправка запроса с login='{login}', password='{password}'"):
            response = courier_client.login(
                login=login,
                password=password
            )

        with allure.step("Проверка ошибки"):
            assert response.status_code == 400
            assert response.json()["message"] == expected_msg