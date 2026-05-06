import pytest
import allure
from api.order_api import OrderAPI
from data.order_data import base_order_data, color_variants


class TestCreateOrder:
    @allure.title("Создание заказа с разными вариантами цветов")
    @pytest.mark.parametrize("color", color_variants)
    def test_create_order_with_color(self, color):
        with allure.step("Подготовка данных заказа"):
            payload = base_order_data.copy()
            payload["color"] = color
        
        with allure.step(f"Отправка запроса на создание заказа с цветом {color}"):
            response = OrderAPI.create_order(payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 201
            assert "track" in response.json()