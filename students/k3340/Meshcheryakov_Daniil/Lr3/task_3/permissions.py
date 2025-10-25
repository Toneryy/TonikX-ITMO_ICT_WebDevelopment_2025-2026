from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать объект только его владельцу.
    Все остальные пользователи имеют только доступ на чтение.
    """
    
    def has_object_permission(self, request, view, obj):
        # Права на чтение разрешены для любого запроса
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Права на запись разрешены только владельцу объекта
        return obj.owner == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать объект только персоналу.
    Все остальные пользователи имеют только доступ на чтение.
    """
    
    def has_permission(self, request, view):
        # Права на чтение разрешены для любого запроса
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Права на запись разрешены только персоналу
        return request.user and request.user.is_staff


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать объект только аутентифицированным пользователям.
    Неаутентифицированные пользователи имеют только доступ на чтение.
    """
    
    def has_permission(self, request, view):
        # Права на чтение разрешены для любого запроса
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Права на запись разрешены только аутентифицированным пользователям
        return request.user and request.user.is_authenticated


class IsReaderOwner(permissions.BasePermission):
    """
    Разрешение для модели Reader.
    Позволяет пользователю редактировать только свой профиль читателя.
    """
    
    def has_object_permission(self, request, view, obj):
        # Права на чтение разрешены для аутентифицированных пользователей
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Права на запись - только владелец или персонал
        if request.user.is_staff:
            return True
        
        # Проверяем, связан ли пользователь с этим профилем читателя
        # (требует добавления поля user в модель Reader)
        return hasattr(obj, 'user') and obj.user == request.user


class IsBorrowingOwner(permissions.BasePermission):
    """
    Разрешение для модели Borrowing.
    Позволяет читателю видеть и управлять только своими выдачами.
    """
    
    def has_permission(self, request, view):
        # Создавать выдачи могут только аутентифицированные пользователи
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Персонал видит все
        if request.user.is_staff:
            return True
        
        # Читатель видит только свои выдачи
        return hasattr(obj.reader, 'user') and obj.reader.user == request.user


class IsReviewOwner(permissions.BasePermission):
    """
    Разрешение для модели Review.
    Позволяет пользователю редактировать только свои отзывы.
    """
    
    def has_permission(self, request, view):
        # Создавать отзывы могут только аутентифицированные пользователи
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return True
    
    def has_object_permission(self, request, view, obj):
        # Читать могут все
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Редактировать/удалять может только автор отзыва или персонал
        if request.user.is_staff:
            return True
        
        return hasattr(obj.reader, 'user') and obj.reader.user == request.user

