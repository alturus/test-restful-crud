## Тестовое задание
 
Используя фреймворк Flask:
 
1. Реализовать сущности авторы и книги
2. Реализовать по RESTful протоколу CRUD операции для авторов и книг
3. Реализовать публичную часть сайта с отображение авторов и их книг (простой вывод списка на странице)

## Использование
### Описание RESTful API
Books

HTTP-метод | Ресурс | Описание | Auth.
--- | --- | --- | ---
GET | /api/v1/books/ | Возвращает перечень книг | -
POST | /api/v1/books/ | Создать книгу | +
GET | /api/v1/books/{book_id}/ | Инф-ция о книге | -
PATCH | /api/v1/books/{book_id}/ | Изменить книгу | +
DELETE | /api/v1/books/{book_id}/ | Удалить книгу | +

Authors

HTTP-метод | Ресурс | Описание | Auth.
--- | --- | --- | ---
GET | /api/v1/authors/ | Возвращает перечень авторов | -
POST | /api/v1/authors/ | Создать автора | +
GET | /api/v1/authors/{author_id}/ | Инф-ция об авторе | -
PATCH | /api/v1/authors/{author_id}/ | Изменить автора | +
DELETE | /api/v1/authors/{author_id}/ | Удалить автора | +

_Auth. - требуется наличие авторизации (токен доступа)_

#### Создание записи о книге
Параметры запроса 

Имя | Тип | Описание
--- | --- | ---
title | string | Наименование книги
isbn | int | 10- или 13-значный международный номер
year | int | Год издания
authors | array | Автор(ы)

Пример:
```
{
    "title": "The Hitchhiker's Guide to Python: Best Practices for Development",
    "isbn": 9781491933176,
    "year": 2016,
    "authors": [
        {"firstname": "Kenneth", "lastname": "Reitz"},
        {"firstname": "Tanya", "lastname": "Schlusser"}
    ]
}
```

#### Создание записи автора
Параметры запроса

Имя | Тип | Описание
--- | --- | ---
firstname | string | Имя автора
lastname | string | Фамилия автора

Пример:
```
{
    "firstname": "Kenneth",
    "lastname": "Reitz"
}
```

### Авторизация
Для операций на изменение и добавление объектов требуется авторизация пользователя с использованием токена JSON Web Token (JWT).

Пример токена:
```
Authorization: Bearer 1pbiI6ZmFsc2V9fQ.EAEglUwJkQhvwuz98OrbdFmqNm2tvv_O-FMrFTTFQ6c
```
#### Регистрация нового пользователя
Необходимо отправить POST запрос к ресурсу `/auth/registration`

Параметры:

Имя | Тип | Описание
--- | --- | ---
username | string | Имя пользователя
password | string | Пароль

Пример ответа:
```
{
    "message": "User test was created",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NDIwOTAzNTgsIm5iZiI6MTU0MjA5MDM1OCwianRpIjoiNDg2YWZlYjktYWY0Zi00OTg5LWIxMTYtMWU5MjUzNDYzZDE0IiwiZXhwIjoxNTQyMDkxMjU4LCJpZGVudGl0eSI6InRlc3QiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJ1c2VybmFtZSI6InRlc3QiLCJhZG1pbiI6ZmFsc2V9fQ.EAEglUwJkQhvwuz98OrbdFmqNm2tvv_O-FMrFTTFQ6c",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NDIwOTAzNTgsIm5iZiI6MTU0MjA5MDM1OCwianRpIjoiYmFiM2VmMWItZjY0Ni00YTkyLTlkYWUtYmRiOGQ4Y2U1ZGEzIiwiZXhwIjoxNTQ0NjgyMzU4LCJpZGVudGl0eSI6InRlc3QiLCJ0eXBlIjoicmVmcmVzaCJ9.RuKtimWa-AjG8E9Jt7eKwkB7t7WDFP5_yTvqYRq-T6c"
}
```

#### Получение токенов для зарегистрированного пользователя
Необходимо отправить POST запрос к ресурсу `/auth/login`

Параметры:

