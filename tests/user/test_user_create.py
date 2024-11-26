import allure
import requests
from data import HOST, REGISTER, USER_EXIST, NO_FIELDS


class TestCreateUser:

    @allure.description('Код операции:200')
    @allure.title('Проверка создания пользователя')
    def test_create_unique_user_positive(self, register_new_user_and_return_login_password):
        payload = register_new_user_and_return_login_password
        response = requests.post(f'{HOST}{REGISTER}', data=payload)
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.description('Код операции:403')
    @allure.title('Проверка создания уже существующего пользователя')
    def test_create_exisiting_user_negative(self, register_new_user_and_return_login_password):
        payload = register_new_user_and_return_login_password
        requests.post(f'{HOST}{REGISTER}', data=payload)
        response = requests.post(f'{HOST}{REGISTER}', data=payload)
        assert response.status_code == 403 and response.json()['message'] == USER_EXIST

    @allure.description('Код операции:403')
    @allure.title('Проверка создания пользователя без заполнения полей')
    def test_create_user_without_fields_negative(self):
        payload = {
            "name": '',
            "password": '',
            "email": ''
        }
        response = requests.post(f'{HOST}{REGISTER}', data=payload)
        assert response.status_code == 403 and response.json()['message'] == NO_FIELDS
