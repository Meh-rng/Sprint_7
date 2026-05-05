import requests
import random
import string
from constants import COURIER_URL, LOGIN_URL


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def register_new_courier_and_return_login_password():
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
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(LOGIN_URL, data=payload)
    if response.status_code == 200:
        return response.json()["id"]
    return None