Имя | Тип | Описание
--- | --- | ---
username | string | Имя пользователя
password | string | Пароль

Пример ответа:
```
{
    "message": "Logged in as test",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NDIxMDY5NDQsIm5iZiI6MTU0MjEwNjk0NCwianRpIjoiMDEyOTM4ZDQtZTA0Ny00ZTRmLThmZTItZTUxNTU2MzFhNDg0IiwiZXhwIjoxNTQyMTA3ODQ0LCJpZGVudGl0eSI6InRlc3QiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJ1c2VybmFtZSI6InRlc3QiLCJhZG1pbiI6ZmFsc2V9fQ.gHuhEhjeMLDJmbtMGYMgO0faZy9rnTyVxG4Lbcgm194",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NDIxMDY5NDQsIm5iZiI6MTU0MjEwNjk0NCwianRpIjoiNDU3ZmMxNjctNDI2Ni00YzIyLTgxOWYtYzM1MTg2NmMyODY0IiwiZXhwIjoxNTQ0Njk4OTQ0LCJpZGVudGl0eSI6InRlc3QiLCJ0eXBlIjoicmVmcmVzaCJ9.B_NGekk6k0xiQ0wpsKhug97omlSOJ1lbNgEy05L23y4"
}
```

#### Обновление токена доступа с использованием refresh-токена
Необходимо отправить POST запрос к ресурсу `/auth/token/refresh`

В заголовке запроса передать refresh-токен.

Пример ответа:
```
{
    "username": "test",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NDIxMDczNDMsIm5iZiI6MTU0MjEwNzM0MywianRpIjoiZjRiZWMzMzgtMzFmYi00NjliLWJhYmItZGFhODFhMTFlZWFlIiwiZXhwIjoxNTQyMTA4MjQzLCJpZGVudGl0eSI6InRlc3QiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJ1c2VybmFtZSI6InRlc3QiLCJhZG1pbiI6ZmFsc2V9fQ.ybS88uQKKnucTShrXn_n7Hkjwhnmt1cI7mSDCrXiNpY"
}
```

#### Блокировка access и refresh токенов пользователя
Для блокировки access-токена необходимо отправить POST запрос к ресурсу `/auth/logout/access` используя действующий access-токен.

Пример ответа:
```
{
    "message": "Access token has been revoked"
}
```

Для блокировки refresh-токена необходимо отправить POST запрос к ресурсу `/auth/logout/refresh` используя действующий refresh-токен.

Пример ответа:
```
{
    "message": "Refresh token has been revoked"
}
```

#### Удаление пользователя
Получить список пользователей и удалить пользователя может только пользователь с правами администратора.

HTTP-метод | Ресурс | Описание
--- | --- | --- 
GET | /auth/users/ | Возвращает перечень пользователей
GET | /auth/users/{user_id}/ | Информация о пользователе
DELETE | /auth/users/{user_id}/ | Удаление пользователя

## Установка
#### Подготовка окружения
1. Клонировать проект
2. Создать виртуальное окружение
3. Установить зависимости
```
$ git clone https://github.com/alturus/test-restful-crud.git
$ python36 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
#### Установить переменные окружения
1. Создать файл .env с необходимыми параметрами
```
FLASK_CONFIG="production"
SECRET_KEY="my_precious_secret_key"
JWT_SECRET_KEY="jwt-secret-string"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="password"
DATABASE_URI="mysql+mysqlconnector://usr:pass@localhost/books"
```

#### Создание базы данных
Предварительно создать базу данных
```
mysql> CREATE DATABASE books CHARACTER SET = 'utf8' COLLATE = 'utf8_general_ci';
mysql> CREATE USER 'books'@'localhost' IDENTIFIED by 'password';
mysql> GRANT ALL PRIVILEGES ON books.* to 'books'@'localhost';
```
Создание необходимых таблиц
```
$ flask deploy
```
#### Запуск
```
$ flask run
```

#### Тестирование
Без отчёта о покрытии кода тестами
```
$ flask test
```
С отчётом о покрытии кода
```
$ flask --coverage
```
