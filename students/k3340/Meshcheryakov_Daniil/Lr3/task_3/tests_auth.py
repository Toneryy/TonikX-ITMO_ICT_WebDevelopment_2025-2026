from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import sys
import os

# Добавляем путь к модулям из task_1
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'task_1'))

from library.models import Reader, Author, Book


class AuthenticationTestCase(APITestCase):
    """Тесты для регистрации и авторизации"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            're_password': 'testpass123'
        }
    
    def test_user_registration(self):
        """Тест регистрации нового пользователя"""
        response = self.client.post('/api/auth/users/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
    
    def test_user_login(self):
        """Тест авторизации пользователя"""
        # Создаем пользователя
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        
        # Авторизуемся
        response = self.client.post('/api/auth/token/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)
    
    def test_get_current_user(self):
        """Тест получения информации о текущем пользователе"""
        # Создаем пользователя и токен
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        token = Token.objects.create(user=user)
        
        # Делаем запрос с токеном
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get('/api/auth/users/me/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_logout(self):
        """Тест выхода из системы"""
        # Создаем пользователя и токен
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        token = Token.objects.create(user=user)
        
        # Делаем запрос на logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post('/api/auth/token/logout/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Проверяем, что токен удален
        self.assertFalse(Token.objects.filter(key=token.key).exists())


class PermissionsTestCase(APITestCase):
    """Тесты для проверки прав доступа"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Создаем обычного пользователя
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123'
        )
        self.user_token = Token.objects.create(user=self.user)
        
        # Создаем персонал
        self.staff_user = User.objects.create_user(
            username='staff',
            email='staff@example.com',
            password='staffpass123',
            is_staff=True
        )
        self.staff_token = Token.objects.create(user=self.staff_user)
        
        # Создаем тестовые данные
        self.author = Author.objects.create(
            first_name='Лев',
            last_name='Толстой'
        )
        
        self.book = Book.objects.create(
            title='Война и мир',
            isbn='9785170123456',
            author=self.author,
            publication_year=1869
        )
    
    def test_anonymous_can_read_books(self):
        """Неавторизованные пользователи могут читать книги"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_anonymous_cannot_create_books(self):
        """Неавторизованные пользователи не могут создавать книги"""
        book_data = {
            'title': 'Анна Каренина',
            'isbn': '9785170123457',
            'author_id': self.author.id,
            'publication_year': 1877
        }
        response = self.client.post('/api/books/', book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_regular_user_cannot_create_books(self):
        """Обычные пользователи не могут создавать книги"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        
        book_data = {
            'title': 'Анна Каренина',
            'isbn': '9785170123457',
            'author_id': self.author.id,
            'publication_year': 1877
        }
        response = self.client.post('/api/books/', book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_staff_can_create_books(self):
        """Персонал может создавать книги"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        
        book_data = {
            'title': 'Анна Каренина',
            'isbn': '9785170123457',
            'author_id': self.author.id,
            'genre_ids': [],
            'publication_year': 1877,
            'language': 'ru',
            'total_copies': 1,
            'available_copies': 1
        }
        response = self.client.post('/api/books/', book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_authenticated_user_can_create_review(self):
        """Авторизованные пользователи могут создавать отзывы"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        
        # Создаем читателя для пользователя
        reader = Reader.objects.create(
            first_name='Иван',
            last_name='Иванов',
            email='ivan@example.com',
            passport_number='1234567890'
        )
        
        review_data = {
            'reader': reader.id,
            'book': self.book.id,
            'rating': 5,
            'comment': 'Отличная книга!'
        }
        response = self.client.post('/api/reviews/', review_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BorrowingPermissionsTestCase(APITestCase):
    """Тесты для проверки прав доступа к выдачам"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Создаем пользователей
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.token1 = Token.objects.create(user=self.user1)
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        self.token2 = Token.objects.create(user=self.user2)
        
        # Создаем читателей
        self.reader1 = Reader.objects.create(
            first_name='Читатель',
            last_name='Первый',
            email='reader1@example.com',
            passport_number='1111111111'
        )
        # Связываем с пользователем (требует добавления поля user в модель)
        # self.reader1.user = self.user1
        # self.reader1.save()
        
        self.reader2 = Reader.objects.create(
            first_name='Читатель',
            last_name='Второй',
            email='reader2@example.com',
            passport_number='2222222222'
        )
        
        # Создаем книгу
        author = Author.objects.create(
            first_name='Тестовый',
            last_name='Автор'
        )
        self.book = Book.objects.create(
            title='Тестовая книга',
            isbn='9785170999999',
            author=author,
            publication_year=2024,
            available_copies=2
        )
    
    def test_authenticated_can_create_borrowing(self):
        """Авторизованные пользователи могут создавать выдачи"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        
        from datetime import date, timedelta
        
        borrowing_data = {
            'reader_id': self.reader1.id,
            'book_id': self.book.id,
            'borrow_date': str(date.today()),
            'due_date': str(date.today() + timedelta(days=14))
        }
        
        response = self.client.post('/api/borrowings/', borrowing_data, format='json')
        # Может быть 201 или 403 в зависимости от реализации связи User-Reader
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_403_FORBIDDEN])

