import pytest
import requests


@pytest.fixture
def base_url():
    return "https://qa-scooter.praktikum-services.ru/api/v1"


@pytest.fixture
def session():
    return requests.Session()
