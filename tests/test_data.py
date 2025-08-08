import random
import string
import allure

@allure.step("Генерация случайной строки длиной {length}")
def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

@allure.feature("Тестовые данные")
class CourierData:

    @staticmethod
    @allure.step("Генерация валидных данных курьера")
    def valid():
        return {
            "login": f"test_{generate_random_string(8)}",
            "password": generate_random_string(10),
            "firstName": generate_random_string(8)
        }

class OrderData:
    @staticmethod
    @allure.step("Генерация валидных данных заказа")
    def valid():
        return {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "ул. Примерная, 1",
            "metroStation": "1",
            "phone": "+79991112233",
            "rentTime": 1,
            "deliveryDate": "2024-12-31",
            "comment": "Тестовый заказ",
            "color": ["BLACK"]  # Значение по умолчанию
        }
