# Быстрый старт - Лабораторная №3

Пошаговая инструкция для запуска и тестирования проекта.

## Предварительные требования

- Python 3.10+
- PostgreSQL 12+
- pip

## Установка

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/TonikX/ITMO_ICT_WebDevelopment_2025-2026.git
cd students/k3340/Meshcheryakov_Daniil/Lr3/task_1
```

### Шаг 2: Создание виртуального окружения (опционально)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Шаг 3: Установка зависимостей

```bash
pip install -r requirements.txt
```

Основные зависимости:
```
Django==4.2.7
djangorestframework==3.14.0
djoser==2.2.2
drf-spectacular==0.27.0
psycopg2-binary==2.9.9
django-filter==23.5
python-dotenv==1.0.0
Pillow==10.1.0
```

### Шаг 4: Настройка PostgreSQL

**Создайте базу данных:**

```sql
CREATE DATABASE library_db;
CREATE USER library_user WITH PASSWORD 'your_password';
ALTER ROLE library_user SET client_encoding TO 'utf8';
ALTER ROLE library_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE library_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;
```

**Создайте файл `.env` в папке `task_1/`:**

```env
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=django-insecure-your-secret-key-change-in-production
DEBUG=True
```

### Шаг 5: Миграции базы данных

```bash
python manage.py makemigrations
python manage.py migrate
```

### Шаг 6: Создание суперпользователя

```bash
python manage.py createsuperuser
```

Введите:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123` (или любой другой)

### Шаг 7: (Опционально) Загрузка тестовых данных

Создайте файл `load_data.py` в папке `library/management/commands/`:

```python
from django.core.management.base import BaseCommand
from library.models import Author, Publisher, Genre, Book, Reader, Review
from datetime import date

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Создаем авторов
        tolstoy = Author.objects.create(
            first_name="Лев",
            last_name="Толстой",
            biography="Великий русский писатель",
            birth_date=date(1828, 9, 9),
            country="Россия"
        )
        
        # Создаем издательство
        publisher = Publisher.objects.create(
            name="АСТ",
            country="Россия",
            city="Москва",
            foundation_year=1990
        )
        
        # Создаем жанр
        genre = Genre.objects.create(
            name="Роман",
            description="Литературный жанр"
        )
        
        # Создаем книгу
        book = Book.objects.create(
            title="Война и мир",
            isbn="9785170123456",
            author=tolstoy,
            publisher=publisher,
            publication_year=1869,
            pages=1300,
            language="ru",
            description="Эпический роман о войне 1812 года",
            total_copies=5,
            available_copies=5
        )
        book.genres.add(genre)
        
        self.stdout.write(self.style.SUCCESS('Тестовые данные загружены!'))
```

Запустите:

```bash
python manage.py load_data
```

### Шаг 8: Запуск сервера

```bash
python manage.py runserver
```

Сервер запустится на `http://localhost:8000`

## Тестирование API

### 1. Через Swagger UI (Рекомендуется!)

Откройте в браузере:

```
http://localhost:8000/api/schema/swagger-ui/
```

**Преимущества Swagger UI:**
- ✅ Интерактивная документация
- ✅ Тестирование API прямо в браузере
- ✅ Автоматическая авторизация
- ✅ Просмотр схем запросов/ответов
- ✅ Примеры данных

**Как использовать:**

1. Откройте Swagger UI
2. Найдите endpoint `/api/auth/token/login/`
3. Нажмите "Try it out"
4. Введите credentials суперпользователя
5. Нажмите "Execute"
6. Скопируйте полученный токен
7. Нажмите кнопку "Authorize" вверху страницы
8. Введите: `Token <ваш_токен>`
9. Теперь можете тестировать все endpoints!

### 2. Через ReDoc

Альтернативная документация:

```
http://localhost:8000/api/schema/redoc/
```

### 3. Через Browsable API (Django REST Framework)

```
http://localhost:8000/api/
```

### 4. Через Admin панель

