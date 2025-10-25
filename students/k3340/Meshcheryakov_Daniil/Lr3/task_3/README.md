# Подзадача 3: Авторизация и аутентификация

## Описание
Интеграция Djoser для регистрации пользователей, авторизации по токенам и управления правами доступа.

## Функциональность

### Регистрация и авторизация
- Регистрация новых пользователей
- Авторизация по токенам (Token Authentication)
- Получение информации о текущем пользователе
- Изменение пароля
- Сброс пароля (опционально)

### Права доступа (Permissions)
- Неавторизованные пользователи: только чтение
- Авторизованные пользователи: полный CRUD для своих записей
- Персонал (staff): полный доступ ко всем операциям

### Эндпоинты Djoser

#### Пользователи
- `POST /api/auth/users/` - регистрация нового пользователя
- `GET /api/auth/users/me/` - получить информацию о текущем пользователе
- `PUT/PATCH /api/auth/users/me/` - обновить информацию о текущем пользователе
- `DELETE /api/auth/users/me/` - удалить текущего пользователя

#### Токены
- `POST /api/auth/token/login/` - получить токен (login)
- `POST /api/auth/token/logout/` - удалить токен (logout)

#### Пароль
- `POST /api/auth/users/set_password/` - изменить пароль
- `POST /api/auth/users/reset_password/` - запросить сброс пароля
- `POST /api/auth/users/reset_password_confirm/` - подтвердить сброс пароля

## Примеры использования

### Регистрация
```bash
POST /api/auth/users/
Content-Type: application/json

{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "strong_password123",
    "re_password": "strong_password123"
}
```

### Авторизация
```bash
POST /api/auth/token/login/
Content-Type: application/json

{
    "username": "newuser",
    "password": "strong_password123"
}

# Ответ:
{
    "auth_token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Использование токена
```bash
GET /api/books/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Получение информации о текущем пользователе
```bash
GET /api/auth/users/me/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Изменение пароля
```bash
POST /api/auth/users/set_password/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json

{
    "new_password": "new_strong_password123",
    "re_new_password": "new_strong_password123",
    "current_password": "strong_password123"
}
```

### Выход
```bash
POST /api/auth/token/logout/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## Настройка прав доступа

Реализованы следующие классы permissions:
- `IsOwnerOrReadOnly` - владелец может редактировать, остальные только читать
- `IsStaffOrReadOnly` - персонал может редактировать, остальные только читать
- `IsAuthenticatedOrReadOnly` - авторизованные могут редактировать, остальные только читать

## Интеграция с моделями

### Связь User с Reader
Каждый зарегистрированный пользователь может быть связан с моделью Reader.
При регистрации можно автоматически создавать профиль читателя.

