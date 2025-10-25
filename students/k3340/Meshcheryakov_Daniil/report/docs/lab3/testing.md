# Тестирование API

Подробное руководство по тестированию всех возможностей Library API.

## Подготовка

Убедитесь, что:
1. ✅ Сервер запущен: `python manage.py runserver`
2. ✅ База данных создана и миграции применены
3. ✅ Создан суперпользователь

## Способы тестирования

### 1. Swagger UI (Рекомендуется!)

**URL:** `http://localhost:8000/api/schema/swagger-ui/`

#### Пошаговая инструкция:

**Шаг 1: Откройте Swagger UI**

Перейдите по ссылке в браузере.

**Шаг 2: Авторизация**

1. Найдите раздел **auth** → `/api/auth/token/login/`
2. Нажмите на endpoint
3. Нажмите кнопку **"Try it out"**
4. Заполните JSON:
```json
{
  "username": "admin",
  "password": "ваш_пароль"
}
```
5. Нажмите **"Execute"**
6. В разделе **Response body** скопируйте значение `auth_token`

**Шаг 3: Установка токена**

1. Нажмите кнопку **"Authorize"** в правом верхнем углу (иконка замка)
2. В поле **Value** введите: `Token ваш_токен`
   - Пример: `Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`
3. Нажмите **"Authorize"**
4. Закройте окно

**Шаг 4: Тестируем endpoints**

Теперь вы можете тестировать любые endpoints!

**Пример - Создание автора:**

1. Найдите **authors** → `POST /api/authors/`
2. Нажмите **"Try it out"**
3. Заполните Request body:
```json
{
  "first_name": "Лев",
  "last_name": "Толстой",
  "biography": "Великий русский писатель",
  "birth_date": "1828-09-09",
  "country": "Россия"
}
```
4. Нажмите **"Execute"**
5. Проверьте Response (должен быть 201 Created)

**Пример - Создание книги:**

1. `POST /api/books/`
2. Request body:
```json
{
  "title": "Война и мир",
  "isbn": "9785170123456",
  "author_id": 1,
  "genre_ids": [1],
  "publication_year": 1869,
  "language": "ru",
  "pages": 1300,
  "description": "Эпический роман",
  "total_copies": 5,
  "available_copies": 5
}
```

**Пример - Взять книгу:**

1. `POST /api/borrowings/`
2. Request body:
```json
{
  "reader_id": 1,
  "book_id": 1,
  "borrow_date": "2024-01-15",
  "due_date": "2024-01-29"
}
```

**Пример - Вернуть книгу:**

1. `POST /api/borrowings/{id}/return_book/`
2. Request body:
```json
{
  "return_date": "2024-01-22"
}
```

---

### 2. ReDoc

**URL:** `http://localhost:8000/api/schema/redoc/`

ReDoc предоставляет красивую документацию только для чтения. Хорошо подходит для изучения API, но не для тестирования.

---

### 3. Browsable API (DRF)

**URL:** `http://localhost:8000/api/`

Django REST Framework предоставляет веб-интерфейс.

**Авторизация:**
1. Войдите через админку: `http://localhost:8000/admin/`
2. После этого вы будете авторизованы во всех DRF endpoints

**Использование:**
- Переходите по ссылкам endpoints
- Заполняйте формы для POST/PUT запросов
- Просматривайте JSON ответы

---

### 4. Postman

#### Импорт OpenAPI schema:

1. Откройте Postman
2. **File** → **Import**
3. Вкладка **Link**
4. Вставьте: `http://localhost:8000/api/schema/`
5. Нажмите **Continue** → **Import**

Все endpoints будут автоматически добавлены!

#### Настройка авторизации:

**Способ 1: Глобальные переменные**

1. Создайте окружение (Environment)
2. Добавьте переменную `token`
3. Получите токен через `/api/auth/token/login/`
4. Сохраните токен в переменной

**Способ 2: На уровне коллекции**

1. Выберите коллекцию
2. **Authorization** → Type: **API Key**
3. Key: `Authorization`
4. Value: `Token {{token}}`
5. Add to: **Header**

#### Примеры запросов:

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

**Список книг:**
```
GET http://localhost:8000/api/books/
Authorization: Token ваш_токен
```

