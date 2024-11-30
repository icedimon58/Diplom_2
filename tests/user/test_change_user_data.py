import allure
import requests
import pytest
from data import HOST, REGISTER, LOGIN, USER, AUTORIZED_ERROR, TEST_DATA


class TestChangeUserData:

    @pytest.mark.parametrize('name,email', TEST_DATA)
    @allure.description('Код операции:200')
    @allure.title('Проверка изменения данных о пользователе с авторизацией')
    def test_change_user_data_with_login_positive(self, generate_new_user_and_return_login_password, name, email):
        payload = generate_new_user_and_return_login_password
        requests.post(f'{HOST}{REGISTER}', data=payload)
        response = requests.post(f'{HOST}{LOGIN}', data=payload)
        headers = {'Authorization': f'{response.json()['accessToken']}'}
        payload['name'] = name
        payload['email'] = email
        response = requests.patch(f'{HOST}{USER}', data=payload, headers=headers)
        assert (response.status_code == 200
                and response.json()['user']['name'] == name
                and response.json()['user']['email'] == email)

    @allure.description('Код операции:401')
    @allure.title('Проверка изменения данных о пользователе без авторизации')
    def test_change_user_data_without_login_negetive(self, generate_new_user_and_return_login_password):
        payload = generate_new_user_and_return_login_password
        requests.post(f'{HOST}{REGISTER}', data=payload)
        payload['name'] = 'new_name'
        email = payload['email']
        payload['email'] = 'new_mail'
        response = requests.patch(f'{HOST}{USER}', data=payload)
        payload['email'] = email
        assert (response.status_code == 401
                and response.json()['message'] == AUTORIZED_ERROR)