```
http://localhost:8000/admin/
```

Войдите с учетными данными суперпользователя.

### 5. Через Postman

**Импортируйте OpenAPI schema:**

1. Откройте Postman
2. File → Import
3. Введите URL: `http://localhost:8000/api/schema/`
4. Import

**Или создайте запросы вручную:**

**Регистрация:**
```
POST http://localhost:8000/api/auth/users/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "re_password": "testpass123"
}
```

**Получение токена:**
```
POST http://localhost:8000/api/auth/token/login/
Content-Type: application/json

{
    "username": "testuser",
    "password": "testpass123"
}
```

**Использование токена:**
```
GET http://localhost:8000/api/books/
Authorization: Token <ваш_токен>
```

### 6. Через cURL

```bash
# Регистрация
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "re_password": "testpass123"
  }'

# Получение токена
TOKEN=$(curl -X POST http://localhost:8000/api/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}' \
  | jq -r '.auth_token')

# Использование токена
curl http://localhost:8000/api/books/ \
  -H "Authorization: Token $TOKEN"

# Получить доступные книги
curl http://localhost:8000/api/books/available/ \
  -H "Authorization: Token $TOKEN"
```

### 7. Через Python requests

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Регистрация
response = requests.post(f"{BASE_URL}/auth/users/", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "re_password": "testpass123"
})
print(response.json())

# Получение токена
response = requests.post(f"{BASE_URL}/auth/token/login/", json={
    "username": "testuser",
    "password": "testpass123"
})
token = response.json()['auth_token']
print(f"Token: {token}")

# Использование API
headers = {"Authorization": f"Token {token}"}
response = requests.get(f"{BASE_URL}/books/", headers=headers)
books = response.json()
print(f"Книг найдено: {books['count']}")
```

## Запуск тестов

### Все тесты

```bash
python manage.py test
```

### Тесты конкретного приложения

```bash
python manage.py test library
```

### С подробным выводом

```bash
python manage.py test --verbosity=2
```

### Coverage (покрытие тестами)

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Проверка кода

### Линтинг (flake8)

```bash
pip install flake8
flake8 library/ --max-line-length=120
```

### Форматирование (black)

```bash
pip install black
black library/
```

## Возможные проблемы и решения

### PostgreSQL не подключается

**Ошибка:** `could not connect to server`

**Решение:**
1. Проверьте, что PostgreSQL запущен
2. Проверьте настройки в `.env`
3. Проверьте права пользователя в PostgreSQL

### Ошибка миграций

**Ошибка:** `No changes detected`

**Решение:**
```bash
python manage.py makemigrations library
python manage.py migrate
```

### Ошибка импорта модулей

**Ошибка:** `ModuleNotFoundError`

**Решение:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Ошибка с Pillow (обложки книг)

**Windows:**
```bash
pip install Pillow --no-cache-dir
```

**Linux:**
```bash
sudo apt-get install python3-dev python3-setuptools
sudo apt-get install libjpeg-dev zlib1g-dev
pip install Pillow
```

## Полезные команды

```bash
# Создать приложение
python manage.py startapp app_name

# Shell с Django окружением
python manage.py shell

# Собрать статические файлы
python manage.py collectstatic

# Проверить проект
python manage.py check

# Показать миграции
python manage.py showmigrations

# Создать дамп данных
python manage.py dumpdata > data.json

# Загрузить дамп данных
python manage.py loaddata data.json
```

## Следующие шаги

1. ✅ Изучите [Модели данных](models.md)
2. ✅ Изучите [API Reference](api.md)
3. ✅ Попробуйте [Примеры использования](examples.md)
4. ✅ Прочитайте про [Авторизацию](task3.md)

## Поддержка

При возникновении проблем:
1. Проверьте логи: `python manage.py runserver --verbosity=2`
2. Проверьте настройки в `.env`
3. Убедитесь что все зависимости установлены
4. Проверьте версию Python: `python --version`

