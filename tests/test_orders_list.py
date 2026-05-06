from api.order_api import OrderAPI


class TestOrdersList:
    def test_get_orders_list(self):
        """В тело ответа возвращается список заказов"""
        response = OrderAPI.get_orders()
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
        