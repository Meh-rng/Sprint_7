import requests


class CourierAPI:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier"

    @staticmethod
    def create_courier(payload):
        """Создание курьера"""
        return requests.post(CourierAPI.BASE_URL, data=payload)

    @staticmethod
    def login_courier(payload):
        """Логин курьера"""
        return requests.post(f"{CourierAPI.BASE_URL}/login", data=payload)
    
    @staticmethod
    def delete_courier(courier_id):
        """Удаление курьера"""
        return requests.delete(f"{CourierAPI.BASE_URL}/{courier_id}")