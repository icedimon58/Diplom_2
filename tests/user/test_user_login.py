import allure
import requests
from data import HOST, REGISTER, LOGIN, NO_PWD_OR_EMAIL_ERROR


class TestLoginUser:

    @allure.description('Код операции:200')
    @allure.title('Проверка авторизации пользователя')
    def test_login_user_positive(self, register_new_user_and_return_login_password):
        payload = register_new_user_and_return_login_password
        requests.post(f'{HOST}{REGISTER}', data=payload)
        response = requests.post(f'{HOST}{LOGIN}', data=payload)
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.description('Код операции:401')
    @allure.title('Проверка авторизации пользователя с неверным паролем')
    def test_login_user_wrong_password_negative(self, register_new_user_and_return_login_password):
        payload = register_new_user_and_return_login_password
        requests.post(f'{HOST}{REGISTER}', data=payload)
        # для того чтобы прошло удаление пользователя сохраняем его старый пароль, указываем новый, а затем возвращаем
        # старое значение
        last_pwd = payload['password']
        payload['password'] = '123'
        response = requests.post(f'{HOST}{LOGIN}', data=payload)
        payload['password'] = last_pwd
        assert response.status_code == 401 and response.json()['message'] == NO_PWD_OR_EMAIL_ERROR

    @allure.description('Код операции:401')
    @allure.title('Проверка авторизации пользователя с неверной почтой')
    def test_login_user_wrong_email_negative(self, register_new_user_and_return_login_password):
        payload = register_new_user_and_return_login_password
        requests.post(f'{HOST}{REGISTER}', data=payload)
        # для того чтобы прошло удаление пользователя сохраняем его старую почту, указываем новую, а затем возвращаем
        # старое значение
        last_email = payload['email']
        payload['email'] = '123'
        response = requests.post(f'{HOST}{LOGIN}', data=payload)
        payload['email'] = last_email
        assert response.status_code == 401 and response.json()['message'] == NO_PWD_OR_EMAIL_ERROR
