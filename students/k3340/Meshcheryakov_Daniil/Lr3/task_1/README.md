# Подзадача 1: Настройка проекта и модели БД

## Описание
Создание Django проекта с Django REST Framework и настройка расширенных моделей для системы "Читальный зал" с использованием PostgreSQL.

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Настройка PostgreSQL

Создайте файл `.env` в корне проекта:

```
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## Создание базы данных

```sql
CREATE DATABASE library_db;
```

## Миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

## Создание суперпользователя

```bash
python manage.py createsuperuser
```

## Запуск сервера

```bash
python manage.py runserver
```

## Модели данных

### Reader (Читатель)
- first_name - Имя
- last_name - Фамилия
- email - Email (уникальный)
- phone - Телефон
- date_of_birth - Дата рождения
- address - Адрес
- registration_date - Дата регистрации
- is_active - Активен ли аккаунт
- passport_number - Номер паспорта (уникальный)

### Author (Автор)
- first_name - Имя
- last_name - Фамилия
- biography - Биография
- birth_date - Дата рождения
- country - Страна

### Publisher (Издательство)
- name - Название
- country - Страна
- city - Город
- foundation_year - Год основания
- website - Сайт

### Genre (Жанр)
- name - Название
- description - Описание

### Book (Книга)
- title - Название
- isbn - ISBN (уникальный)
- author - Автор (ForeignKey)
- publisher - Издательство (ForeignKey)
- genres - Жанры (ManyToMany)
- publication_year - Год издания
- pages - Количество страниц
- language - Язык
- description - Описание
- cover_image - Обложка
- available_copies - Доступных экземпляров
- total_copies - Всего экземпляров

### Borrowing (Выдача книги)
- reader - Читатель (ForeignKey)
- book - Книга (ForeignKey)
- borrow_date - Дата выдачи
- due_date - Дата возврата (план)
- return_date - Дата возврата (факт)
- status - Статус (активна/возвращена/просрочена)
- fine_amount - Сумма штрафа

### Review (Отзыв)
- reader - Читатель (ForeignKey)
- book - Книга (ForeignKey)
- rating - Оценка (1-5)
- comment - Комментарий
- created_at - Дата создания

