"""
Обновленные ViewSets с интеграцией прав доступа
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date
import sys
import os

# Добавляем пути к модулям
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'task_1'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'task_2'))

from library.models import Reader, Author, Publisher, Genre, Book, Borrowing, Review
from serializers import (
    ReaderSerializer, AuthorSerializer, PublisherSerializer,
    GenreSerializer, BookListSerializer, BookDetailSerializer,
    BorrowingListSerializer, BorrowingDetailSerializer, ReviewSerializer
)
from .permissions import (
    IsStaffOrReadOnly, IsReaderOwner, IsBorrowingOwner, IsReviewOwner
)


class ReaderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с читателями с правами доступа.
    
    Права:
    - Просмотр списка: только аутентифицированные
    - Создание: персонал
    - Редактирование: владелец или персонал
    - Удаление: персонал
    """
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['first_name', 'last_name', 'email', 'passport_number']
    ordering_fields = ['registration_date', 'last_name']
    ordering = ['-registration_date']
    
    def get_permissions(self):
        """Определяем права доступа в зависимости от действия"""
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsReaderOwner]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def borrowings(self, request, pk=None):
        """Получить все выдачи конкретного читателя"""
        reader = self.get_object()
        
        # Пользователь может видеть только свои выдачи (если не персонал)
        if not request.user.is_staff:
            if not (hasattr(reader, 'user') and reader.user == request.user):
                return Response(
                    {'error': 'У вас нет доступа к этим данным'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        borrowings = reader.borrowings.all()
        serializer = BorrowingListSerializer(borrowings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def reviews(self, request, pk=None):
        """Получить все отзывы конкретного читателя"""
        reader = self.get_object()
        reviews = reader.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с авторами.
    Редактирование только для персонала.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country']
    search_fields = ['first_name', 'last_name', 'country']
    ordering_fields = ['last_name', 'birth_date']
    ordering = ['last_name']
    
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Получить все книги конкретного автора"""
        author = self.get_object()
        books = author.books.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)


class PublisherViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с издательствами.
    Редактирование только для персонала.
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country', 'city']
    search_fields = ['name', 'country', 'city']
    ordering_fields = ['name', 'foundation_year']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Получить все книги конкретного издательства"""
        publisher = self.get_object()
        books = publisher.books.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с жанрами.
    Редактирование только для персонала.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Получить все книги конкретного жанра"""
        genre = self.get_object()
        books = genre.books.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с книгами.
    
    Права:
    - Просмотр: все пользователи
    - Создание/редактирование/удаление: только персонал
    """
    queryset = Book.objects.all().select_related('author', 'publisher').prefetch_related('genres')
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publisher', 'language', 'publication_year', 'genres']
    search_fields = ['title', 'isbn', 'author__first_name', 'author__last_name', 'description']
    ordering_fields = ['title', 'publication_year', 'available_copies']
    ordering = ['title']
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'list':
            return BookListSerializer
        return BookDetailSerializer
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Получить только доступные книги"""
        books = self.queryset.filter(available_copies__gt=0)
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Получить все отзывы на конкретную книгу"""
        book = self.get_object()
        reviews = book.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def borrowings(self, request, pk=None):
        """Получить историю выдач конкретной книги (только персонал)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Доступ запрещен'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        book = self.get_object()
        borrowings = book.borrowings.all()
        serializer = BorrowingListSerializer(borrowings, many=True)
        return Response(serializer.data)


class BorrowingViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с выдачами книг.
    
    Права:
    - Просмотр списка: аутентифицированные (свои выдачи) или персонал (все)
    - Создание: аутентифицированные
    - Редактирование: владелец или персонал
    """
    queryset = Borrowing.objects.all().select_related('reader', 'book')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'reader', 'book']
    ordering_fields = ['borrow_date', 'due_date']
    ordering = ['-borrow_date']
    
    def get_permissions(self):
        """Определяем права доступа в зависимости от действия"""
        if self.action in ['create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsBorrowingOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Фильтруем queryset: пользователи видят только свои выдачи"""
        queryset = super().get_queryset()
        
        if not self.request.user.is_staff:
            # Пользователи видят только свои выдачи
            # (требует добавления поля user в модель Reader)
            queryset = queryset.filter(reader__user=self.request.user)
        
        return queryset
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'list':
            return BorrowingListSerializer
        return BorrowingDetailSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Получить все активные выдачи"""
        borrowings = self.get_queryset().filter(status='active')
        serializer = BorrowingListSerializer(borrowings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Получить все просроченные выдачи"""
        borrowings = self.get_queryset().filter(status='overdue')
        serializer = BorrowingListSerializer(borrowings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """
        Вернуть книгу.
        
        Параметры:
        - return_date: дата возврата (опционально, по умолчанию - сегодня)
        """
        borrowing = self.get_object()
        
        # Проверяем права доступа
        if not request.user.is_staff:
            if not (hasattr(borrowing.reader, 'user') and borrowing.reader.user == request.user):
                return Response(
                    {'error': 'У вас нет доступа к этой выдаче'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        if borrowing.status == 'returned':
            return Response(
                {'error': 'Книга уже возвращена'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Получаем дату возврата из запроса или используем сегодняшнюю
        return_date = request.data.get('return_date', date.today())
        
        # Обновляем выдачу
        borrowing.return_date = return_date
        borrowing.status = 'returned'
        
        # Вычисляем штраф, если книга возвращена с опозданием
        if isinstance(return_date, str):
            return_date = date.fromisoformat(return_date)
        
        if return_date > borrowing.due_date:
            days_late = (return_date - borrowing.due_date).days
            borrowing.fine_amount = days_late * 10  # 10 рублей за день просрочки
        
        borrowing.save()
        
        # Увеличиваем количество доступных копий
        book = borrowing.book
        book.available_copies += 1
        book.save()
        
        serializer = BorrowingDetailSerializer(borrowing)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с отзывами.
    
    Права:
    - Просмотр: все пользователи
    - Создание: аутентифицированные
    - Редактирование/удаление: владелец или персонал
    """
    queryset = Review.objects.all().select_related('reader', 'book')
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rating', 'book', 'reader']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Определяем права доступа в зависимости от действия"""
        if self.action in ['create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsReviewOwner]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

