import requests
import allure

class CourierClient:
    def __init__(self, base_url):
        self.base_url = base_url

    @allure.step("Создание курьера")
    def create(self, data):
        return requests.post(f"{self.base_url}/courier", json=data)

    @allure.step("Авторизация курьера")
    def login(self, login, password):
        return requests.post(f"{self.base_url}/courier/login",
                             json={"login": login, "password": password})

    @allure.step("Удаление курьера по ID")
    def delete(self, courier_id):
        # Если courier_id пустой (None или ""), отправляем запрос без ID
        if not courier_id:
            return requests.delete(f"{self.base_url}/courier")

        return requests.delete(f"{self.base_url}/courier/{courier_id}")
