import requests
from constants import ORDERS_URL


class OrderAPI:
    @staticmethod
    def create_order(payload):
        """Создание заказа"""
        return requests.post(ORDERS_URL, json=payload)

    @staticmethod
    def get_orders(params=None):
        """Получение списка заказов"""
        return requests.get(ORDERS_URL, params=params)