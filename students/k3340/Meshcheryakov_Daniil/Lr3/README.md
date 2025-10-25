# Лабораторная работа №3: Django REST Framework

**Студент**: Мещеряков Даниил  
**Группа**: K3340  
**Вариант**: Читальный зал

## 🚀 Быстрый запуск

### 1. Установка зависимостей

```bash
cd task_1
pip install -r requirements.txt
```

### 2. Настройка базы данных PostgreSQL

Создайте файл `.env` в папке `task_1/`:

```env
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=ваш_пароль
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=ваш-секретный-ключ
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

## 🧪 Тестирование API

### Swagger UI (Рекомендуется!)

Откройте в браузере:

```
http://localhost:8000/api/schema/swagger-ui/
```

**Как использовать Swagger:**

1. Откройте Swagger UI
2. Найдите endpoint `/api/auth/token/login/`
3. Нажмите "Try it out"
4. Введите username и password суперпользователя
5. Нажмите "Execute"
6. Скопируйте полученный токен
7. Нажмите кнопку "Authorize" вверху страницы
8. Введите: `Token <ваш_токен>` (например: `Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`)
9. Нажмите "Authorize"
10. Теперь можете тестировать все endpoints!

### Другие способы тестирования

**ReDoc:**
```
http://localhost:8000/api/schema/redoc/
```

**Browsable API (DRF):**
```
http://localhost:8000/api/
```

**Admin панель:**
```
http://localhost:8000/admin/
```

**Postman:**
- Импортируйте OpenAPI schema: `http://localhost:8000/api/schema/`

## 📚 Основные endpoints

### Аутентификация

```
POST   /api/auth/users/              # Регистрация
POST   /api/auth/token/login/        # Получить токен
POST   /api/auth/token/logout/       # Выход
GET    /api/auth/users/me/           # Текущий пользователь
```

### API

```
GET    /api/books/                   # Список книг
POST   /api/books/                   # Создать книгу (персонал)
GET    /api/books/available/         # Доступные книги
GET    /api/borrowings/              # Список выдач
POST   /api/borrowings/              # Взять книгу
POST   /api/borrowings/{id}/return_book/  # Вернуть книгу
GET    /api/reviews/                 # Список отзывов
POST   /api/reviews/                 # Создать отзыв
```

И другие для читателей, авторов, издательств, жанров.

## 💡 Примеры запросов

### cURL

```bash
# Регистрация
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com", "password": "pass123", "re_password": "pass123"}'

# Получение токена
curl -X POST http://localhost:8000/api/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "pass123"}'

# Получить книги (с токеном)
curl http://localhost:8000/api/books/ \
  -H "Authorization: Token ваш-токен"
```

### Python

```python
import requests

# Получение токена
response = requests.post('http://localhost:8000/api/auth/token/login/', json={
    "username": "test",
    "password": "pass123"
})
token = response.json()['auth_token']

# Использование API
headers = {"Authorization": f"Token {token}"}
response = requests.get('http://localhost:8000/api/books/', headers=headers)
books = response.json()
```

## 🧪 Запуск тестов

```bash
python manage.py test
```

## 📖 Структура проекта

```
Lr3/
├── task_1/     # Полный Django проект (модели + API + авторизация + Swagger)
│   ├── library_api/     # Настройки проекта
│   ├── library/         # Приложение с моделями и API
│   ├── manage.py
│   └── requirements.txt
├── task_2/     # Примеры кода: Сериализаторы + ViewSets
└── task_3/     # Примеры кода: Авторизация + permissions
```

**Примечание:** `task_2` и `task_3` содержат примеры кода для отчета. Весь рабочий код находится в `task_1`.

## ✅ Реализовано

- ✅ **7 моделей данных** (Reader, Author, Publisher, Genre, Book, Borrowing, Review)
- ✅ **Полный CRUD API** для всех моделей
- ✅ **Swagger/OpenAPI** документация (drf-spectacular)
- ✅ **Аутентификация** через Djoser (Token auth)
- ✅ **Фильтрация, поиск, сортировка, пагинация**
- ✅ **Кастомные действия** (available books, return book, active/overdue borrowings)
- ✅ **Автоматический расчет** доступности книг и штрафов
- ✅ **Разграничение прав доступа**
- ✅ **Админ-панель Django**
- ✅ **Тесты**

## 🔧 Возможные проблемы

### PostgreSQL не подключается

Проверьте:
- PostgreSQL запущен
- Настройки в `.env` корректны
- База данных создана

### Ошибка с Pillow

**Windows:**
```bash
pip install Pillow --no-cache-dir
```

**Linux:**
```bash
sudo apt-get install libjpeg-dev zlib1g-dev
pip install Pillow
```

### Ошибка миграций

```bash
python manage.py makemigrations library
python manage.py migrate
```

## 📚 Документация

Полная документация доступна в:
- `report/docs/lab3/` - документация для отчета
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/

## 🎯 Технологии

- Django 4.2
- Django REST Framework 3.14
- drf-spectacular 0.27 (Swagger)
- Djoser 2.2 (аутентификация)
- PostgreSQL
- django-filter
- Pillow

## 👤 Автор

**Мещеряков Даниил**  
Группа K3340  
Университет ИТМО  
2024-2025