---

### 5. cURL

#### Регистрация
```bash
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "re_password": "testpass123"
  }'
```

#### Получение токена
```bash
TOKEN=$(curl -X POST http://localhost:8000/api/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}' \
  | jq -r '.auth_token')

echo "Token: $TOKEN"
```

#### Список книг
```bash
curl http://localhost:8000/api/books/ \
  -H "Authorization: Token $TOKEN"
```

#### Создание книги
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Анна Каренина",
    "isbn": "9785170123457",
    "author_id": 1,
    "genre_ids": [1],
    "publication_year": 1877,
    "language": "ru",
    "total_copies": 3,
    "available_copies": 3
  }'
```

#### Поиск книг
```bash
curl "http://localhost:8000/api/books/?search=Толстой" \
  -H "Authorization: Token $TOKEN"
```

#### Фильтрация
```bash
curl "http://localhost:8000/api/books/?language=ru&ordering=-publication_year" \
  -H "Authorization: Token $TOKEN"
```

---

### 6. Python requests

```python
import requests
from datetime import date, timedelta

BASE_URL = "http://localhost:8000/api"

class LibraryAPI:
    def __init__(self):
        self.token = None
        self.headers = {}
    
    def register(self, username, email, password):
        """Регистрация"""
        response = requests.post(f"{BASE_URL}/auth/users/", json={
            "username": username,
            "email": email,
            "password": password,
            "re_password": password
        })
        return response.json()
    
    def login(self, username, password):
        """Авторизация"""
        response = requests.post(f"{BASE_URL}/auth/token/login/", json={
            "username": username,
            "password": password
        })
        self.token = response.json()['auth_token']
        self.headers = {"Authorization": f"Token {self.token}"}
        return self.token
    
    def get_books(self, **params):
        """Получить книги"""
        response = requests.get(f"{BASE_URL}/books/", 
                              params=params,
                              headers=self.headers)
        return response.json()
    
    def create_book(self, book_data):
        """Создать книгу"""
        response = requests.post(f"{BASE_URL}/books/",
                               json=book_data,
                               headers=self.headers)
        return response.json()
    
    def borrow_book(self, reader_id, book_id, days=14):
        """Взять книгу"""
        today = date.today()
        due = today + timedelta(days=days)
        
        response = requests.post(f"{BASE_URL}/borrowings/", json={
            "reader_id": reader_id,
            "book_id": book_id,
            "borrow_date": str(today),
            "due_date": str(due)
        }, headers=self.headers)
        return response.json()
    
    def return_book(self, borrowing_id):
        """Вернуть книгу"""
        response = requests.post(
            f"{BASE_URL}/borrowings/{borrowing_id}/return_book/",
            json={"return_date": str(date.today())},
            headers=self.headers
        )
        return response.json()

# Использование:
api = LibraryAPI()

# Регистрация
api.register("testuser", "test@example.com", "pass123")

# Авторизация
token = api.login("testuser", "pass123")
print(f"Token: {token}")

# Получить книги
books = api.get_books(search="Война")
print(f"Найдено книг: {books['count']}")

