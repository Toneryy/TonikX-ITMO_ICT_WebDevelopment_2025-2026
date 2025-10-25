# Лабораторная работа №3: Django REST Framework

## Описание

Реализация RESTful API для системы "Читальный зал" с использованием Django REST Framework, Djoser и PostgreSQL.

## Задачи

Лабораторная работа разделена на 3 подзадачи:

1. **Подзадача 1** - Настройка проекта DRF и расширенные модели БД с PostgreSQL
2. **Подзадача 2** - Реализация API endpoints (сериализаторы, ViewSets, CRUD)
3. **Подзадача 3** - Интеграция Djoser для авторизации по токенам и права доступа + Swagger документация

## Технологический стек

- **Python 3.10+**
- **Django 4.2** - веб-фреймворк
- **Django REST Framework 3.14** - для построения API
- **Djoser 2.2** - аутентификация и управление пользователями
- **PostgreSQL** - база данных
- **drf-spectacular** - Swagger/OpenAPI документация

## Быстрый старт

### 1. Установка зависимостей

```bash
cd students/k3340/Meshcheryakov_Daniil/Lr3/task_1
pip install -r requirements.txt
```

### 2. Настройка базы данных

Создайте файл `.env`:

```env
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key
DEBUG=True
```

Создайте базу данных:

```sql
CREATE DATABASE library_db;
```

### 3. Миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 5. Запуск сервера

```bash
python manage.py runserver
```

## Тестирование API

### Через Swagger UI

Откройте в браузере:

```
http://localhost:8000/api/schema/swagger-ui/
```

### Через Browsable API

```
http://localhost:8000/api/
```

### Через cURL

```bash
# Регистрация
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com", "password": "pass123", "re_password": "pass123"}'

# Получение токена
curl -X POST http://localhost:8000/api/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "pass123"}'
```

## Основные endpoints

- **Swagger UI**: `/api/schema/swagger-ui/`
- **ReDoc**: `/api/schema/redoc/`
- **OpenAPI Schema**: `/api/schema/`
- **Auth**: `/api/auth/`
- **Books**: `/api/books/`
- **Borrowings**: `/api/borrowings/`
- **Reviews**: `/api/reviews/`

## Функциональность

- ✅ Полный CRUD для всех моделей
- ✅ Аутентификация по токенам
- ✅ Разграничение прав доступа
- ✅ Фильтрация, поиск, сортировка
- ✅ Автоматический Swagger/OpenAPI
- ✅ Тесты API

## Структура проекта

```
Lr3/
├── task_1/     # Полный Django проект (модели + API + авторизация + Swagger)
├── task_2/     # Примеры кода: Сериализаторы + ViewSets
└── task_3/     # Примеры кода: Авторизация + permissions
```

## Навигация

- [Быстрый старт](quickstart.md)
- [Тестирование](testing.md)

