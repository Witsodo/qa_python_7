import requests
import allure
from data.urls import Endpoints

class CourierClient:
    def __init__(self):
        pass

    @allure.step("Создание курьера")
    def create(self, data):
        return requests.post(Endpoints.COURIER, json=data)

    @allure.step("Авторизация курьера")
    def login(self, login, password):
        return requests.post(Endpoints.COURIER_LOGIN,
                             json={"login": login, "password": password})

    @allure.step("Удаление курьера по ID")
    def delete(self, courier_id):
        # Если courier_id пустой (None или ""), отправляем запрос без ID
        url = Endpoints.COURIER_ID.format(courier_id=courier_id) if courier_id else Endpoints.COURIER
        return requests.delete(url)
