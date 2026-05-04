import pytest
from api.courier_api import CourierAPI
from helpers.data_helper import register_new_courier_and_return_login_password, get_courier_id


@pytest.fixture
def courier_for_login():
    """Создаёт курьера и удаляет после теста"""
    login_pass = register_new_courier_and_return_login_password()
    yield login_pass
    if login_pass:
        courier_id = get_courier_id(login_pass[0], login_pass[1])
        if courier_id:
            CourierAPI.delete_courier(courier_id)


class TestLoginCourier:
    def test_login_success(self, courier_for_login):
        """Курьер может авторизоваться"""
        assert len(courier_for_login) == 3
        payload = {
            "login": courier_for_login[0],
            "password": courier_for_login[1]
        }
        response = CourierAPI.login_courier(payload)
        assert response.status_code == 200
        assert "id" in response.json()

    def test_login_without_login(self):
        """Если нет логина, запрос возвращает ошибку"""
        payload = {"password": "1234"}
        response = CourierAPI.login_courier(payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    def test_login_without_password(self):
        """Если нет пароля, запрос возвращает ошибку"""
        payload = {"login": "test_login"}
        response = CourierAPI.login_courier(payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    def test_login_nonexistent_user(self):
        """Авторизация с несуществующим пользователем"""
        payload = {"login": "nonexistent", "password": "wrong"}
        response = CourierAPI.login_courier(payload)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    def test_login_wrong_password(self, courier_for_login):
        """Авторизация с неправильным паролем"""
        assert len(courier_for_login) == 3
        payload = {
            "login": courier_for_login[0],
            "password": "wrong_password"
        }
        response = CourierAPI.login_courier(payload)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"