import allure
from api.courier_api import CourierAPI
from helpers.data_helper import (
    generate_random_courier_data,
    generate_courier_data_without_firstname,
    generate_courier_data_without_login,
    generate_courier_data_without_password,
    get_courier_id
)


class TestCreateCourier:
    @allure.title("Создание курьера с валидными данными")
    def test_create_courier_success(self, delete_courier_after_test):
        payload = generate_random_courier_data()
        
        with allure.step("Отправка запроса на создание курьера"):
            response = CourierAPI.create_courier(payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 201
            assert response.json()["ok"] == True
        
        with allure.step("Регистрация на удаление"):
            courier_id = get_courier_id(payload["login"], payload["password"])
            delete_courier_after_test(courier_id)

    @allure.title("Создание двух одинаковых курьеров")
    def test_create_duplicate_courier(self, delete_courier_after_test):
        payload = generate_random_courier_data()
        
        with allure.step("Создание первого курьера"):
            response1 = CourierAPI.create_courier(payload)
            assert response1.status_code == 201
        
        with allure.step("Попытка создания второго курьера с теми же данными"):
            response2 = CourierAPI.create_courier(payload)
        
        with allure.step("Проверка ответа"):
            assert response2.status_code == 409
            assert response2.json()["message"] == "Этот логин уже используется"
        
        with allure.step("Регистрация на удаление"):
            courier_id = get_courier_id(payload["login"], payload["password"])
            delete_courier_after_test(courier_id)

    @allure.title("Создание курьера без имени (firstName)")
    def test_create_courier_without_firstname(self, delete_courier_after_test):
        payload = generate_courier_data_without_firstname()
        
        with allure.step("Отправка запроса на создание курьера без firstName"):
            response = CourierAPI.create_courier(payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 201
            assert response.json()["ok"] == True
        
        with allure.step("Регистрация на удаление"):
            courier_id = get_courier_id(payload["login"], payload["password"])
            delete_courier_after_test(courier_id)

    @allure.title("Создание курьера без логина")
    def test_create_courier_without_login(self):
        payload = generate_courier_data_without_login()
        
        with allure.step("Отправка запроса без логина"):
            response = CourierAPI.create_courier(payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Создание курьера без пароля")
    def test_create_courier_without_password(self):
        payload = generate_courier_data_without_password()
        
        with allure.step("Отправка запроса без пароля"):
            response = CourierAPI.create_courier(payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"