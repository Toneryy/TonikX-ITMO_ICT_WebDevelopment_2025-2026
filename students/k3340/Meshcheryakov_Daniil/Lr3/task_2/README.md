# Подзадача 2: API Endpoints

## Описание
Реализация RESTful API endpoints для всех моделей библиотеки с использованием Django REST Framework.

## Компоненты

### Сериализаторы (serializers.py)
- `ReaderSerializer` - для модели читателей
- `AuthorSerializer` - для модели авторов
- `PublisherSerializer` - для издательств
- `GenreSerializer` - для жанров
- `BookSerializer` - для книг (с вложенными данными)
- `BorrowingSerializer` - для выдач книг
- `ReviewSerializer` - для отзывов

### ViewSets (views.py)
- `ReaderViewSet` - CRUD операции для читателей
- `AuthorViewSet` - CRUD операции для авторов
- `PublisherViewSet` - CRUD операции для издательств
- `GenreViewSet` - CRUD операции для жанров
- `BookViewSet` - CRUD операции для книг + фильтрация и поиск
- `BorrowingViewSet` - CRUD операции для выдач + кастомные действия
- `ReviewViewSet` - CRUD операции для отзывов

### URL Routing (urls.py)
Все endpoints организованы с использованием `DefaultRouter`:
- `/api/readers/` - читатели
- `/api/authors/` - авторы
- `/api/publishers/` - издательства
- `/api/genres/` - жанры
- `/api/books/` - книги
- `/api/borrowings/` - выдачи книг
- `/api/reviews/` - отзывы

## Функциональность

### Фильтрация
- Книги: по автору, жанру, языку, году издания, доступности
- Выдачи: по статусу, читателю, книге
- Отзывы: по оценке, книге

### Поиск
- Книги: по названию, автору, ISBN
- Читатели: по имени, email
- Авторы: по имени, стране

### Кастомные действия
- `BookViewSet.available` - получить только доступные книги
- `BookViewSet.by_genre` - получить книги по жанру
- `BorrowingViewSet.active` - получить активные выдачи
- `BorrowingViewSet.overdue` - получить просроченные выдачи
- `BorrowingViewSet.return_book` - вернуть книгу

## Тестирование API

Примеры запросов:

```bash
# Получить все книги
GET http://localhost:8000/api/books/

# Получить книги с фильтрацией
GET http://localhost:8000/api/books/?author=1&language=ru

# Поиск книг
GET http://localhost:8000/api/books/?search=Война

# Создать читателя
POST http://localhost:8000/api/readers/
{
    "first_name": "Иван",
    "last_name": "Иванов",
    "email": "ivan@example.com",
    "passport_number": "1234567890"
}

# Взять книгу
POST http://localhost:8000/api/borrowings/
{
    "reader": 1,
    "book": 1,
    "borrow_date": "2024-01-15",
    "due_date": "2024-01-29"
}

# Вернуть книгу
POST http://localhost:8000/api/borrowings/1/return_book/
{
    "return_date": "2024-01-28"
}
```

