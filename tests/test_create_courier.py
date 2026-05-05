import allure
from api.courier_api import CourierAPI
from helpers.data_helper import generate_random_string, get_courier_id


class TestCreateCourier:
    @allure.title("Создание курьера с валидными данными")
    def test_create_courier_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        with allure.step("Отправка запроса на создание курьера"):
            response = CourierAPI.create_courier(payload)
        
        with allure.step("Проверка кода ответа и тела"):
            assert response.status_code == 201
            assert response.json()["ok"] == True
        
        with allure.step("Очистка: удаление курьера"):
            courier_id = get_courier_id(login, password)
            if courier_id:
                CourierAPI.delete_courier(courier_id)

    @allure.title("Создание двух одинаковых курьеров")
    def test_create_duplicate_courier(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        with allure.step("Создание первого курьера"):
            CourierAPI.create_courier(payload)
        
        with allure.step("Попытка создания второго курьера с теми же данными"):
            response = CourierAPI.create_courier(payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 409
            # По документации: "Этот логин уже используется"
            assert response.json()["message"] == "Этот логин уже используется"
        
        with allure.step("Очистка: удаление курьера"):
            courier_id = get_courier_id(login, password)
            if courier_id:
                CourierAPI.delete_courier(courier_id)

    @allure.title("Создание курьера без имени (firstName)")
    def test_create_courier_without_firstname(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password
        }
        
        with allure.step("Отправка запроса на создание курьера без firstName"):
            response = CourierAPI.create_courier(payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 201
            assert response.json()["ok"] == True
        
        with allure.step("Очистка: удаление курьера"):
            courier_id = get_courier_id(login, password)
            if courier_id:
                CourierAPI.delete_courier(courier_id)

    @allure.title("Создание курьера без логина")
    def test_create_courier_without_login(self):
        payload = {
            "password": "1234",
            "firstName": "Test"
        }
        
        with allure.step("Отправка запроса без логина"):
            response = CourierAPI.create_courier(payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Создание курьера без пароля")
    def test_create_courier_without_password(self):
        payload = {
            "login": "test_login",
            "firstName": "Test"
        }
        
        with allure.step("Отправка запроса без пароля"):
            response = CourierAPI.create_courier(payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"