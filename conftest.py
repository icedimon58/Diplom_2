import requests
import pytest
from data import HOST, USER, LOGIN
from helpers import generate_random_string


@pytest.fixture
def generate_new_user_and_return_login_password():
    name = generate_random_string(10)
    password = generate_random_string(10)
    email = generate_random_string(10) + '@yandex.ru'

    payload = {
        "name": name,
        "password": password,
        "email": email
    }

    yield payload
    response = requests.post(f'{HOST}{LOGIN}', data=payload)
    headers = {'Authorization': f'{response.json()['accessToken']}'}
    requests.delete(f'{HOST}{USER}', data=payload, headers=headers)
