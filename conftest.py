import pytest
from api.courier_api import CourierAPI
from helpers.data_helper import get_courier_id, generate_random_string


@pytest.fixture
def random_courier_data():
    """Генерирует случайные данные для курьера (без регистрации)"""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }


@pytest.fixture
def created_courier():
    """Создаёт курьера и удаляет после теста (даже при падении)"""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    CourierAPI.create_courier(payload)
    
    yield {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    # Очистка выполняется всегда
    courier_id = get_courier_id(login, password)
    if courier_id:
        CourierAPI.delete_courier(courier_id)

@pytest.fixture

def courier_without_firstname():
    """Создаёт курьера без имени и удаляет после теста"""
    login = generate_random_string(10)
    password = generate_random_string(10)
    
    payload = {
        "login": login,
        "password": password
    }
    
    CourierAPI.create_courier(payload)
    
    yield {
        "login": login,
        "password": password
    }
    
    courier_id = get_courier_id(login, password)
    if courier_id:
        CourierAPI.delete_courier(courier_id)
        