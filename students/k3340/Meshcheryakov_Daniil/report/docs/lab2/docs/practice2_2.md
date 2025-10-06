# Практическая работа №2.2: Реализация CRUD-интерфейса средствами Django

## Цель работы

Научиться реализовывать CRUD-интерфейсы (_Create, Read, Update, Delete_) средствами Django Web Framework.

---

## Ход работы

### 1. Создание модели Book

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} ({self.author}, {self.year})"
```

---

### 2. Настройка views.py

```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm

def book_list(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", {"books": books})

def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "books/book_form.html", {"form": form, "title": "Добавить книгу"})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "books/book_form.html", {"form": form, "title": "Редактировать книгу"})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "books/book_delete.html", {"book": book})
```

---

### 3. Форма (forms.py)

```python
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "year"]
```

---

### 4. Настройка URL-маршрутов

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("create/", views.book_create, name="book_create"),
    path("<int:pk>/update/", views.book_update, name="book_update"),
    path("<int:pk>/delete/", views.book_delete, name="book_delete"),
]
```

---

### 5. Шаблоны

#### 📄 `book_list.html`

```html
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <title>Список книг</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
  </head>
  <body class="bg-light">
    <div class="container py-5">
      <h1 class="mb-4 text-center">📚 Список книг</h1>

      <div class="text-end mb-3">
        <a href="{% url 'book_create' %}" class="btn btn-success"
          >➕ Добавить книгу</a
        >
      </div>

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
            <td class="text-center">{{ forloop.counter }}</td>
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td class="text-center">{{ book.year }}</td>
            <td class="text-center">
              <a
                href="{% url 'book_update' book.pk %}"
                class="btn btn-warning btn-sm"
                >✏</a
              >
              <a
                href="{% url 'book_delete' book.pk %}"
                class="btn btn-danger btn-sm"
                >🗑</a
              >
            </td>
          </tr>
          {% empty %}
          <tr>
            <td colspan="5" class="text-center text-muted">Нет книг</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </body>
</html>
```

---

#### 📄 `book_form.html`

```html
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <title>{{ title }}</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
  </head>
  <body class="bg-light">
    <div class="container py-5">
      <h2 class="mb-4 text-center">{{ title }}</h2>
      <form method="post" class="card p-4 shadow-sm bg-white">
        {% csrf_token %} {{ form.as_p }}
        <button class="btn btn-primary">💾 Сохранить</button>
        <a href="{% url 'book_list' %}" class="btn btn-secondary">⬅ Назад</a>
      </form>
    </div>
  </body>
</html>
```

---

#### 📄 `book_delete.html`

```html
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <title>Удаление книги</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
  </head>
  <body class="bg-light">
    <div class="container py-5 text-center">
      <h3 class="mb-4">Удалить книгу "{{ book.title }}"?</h3>
      <form method="post">
        {% csrf_token %}
        <button class="btn btn-danger">🗑 Удалить</button>
        <a href="{% url 'book_list' %}" class="btn btn-secondary">Отмена</a>
      </form>
    </div>
  </body>
</html>
```

---

## Результаты

- Реализованы функции добавления, редактирования, просмотра и удаления книг.
- Все действия выполняются через веб-интерфейс на Django.
- Интерфейс оформлен с помощью **Bootstrap 5**.

---

## Выводы

1. Освоена базовая реализация CRUD-интерфейсов в Django.
2. Использованы формы `ModelForm` для удобства работы с моделями.
3. В шаблонах применены теги Django (`{% csrf_token %}`, `{% for %}` и др.).
4. Интерфейс стал понятным и аккуратным благодаря Bootstrap.
