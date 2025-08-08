import requests
import allure

class OrderClient:
    def __init__(self, base_url):
        self.base_url = base_url

    @allure.step("Создание заказа")
    def create(self, data):
        return requests.post(f"{self.base_url}/orders", json=data)

    @allure.step("Получение заказа по трек-номеру")
    def get_by_track(self, track):
        return requests.get(f"{self.base_url}/orders/track", params={"t": track})

    @allure.step("Принятие заказа курьером")
    def accept(self, order_id, courier_id):
        return requests.put(
            f"{self.base_url}/orders/accept/{order_id}",
            params={"courierId": courier_id}
        )

    @allure.step("Завершение заказа")
    def finish(self, order_id):
        return requests.put(f"{self.base_url}/orders/finish/{order_id}")

    @allure.step("Отмена заказа")
    def cancel(self, track):
        return requests.put(f"{self.base_url}/orders/cancel", json={"track": track})

    @allure.step("Получение списка заказов")
    def get_list(self, **params):
        return requests.get(f"{self.base_url}/orders", params=params)