# Создать книгу (требуется права персонала)
book = api.create_book({
    "title": "Новая книга",
    "isbn": "9785170999999",
    "author_id": 1,
    "genre_ids": [1],
    "publication_year": 2024,
    "language": "ru",
    "total_copies": 2,
    "available_copies": 2
})
```

---

## Сценарии тестирования

### Сценарий 1: Регистрация и авторизация

1. ✅ Зарегистрировать нового пользователя
2. ✅ Получить токен авторизации
3. ✅ Получить информацию о себе `/api/auth/users/me/`
4. ✅ Изменить email
5. ✅ Изменить пароль
6. ✅ Выйти (удалить токен)

### Сценарий 2: Работа с книгами

1. ✅ Получить список всех книг
2. ✅ Поиск книги по названию
3. ✅ Фильтрация по языку и году
4. ✅ Получить только доступные книги `/api/books/available/`
5. ✅ Получить детали конкретной книги
6. ✅ Посмотреть отзывы на книгу `/api/books/{id}/reviews/`
7. ✅ Создать новую книгу (персонал)

### Сценарий 3: Выдача и возврат книг

1. ✅ Создать читателя
2. ✅ Взять книгу (создать borrowing)
3. ✅ Проверить, что available_copies уменьшился
4. ✅ Получить список активных выдач `/api/borrowings/active/`
5. ✅ Вернуть книгу `/api/borrowings/{id}/return_book/`
6. ✅ Проверить, что available_copies увеличился
7. ✅ Проверить расчет штрафа при просрочке

### Сценарий 4: Отзывы

1. ✅ Создать отзыв на книгу
2. ✅ Получить все отзывы
3. ✅ Фильтрация по оценке
4. ✅ Обновить свой отзыв
5. ✅ Удалить свой отзыв

### Сценарий 5: Права доступа

1. ✅ Неавторизованный: может читать книги
2. ✅ Неавторизованный: НЕ может создавать книги (403)
3. ✅ Обычный пользователь: может создавать отзывы
4. ✅ Обычный пользователь: НЕ может создавать книги (403)
5. ✅ Персонал: может создавать/редактировать книги
6. ✅ Персонал: может видеть все выдачи

---

## Проверка функциональности

### ✅ Модели и CRUD

- [ ] Создание всех типов объектов (Reader, Author, Book, etc.)
- [ ] Чтение списков с пагинацией
- [ ] Чтение деталей объектов
- [ ] Обновление объектов (PUT/PATCH)
- [ ] Удаление объектов

### ✅ Фильтрация и поиск

- [ ] Поиск книг по названию
- [ ] Поиск книг по автору
- [ ] Фильтрация по языку
- [ ] Фильтрация по году издания
- [ ] Сортировка по разным полям

### ✅ Кастомные действия

- [ ] `/api/books/available/` - доступные книги
- [ ] `/api/borrowings/active/` - активные выдачи
- [ ] `/api/borrowings/overdue/` - просроченные выдачи
- [ ] `/api/borrowings/{id}/return_book/` - возврат книги
- [ ] `/api/authors/{id}/books/` - книги автора
- [ ] `/api/books/{id}/reviews/` - отзывы на книгу

### ✅ Аутентификация

- [ ] Регистрация пользователя
- [ ] Получение токена
- [ ] Использование токена в заголовках
- [ ] Получение информации о себе
- [ ] Изменение пароля
- [ ] Удаление токена (logout)

### ✅ Права доступа

- [ ] Неавторизованные могут читать книги
- [ ] Неавторизованные НЕ могут создавать книги
- [ ] Авторизованные могут создавать отзывы
- [ ] Только персонал может создавать книги
- [ ] Пользователи видят только свои выдачи
- [ ] Персонал видит все выдачи

### ✅ Бизнес-логика

- [ ] При создании выдачи уменьшается available_copies
- [ ] При возврате книги увеличивается available_copies
- [ ] Автоматический расчет штрафа при просрочке
- [ ] Нельзя взять книгу, если available_copies = 0
- [ ] Автоматическая смена статуса на 'overdue'
- [ ] Расчет среднего рейтинга книги

---

## Полезные команды

### Сброс базы данных

```bash
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

### Создание тестовых данных

```bash
python manage.py shell
```

```python
from library.models import *
from datetime import date

# Автор
author = Author.objects.create(
    first_name="Лев",
    last_name="Толстой",
    birth_date=date(1828, 9, 9),
    country="Россия"
)

# Жанр
genre = Genre.objects.create(name="Роман")

# Издательство
publisher = Publisher.objects.create(
    name="АСТ",
    country="Россия",
    city="Москва"
)

# Книга
book = Book.objects.create(
    title="Война и мир",
    isbn="9785170123456",
    author=author,
    publisher=publisher,
    publication_year=1869,
    language="ru",
    total_copies=5,
    available_copies=5
)
book.genres.add(genre)

# Читатель
reader = Reader.objects.create(
    first_name="Иван",
    last_name="Иванов",
    email="ivan@example.com",
    passport_number="1234567890"
)
```

---

## Отладка

### Просмотр SQL запросов

```python
from django.conf import settings
settings.DEBUG = True

from django.db import connection
from library.models import Book

books = Book.objects.all()
print(connection.queries)
```

### Логирование

Добавьте в `settings.py`:

```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

