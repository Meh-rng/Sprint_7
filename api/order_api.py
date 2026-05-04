import requests


class OrderAPI:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/orders"

    @staticmethod
    def create_order(payload):
        """Создание заказа (требует JSON)"""
        return requests.post(OrderAPI.BASE_URL, json=payload)

    @staticmethod
    def get_orders(params=None):
        """Получение списка заказов"""
        return requests.get(OrderAPI.BASE_URL, params=params)