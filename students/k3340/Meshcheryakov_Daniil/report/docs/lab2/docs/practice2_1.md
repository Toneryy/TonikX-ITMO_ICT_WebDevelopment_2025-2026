# Практическая работа 2.2: Реализация CRUD-интерфейса в Django

## Условие

Реализовать CRUD (Create, Read, Update, Delete) интерфейс для работы с объектами модели **Book**.
Пользователь должен иметь возможность добавлять, просматривать, редактировать и удалять книги.
Для отображения данных использовать HTML-шаблоны и **Bootstrap** для оформления.

---

## Код программы

### `models.py`

```python
from django.db import models

class Book(models.Model):
    title = models.CharField("Название", max_length=200)
    author = models.CharField("Автор", max_length=100)
    year = models.IntegerField("Год издания")

    def __str__(self):
        return f"{self.title} ({self.author})"
```

---

### `views.py`

```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request, 'main/book_list.html', {'books': books})

def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        year = request.POST.get('year')
        Book.objects.create(title=title, author=author, year=year)
        return redirect('book_list')
    return render(request, 'main/book_form.html')

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.year = request.POST.get('year')
        book.save()
        return redirect('book_list')
    return render(request, 'main/book_form.html', {'book': book})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'main/book_confirm_delete.html', {'book': book})
```

---

### `urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.book_create, name='book_create'),
    path('edit/<int:pk>/', views.book_update, name='book_update'),
    path('delete/<int:pk>/', views.book_delete, name='book_delete'),
]
```

---

### `book_list.html`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Список книг</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-5">
  <h1 class="mb-4 text-center">📚 Список книг</h1>
  <div class="d-flex justify-content-end mb-3">
    <a href="{% url 'book_create' %}" class="btn btn-primary">➕ Добавить книгу</a>
  </div>

  {% if books %}
  <table class="table table-striped table-bordered align-middle">
    <thead class="table-dark text-center">
      <tr>
        <th>#</th>
        <th>Название</th>
        <th>Автор</th>
        <th>Год</th>
        <th>Действия</th>
      </tr>
    </thead>
    <tbody>
      {% for book in books %}
      <tr>
        <td>{{ forloop.counter }}</td>
        <td>{{ book.title }}</td>
        <td>{{ book.author }}</td>
        <td>{{ book.year }}</td>
        <td class="text-center">
          <a href="{% url 'book_update' book.pk %}" class="btn btn-sm btn-warning">✏ Редактировать</a>
          <a href="{% url 'book_delete' book.pk %}" class="btn btn-sm btn-danger">🗑 Удалить</a>
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  {% else %}
  <div class="alert alert-info text-center">Нет добавленных книг.</div>
  {% endif %}
</div>
</body>
</html>
```

---

### `book_form.html`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>{% if book %}Редактировать книгу{% else %}Добавить книгу{% endif %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-5">
  <div class="card shadow-sm">
    <div class="card-body">
      <h2 class="mb-4">{% if book %}Редактировать{% else %}Добавить{% endif %} книгу</h2>
      <form method="post">
        {% csrf_token %}
        <div class="mb-3">
          <label class="form-label">Название</label>
          <input type="text" name="title" class="form-control" value="{{ book.title|default:'' }}" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Автор</label>
          <input type="text" name="author" class="form-control" value="{{ book.author|default:'' }}" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Год издания</label>
          <input type="number" name="year" class="form-control" value="{{ book.year|default:'' }}" required>
        </div>
        <button type="submit" class="btn btn-success">💾 Сохранить</button>
        <a href="{% url 'book_list' %}" class="btn btn-secondary">⬅ Назад</a>
      </form>
    </div>
  </div>
</div>
</body>
</html>
```

---

### `book_confirm_delete.html`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Удаление книги</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-5">
  <div class="card shadow-sm text-center">
    <div class="card-body">
      <h2>Удалить книгу "{{ book.title }}"?</h2>
      <form method="post" class="mt-4">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">✅ Да, удалить</button>
        <a href="{% url 'book_list' %}" class="btn btn-secondary">❌ Отмена</a>
      </form>
    </div>
  </div>
</div>
</body>
</html>
```

---

## Запуск

1) Выполнить миграции:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2) Запустить сервер:

   ```bash
   python manage.py runserver
   ```

3) Перейти в браузере по адресу:

   ```
   http://127.0.0.1:8000/
   ```

---

## Результат

На странице отображается список книг.
Пользователь может:

* добавлять новые книги;
* редактировать существующие;
* удалять записи.

Интерфейс оформлен с использованием **Bootstrap**.

---

## Выводы

1. Реализованы все операции CRUD для модели **Book**.
2. Интерфейс оформлен с помощью Bootstrap, что улучшает визуальное восприятие.
3. Работа с базой данных выполняется средствами **Django ORM**.
4. Проект готов к дальнейшему расширению и интеграции дополнительных функций.
