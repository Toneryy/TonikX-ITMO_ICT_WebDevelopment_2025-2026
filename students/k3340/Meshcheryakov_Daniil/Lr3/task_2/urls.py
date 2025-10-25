from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
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
    path('', include(router.urls)),
]

