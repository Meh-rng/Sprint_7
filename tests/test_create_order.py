import pytest
from api.order_api import OrderAPI
from data.order_data import base_order_data, color_variants


class TestCreateOrder:
    @pytest.mark.parametrize("color", color_variants)
    def test_create_order_with_color(self, color):
        """Создание заказа с разными вариантами цветов"""
        payload = base_order_data.copy()
        payload["color"] = color
        response = OrderAPI.create_order(payload)
        assert response.status_code == 201
        assert "track" in response.json()

    def test_create_order_without_color(self):
        """Создание заказа без указания цвета"""
        payload = base_order_data.copy()
        response = OrderAPI.create_order(payload)
        assert response.status_code == 201
        assert "track" in response.json()

    def test_create_order_with_black_color(self):
        """Создание заказа с чёрным цветом"""
        payload = base_order_data.copy()
        payload["color"] = ["BLACK"]
        response = OrderAPI.create_order(payload)
        assert response.status_code == 201
        assert "track" in response.json()

    def test_create_order_with_grey_color(self):
        """Создание заказа с серым цветом"""
        payload = base_order_data.copy()
        payload["color"] = ["GREY"]
        response = OrderAPI.create_order(payload)
        assert response.status_code == 201
        assert "track" in response.json()

    def test_create_order_with_both_colors(self):
        """Создание заказа с двумя цветами"""
        payload = base_order_data.copy()
        payload["color"] = ["BLACK", "GREY"]
        response = OrderAPI.create_order(payload)
        assert response.status_code == 201
        assert "track" in response.json()
        