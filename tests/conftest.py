import pytest
import allure
from tests.clients.courier_client import CourierClient
from tests.clients.order_client import OrderClient
from tests.test_data import CourierData, OrderData

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


#Фикстуры клиентов
@pytest.fixture
def courier_client():
    with allure.step("Инициализация клиента для работы с API курьеров"):
        return CourierClient(BASE_URL)

@pytest.fixture
def order_client():
    with allure.step("Инициализация клиента для работы с API заказов"):
        return OrderClient(BASE_URL)

#Фикстуры данных
@pytest.fixture
def registered_courier(courier_client):
    with allure.step("Создание тестового курьера"):
        courier_data = CourierData.valid()
        response = courier_client.create(courier_data)
        assert response.status_code == 201

    yield courier_data

    with allure.step("Удаление тестового курьера"):
        try:
            login_resp = courier_client.login(
                courier_data["login"],
                courier_data["password"]
            )
            if login_resp.status_code == 200:
                courier_id = login_resp.json()["id"]
                courier_client.delete(courier_id)
        except Exception as e:
            allure.attach(f"Ошибка при удалении курьера: {str(e)}", name="Cleanup Error")


@pytest.fixture
def created_order(order_client):
    with allure.step("Создание тестового заказа"):
        order_data = OrderData.valid()
        response = order_client.create(order_data)
        assert response.status_code == 201
        track = response.json()["track"]

    yield track

    with allure.step("Отмена тестового заказа"):
        try:
            order_client.cancel(track)
        except Exception as e:
            allure.attach(f"Ошибка при отмене заказа: {str(e)}", name="Cleanup Error")