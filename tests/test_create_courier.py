import pytest
from api.courier_api import CourierAPI
from helpers.data_helper import register_new_courier_and_return_login_password, get_courier_id


@pytest.fixture
def courier_data():
    """Создаёт курьера и удаляет после теста"""
    login_pass = register_new_courier_and_return_login_password()
    yield login_pass
    # Удаляем курьера после теста
    if login_pass:
        courier_id = get_courier_id(login_pass[0], login_pass[1])
        if courier_id:
            CourierAPI.delete_courier(courier_id)


class TestCreateCourier:
    def test_create_courier_success(self, courier_data):
        """Курьера можно создать"""
        assert len(courier_data) == 3, "Курьер не создался"

    def test_create_duplicate_courier(self, courier_data):
        """Нельзя создать двух одинаковых курьеров"""
        assert len(courier_data) == 3, "Первый курьер не создался"

        payload = {
            "login": courier_data[0],
            "password": courier_data[1],
            "firstName": courier_data[2]
        }
        response = CourierAPI.create_courier(payload)
        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется"

    def test_create_courier_without_login(self):
        """Если нет логина, запрос возвращает ошибку"""
        payload = {
            "password": "1234",
            "firstName": "Test"
        }
        response = CourierAPI.create_courier(payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    def test_create_courier_without_password(self):
        """Если нет пароля, запрос возвращает ошибку"""
        payload = {
            "login": "test_login",
            "firstName": "Test"
        }
        response = CourierAPI.create_courier(payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    def test_create_courier_without_firstname(self):
        """Можно создать курьера без имени (firstName не обязателен)"""
        import random
        import string
        unique_login = ''.join(random.choices(string.ascii_lowercase, k=10))
        unique_password = ''.join(random.choices(string.ascii_lowercase, k=10))
        payload = {
            "login": unique_login,
            "password": unique_password
        }
        response = CourierAPI.create_courier(payload)
        assert response.status_code == 201
        assert response.json()["ok"] == True
        
        # Удаляем созданного курьера
        courier_id = get_courier_id(unique_login, unique_password)
        if courier_id:
            CourierAPI.delete_courier(courier_id)