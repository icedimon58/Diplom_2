import allure
import requests
from data import HOST, REGISTER, LOGIN, INGRIDIENTS_HASH, ORDERS, AUTORIZED_ERROR
from helpers import make_order


class TestCreateOrders:
    @allure.description('Код операции:200')
    @allure.title('Проверка получения заказов пользователя с авторизацией')
    def test_get_user_orders_with_autorisation_positive(self, generate_new_user_and_return_login_password):
        payload = generate_new_user_and_return_login_password
        requests.post(f'{HOST}{REGISTER}', data=payload)
        response = requests.post(f'{HOST}{LOGIN}', data=payload)
        headers = {'Authorization': f'{response.json()['accessToken']}'}
        # вызываем функцию создания заказа
        make_order(headers, INGRIDIENTS_HASH[0])
        make_order(headers, INGRIDIENTS_HASH[1])
        response = requests.get(f'{HOST}{ORDERS}', headers=headers)
        # для подсчета количества возвращённых заказов для пользователя подсчитываем
        # количество повторений id в ответе сервера
        expected_orders = str(response.json()).count('id')
        assert (response.status_code == 200 and expected_orders == 2)

    @allure.description('Код операции:401')
    @allure.title('Получение заказа без авторизации')
    def test_get_user_orders_without_autorisation_negative(self):
        make_order({}, INGRIDIENTS_HASH[0])
        response = requests.get(f'{HOST}{ORDERS}')
        assert (response.status_code == 401 and response.json()['message'] == AUTORIZED_ERROR)
