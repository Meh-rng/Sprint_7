import allure
from api.courier_api import CourierAPI
from helpers.data_helper import (
    generate_random_courier_data,
    get_courier_id
)


class TestLoginCourier:
    @allure.title("Успешная авторизация курьера")
    def test_login_success(self, delete_courier_after_test):
        with allure.step("Генерация данных курьера"):
            payload = generate_random_courier_data()
        
        with allure.step("Создание курьера"):
            CourierAPI.create_courier(payload)
        
        with allure.step("Регистрация на удаление"):
            courier_id = get_courier_id(payload["login"], payload["password"])
            delete_courier_after_test(courier_id)
        
        with allure.step("Авторизация курьера"):
            login_payload = {"login": payload["login"], "password": payload["password"]}
            response = CourierAPI.login_courier(login_payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Авторизация без логина")
    def test_login_without_login(self):
        with allure.step("Отправка запроса без логина"):
            payload = {"password": "1234"}
            response = CourierAPI.login_courier(payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Авторизация без пароля")
    def test_login_without_password(self):
        with allure.step("Отправка запроса без пароля"):
            payload = {"login": "test_login"}
            response = CourierAPI.login_courier(payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Авторизация с несуществующим пользователем")
    def test_login_nonexistent_user(self):
        with allure.step("Отправка запроса с несуществующим логином"):
            payload = {"login": "nonexistent", "password": "wrong"}
            response = CourierAPI.login_courier(payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Авторизация с неправильным паролем")
    def test_login_wrong_password(self, delete_courier_after_test):
        with allure.step("Генерация данных курьера"):
            payload = generate_random_courier_data()
        
        with allure.step("Создание курьера"):
            CourierAPI.create_courier(payload)
        
        with allure.step("Регистрация на удаление"):
            courier_id = get_courier_id(payload["login"], payload["password"])
            delete_courier_after_test(courier_id)
        
        with allure.step("Авторизация с неправильным паролем"):
            login_payload = {"login": payload["login"], "password": "wrong_password"}
            response = CourierAPI.login_courier(login_payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"
            