import requests
import allure
from data.urls import Endpoints

class OrderClient:
    def __init__(self):
        pass

    @allure.step("Создание заказа")
    def create(self, data):
        return requests.post(Endpoints.ORDERS, json=data)

    @allure.step("Получение заказа по трек-номеру")
    def get_by_track(self, track):
        return requests.get(Endpoints.ORDERS_TRACK, params={"t": track})

    @allure.step("Принятие заказа курьером")
    def accept(self, order_id, courier_id):
        return requests.put(
            Endpoints.ORDERS_ACCEPT.format(order_id=order_id),
            params={"courierId": courier_id}
        )

    @allure.step("Завершение заказа")
    def finish(self, order_id):
        return requests.put(Endpoints.ORDERS_FINISH.format(order_id=order_id))

    @allure.step("Отмена заказа")
    def cancel(self, track):
        return requests.put(Endpoints.ORDERS_CANCEL, json={"track": track})

    @allure.step("Получение списка заказов")
    def get_list(self, **params):
        return requests.get(Endpoints.ORDERS, params=params)