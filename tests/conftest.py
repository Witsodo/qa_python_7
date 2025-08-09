import pytest
import allure
import json
from requests.exceptions import RequestException, HTTPError
from clients.courier_client import CourierClient
from clients.order_client import OrderClient
from data.test_data import CourierData, OrderData

#Фикстуры клиентов
@pytest.fixture
def courier_client():
    with allure.step("Инициализация клиента для работы с API курьеров"):
        return CourierClient()

@pytest.fixture
def order_client():
    with allure.step("Инициализация клиента для работы с API заказов"):
        return OrderClient()

#Фикстуры данных
@pytest.fixture
def registered_courier(courier_client):
    with allure.step("Создание тестового курьера"):
        courier_data = CourierData.valid()
        try:
            response = courier_client.create(courier_data)
            response.raise_for_status()  #для статусов 4xx/5xx
        except RequestException as e:
            # Ловим:
            # - таймауты (requests.Timeout)
            # - проблемы с соединением (requests.ConnectionError)
            # - другие ошибки библиотеки requests
            pytest.fail(f"Ошибка создания курьера: {str(e)}", pytrace=False)

        yield courier_data

        with allure.step("Удаление тестового курьера"):
            try:
                # Получаем ID курьера для удаления
                login_resp = courier_client.login(
                    courier_data["login"],
                    courier_data["password"]
                )
                login_resp.raise_for_status()
                courier_id = login_resp.json()["id"]

                # Удаляем курьера
                delete_resp = courier_client.delete(courier_id)
                delete_resp.raise_for_status()

            except HTTPError as e:
                # Обрабатываем HTTP ошибки
                allure.attach(
                    f"HTTP ошибка при удалении курьера ({e.response.status_code}): {str(e)}",
                    name="Cleanup HTTP Warning"
                )
            except json.JSONDecodeError as e:
                # Ошибка парсинга JSON ответа
                allure.attach(
                    f"Ошибка формата ответа сервера: {str(e)}",
                    name="Cleanup JSON Parse Warning"
                )
            except KeyError as e:
                # Отсутствие ожидаемого поля в JSON
                allure.attach(
                    f"Неверная структура ответа: отсутствует поле {str(e)}",
                    name="Cleanup Response Structure Warning"
                )
            except RequestException as e:
                # Сетевые проблемы при выполнении запроса
                allure.attach(
                    f"Проблема соединения при удалении: {str(e)}",
                    name="Cleanup Network Warning"
                )

@pytest.fixture
def created_order(order_client):
    with allure.step("Создание тестового заказа"):
        order_data = OrderData.valid()
        try:
            response = order_client.create(order_data)
            response.raise_for_status()
            track = response.json()["track"]
        except RequestException as e:
            # Проблемы сети/соединения при создании заказа
            pytest.fail(f"Сетевая ошибка при создании заказа: {str(e)}", pytrace=False)
        except json.JSONDecodeError as e:
            # Невалидный JSON в ответе
            pytest.fail(f"Ошибка разбора ответа сервера: {str(e)}", pytrace=False)
        except KeyError as e:
            # Нет поля 'track' в ответе
            pytest.fail(f"Некорректный ответ сервера: отсутствует track-номер", pytrace=False)

    yield track

    with allure.step("Отмена тестового заказа"):
        try:
            response = order_client.cancel(track)
            response.raise_for_status()
        except HTTPError as e:
            # Обрабатываем специфичные HTTP ошибки при отмене
            if e.response.status_code == 409:
                allure.attach("Заказ уже был отменен", name="Cancel Warning")
            else:
                allure.attach(
                    f"HTTP ошибка при отмене заказа: {e.response.status_code}",
                    name="Cancel HTTP Warning"
                )
        except RequestException as e:
            # Общие сетевые проблемы при отмене
            allure.attach(
                f"Ошибка соединения при отмене заказа: {str(e)}",
                name="Cancel Network Warning"
            )