from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'library'

# Создаем роутер для ViewSets
router = DefaultRouter()
router.register(r'readers', views.ReaderViewSet, basename='reader')
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'publishers', views.PublisherViewSet, basename='publisher')
router.register(r'genres', views.GenreViewSet, basename='genre')
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'borrowings', views.BorrowingViewSet, basename='borrowing')
router.register(r'reviews', views.ReviewViewSet, basename='review')

urlpatterns = [
    # Djoser endpoints для аутентификации
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    
    # API root
    path('', views.api_root, name='api-root'),
    
    # ViewSets через роутер
    path('', include(router.urls)),
]

