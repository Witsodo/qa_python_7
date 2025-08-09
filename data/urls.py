
BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

class Endpoints:

    COURIER = f"{BASE_URL}/courier"
    COURIER_LOGIN = f"{BASE_URL}/courier/login"
    COURIER_ID = f"{BASE_URL}/courier/{{courier_id}}"
    ORDERS = f"{BASE_URL}/orders"
    ORDERS_TRACK = f"{BASE_URL}/orders/track"
    ORDERS_ACCEPT = f"{BASE_URL}/orders/accept/{{order_id}}"
    ORDERS_FINISH = f"{BASE_URL}/orders/finish/{{order_id}}"
    ORDERS_CANCEL = f"{BASE_URL}/orders/cancel"
