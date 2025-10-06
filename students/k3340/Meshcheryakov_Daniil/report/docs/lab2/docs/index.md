# Лабораторная работа №2

**Студент:** Мещеряков Даниил Павлович  
**Группа:** K3340  
**ИСУ:** 409130  
**Поток:** WEB 2.3  

---

## 🎯 Цели работы

* Освоить базовые принципы работы с **Django Framework**.
* Научиться создавать **CRUD**-интерфейсы, подключать **Bootstrap**, **пагинацию** и **поиск**.
* Получить опыт организации Django-проекта и шаблонов.

---

## 📘 Структура заданий

| №   | Название                                                | Ссылка                      |
| --- | ------------------------------------------------------- | --------------------------- |
| 2.1 | Базовый CRUD — создание, редактирование и удаление книг | [Открыть отчёт](practice2_1.md) |
| 2.2 | Добавление пагинации и поиска                           | [Открыть отчёт](practice2_2.md) |
| 2.3 | Подключение Bootstrap и оформление страницы             | [Открыть отчёт](practice2_3.md) |

---

## ⚙️ Используемые технологии

* **Python 3.12+**
* **Django**
* **Bootstrap 5**
* **SQLite3**
* **HTML / CSS**

---

## 🧩 Структура проекта

```
simple_django_web_project/
│
├── manage.py
├── db.sqlite3
├── books/                ← приложение с CRUD
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   └── books/
│   │       ├── book_list.html
│   │       ├── book_form.html
│   │       └── book_confirm_delete.html
│   └── ...
│
└── report/
    ├── docs/
    │   ├── index.md
    │   ├── task2_1.md
    │   ├── task2_2.md
    │   ├── task2_3.md
    └── mkdocs.yml
```

---

## 🌐 Ссылка на отчёт (GitHub Pages)

👉 [https://vash_login.github.io/TonikX-ITMO_ICT_WebDevelopment_2025-2026/students/k3340/Meshcheryakov_Daniil/simple_django_web_project/report/](#)
