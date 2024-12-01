import allure
import requests
import pytest
from data import HOST, REGISTER, LOGIN, INGRIDIENTS_HASH, ORDERS, INGRIDIENT_ERROR
from helpers import generate_random_string


class TestCreateOrders:
    @pytest.mark.parametrize('ingredient', INGRIDIENTS_HASH)
    @allure.description('Код операции:200')
    @allure.title('Проверка создания заказа с авторизацией')
    def test_create_order_with_autorisation_positive(self, generate_new_user_and_return_login_password, ingredient):
        payload = generate_new_user_and_return_login_password
        requests.post(f'{HOST}{REGISTER}', data=payload)
        response = requests.post(f'{HOST}{LOGIN}', data=payload)
        payload_ingrid = {'ingredients': ingredient}
        headers = {'Authorization': f'{response.json()['accessToken']}'}
        response = requests.post(f'{HOST}{ORDERS}', data=payload_ingrid, headers=headers)
        assert (response.status_code == 200 and response.json()['order']['owner']['name'] == payload['name'])

    @allure.description('Код операции:200')
    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_without_autorisation_positive(self):
        payload_ingrid = {'ingredients': INGRIDIENTS_HASH[0]}
        response = requests.post(f'{HOST}{ORDERS}', data=payload_ingrid)
        assert (response.status_code == 200)

    @allure.description('Код операции:400')
    @allure.title('Проверка создания заказа с авторизацией, но без ингридиентов')
    def test_create_order_without_ingridients_negative(self, generate_new_user_and_return_login_password):
        payload = generate_new_user_and_return_login_password
        requests.post(f'{HOST}{REGISTER}', data=payload)
        response = requests.post(f'{HOST}{LOGIN}', data=payload)
        payload_ingrid = {'ingredients': ''}
        headers = {'Authorization': f'{response.json()['accessToken']}'}
        response = requests.post(f'{HOST}{ORDERS}', data=payload_ingrid, headers=headers)
        assert (response.status_code == 400 and response.json()['message'] == INGRIDIENT_ERROR)

    @allure.description('Код операции:500')
    @allure.title('Проверка создания заказа с авторизацией и неверным хэшем')
    def test_create_order_without_ingridients_negative(self, generate_new_user_and_return_login_password):
        payload = generate_new_user_and_return_login_password
        requests.post(f'{HOST}{REGISTER}', data=payload)
        response = requests.post(f'{HOST}{LOGIN}', data=payload)
        payload_ingrid = {'ingredients': generate_random_string(24)}
        headers = {'Authorization': f'{response.json()['accessToken']}'}
        response = requests.post(f'{HOST}{ORDERS}', data=payload_ingrid, headers=headers)
        assert (response.status_code == 500)
