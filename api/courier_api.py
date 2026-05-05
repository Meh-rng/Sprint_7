import requests
from constants import COURIER_URL, LOGIN_URL


class CourierAPI:
    @staticmethod
    def create_courier(payload):
        """Создание курьера"""
        return requests.post(COURIER_URL, data=payload)

    @staticmethod
    def login_courier(payload):
        """Логин курьера"""
        return requests.post(LOGIN_URL, data=payload)

    @staticmethod
    def delete_courier(courier_id):
        """Удаление курьера"""
        return requests.delete(f"{COURIER_URL}/{courier_id}")