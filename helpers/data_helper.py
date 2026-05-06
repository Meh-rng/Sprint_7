import requests
import random
import string
from constants import COURIER_URL, LOGIN_URL


def generate_random_string(length):
    """Генерирует случайную строку заданной длины"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_courier_data():
    """Генерирует случайные данные для курьера (с именем)"""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }


def generate_courier_data_without_firstname():
    """Генерирует данные для курьера без имени"""
    login = generate_random_string(10)
    password = generate_random_string(10)
    return {
        "login": login,
        "password": password
    }


def generate_courier_data_without_login():
    """Генерирует данные для курьера без логина"""
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    return {
        "password": password,
        "firstName": first_name
    }


def generate_courier_data_without_password():
    """Генерирует данные для курьера без пароля"""
    login = generate_random_string(10)
    first_name = generate_random_string(10)
    return {
        "login": login,
        "firstName": first_name
    }


def register_new_courier_and_return_login_password():
    """Регистрирует нового курьера и возвращает [login, password, first_name]"""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(COURIER_URL, data=payload)

    if response.status_code == 201:
        return [login, password, first_name]
    return []


def get_courier_id(login, password):
    """Возвращает ID курьера по логину и паролю"""
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(LOGIN_URL, data=payload)
    if response.status_code == 200:
        return response.json()["id"]
    return None