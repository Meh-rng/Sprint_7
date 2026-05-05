import allure
from api.courier_api import CourierAPI
from helpers.data_helper import generate_random_string, get_courier_id


class TestLoginCourier:
    @allure.title("Успешная авторизация курьера")
    def test_login_success(self):
        with allure.step("Генерация данных курьера"):
            login = generate_random_string(10)
            password = generate_random_string(10)
            first_name = generate_random_string(10)
            
            create_payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
        
        with allure.step("Создание курьера"):
            CourierAPI.create_courier(create_payload)
        
        with allure.step("Авторизация курьера"):
            login_payload = {"login": login, "password": password}
            response = CourierAPI.login_courier(login_payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert "id" in response.json()
        
        with allure.step("Очистка: удаление курьера"):
            courier_id = get_courier_id(login, password)
            if courier_id:
                CourierAPI.delete_courier(courier_id)

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
    def test_login_wrong_password(self):
        with allure.step("Генерация данных курьера"):
            login = generate_random_string(10)
            password = generate_random_string(10)
            first_name = generate_random_string(10)
            
            create_payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
        
        with allure.step("Создание курьера"):
            CourierAPI.create_courier(create_payload)
        
        with allure.step("Авторизация с неправильным паролем"):
            login_payload = {"login": login, "password": "wrong_password"}
            response = CourierAPI.login_courier(login_payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"
        
        with allure.step("Очистка: удаление курьера"):
            courier_id = get_courier_id(login, password)
            if courier_id:
                CourierAPI.delete_courier(courier_id)
                