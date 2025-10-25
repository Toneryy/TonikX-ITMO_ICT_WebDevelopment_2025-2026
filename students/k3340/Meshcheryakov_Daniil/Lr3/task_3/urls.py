from django.urls import path, include
from rest_framework.routers import DefaultRouter
import sys
import os

# Добавляем путь к модулям из task_2
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'task_2'))

from views import (
    ReaderViewSet, AuthorViewSet, PublisherViewSet,
    GenreViewSet, BookViewSet, BorrowingViewSet, ReviewViewSet
)

# Создаем роутер и регистрируем ViewSets
router = DefaultRouter()
router.register(r'readers', ReaderViewSet, basename='reader')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'publishers', PublisherViewSet, basename='publisher')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'books', BookViewSet, basename='book')
router.register(r'borrowings', BorrowingViewSet, basename='borrowing')
router.register(r'reviews', ReviewViewSet, basename='review')

app_name = 'api'

urlpatterns = [
    # Djoser endpoints для аутентификации
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    
    # API endpoints
    path('', include(router.urls)),
]

