import pytest
from api.courier_api import CourierAPI


@pytest.fixture
def delete_courier_after_test():
    """Фикстура для удаления курьера после теста"""
    courier_ids = []
    
    def register_for_deletion(courier_id):
        if courier_id:
            courier_ids.append(courier_id)
    
    yield register_for_deletion
    
    for courier_id in courier_ids:
        CourierAPI.delete_courier(courier_id)


@pytest.fixture
def created_courier(delete_courier_after_test):
    """Создаёт курьера и регистрирует на удаление"""
    from helpers.data_helper import generate_random_courier_data
    payload = generate_random_courier_data()
    CourierAPI.create_courier(payload)
    
    from helpers.data_helper import get_courier_id
    courier_id = get_courier_id(payload["login"], payload["password"])
    delete_courier_after_test(courier_id)
    
    return payload