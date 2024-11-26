# Дипломная работа 
# Задание №2
API-тесты страницы 'https://stellarburgers.nomoreparties.site'
## Установка зависимостей:

`pip install -r requirments.txt`

## Структура проекта:
Все тесты лежат в папке tests

    директория order содержит тесты API по работе с заказом

    директория user содержит тесты API по работе с пользователем

## Запуск тестов с формированием отчета в Allure:
`pytest  -v -s  --alluredir allure_results`

## Просмотр отчета в Allure:

`pytest  -v -s  --alluredir allure_results`
