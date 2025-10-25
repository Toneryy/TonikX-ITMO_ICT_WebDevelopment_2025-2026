from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
import sys
import os

# Добавляем путь к модулям из task_1
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'task_1'))

from library.models import Reader, Author, Publisher, Genre, Book, Borrowing, Review
from datetime import date, timedelta


class ReaderAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.reader_data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'ivan@example.com',
            'passport_number': '1234567890'
        }
    
    def test_create_reader(self):
        """Тест создания читателя через API"""
        response = self.client.post('/api/readers/', self.reader_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reader.objects.count(), 1)
        self.assertEqual(Reader.objects.get().email, 'ivan@example.com')
    
    def test_list_readers(self):
        """Тест получения списка читателей"""
        Reader.objects.create(**self.reader_data)
        response = self.client.get('/api/readers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class BookAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(
            first_name='Лев',
            last_name='Толстой'
        )
        self.genre = Genre.objects.create(name='Роман')
        
        self.book_data = {
            'title': 'Война и мир',
            'isbn': '9785170123456',
            'author_id': self.author.id,
            'genre_ids': [self.genre.id],
            'publication_year': 1869,
            'language': 'ru',
            'total_copies': 3,
            'available_copies': 3
        }
    
    def test_create_book(self):
        """Тест создания книги через API"""
        response = self.client.post('/api/books/', self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
    
    def test_list_books(self):
        """Тест получения списка книг"""
        Book.objects.create(
            title='Война и мир',
            isbn='9785170123456',
            author=self.author,
            publication_year=1869
        )
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_available_books(self):
        """Тест получения доступных книг"""
        Book.objects.create(
            title='Война и мир',
            isbn='9785170123456',
            author=self.author,
            publication_year=1869,
            available_copies=2
        )
        response = self.client.get('/api/books/available/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class BorrowingAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.reader = Reader.objects.create(
            first_name='Петр',
            last_name='Петров',
            email='petr@example.com',
            passport_number='0987654321'
        )
        
        self.author = Author.objects.create(
            first_name='Александр',
            last_name='Пушкин'
        )
        
        self.book = Book.objects.create(
            title='Евгений Онегин',
            isbn='9785170123457',
            author=self.author,
            publication_year=1833,
            total_copies=2,
            available_copies=2
        )
        
        self.borrowing_data = {
            'reader_id': self.reader.id,
            'book_id': self.book.id,
            'borrow_date': str(date.today()),
            'due_date': str(date.today() + timedelta(days=14))
        }
    
    def test_create_borrowing(self):
        """Тест создания выдачи книги"""
        response = self.client.post('/api/borrowings/', self.borrowing_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Проверяем, что количество доступных книг уменьшилось
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 1)
    
    def test_return_book(self):
        """Тест возврата книги"""
        borrowing = Borrowing.objects.create(
            reader=self.reader,
            book=self.book,
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14)
        )
        
        # Уменьшаем доступные копии
        self.book.available_copies = 1
        self.book.save()
        
        response = self.client.post(f'/api/borrowings/{borrowing.id}/return_book/', {
            'return_date': str(date.today())
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Проверяем, что количество доступных книг увеличилось
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 2)
        
        # Проверяем статус выдачи
        borrowing.refresh_from_db()
        self.assertEqual(borrowing.status, 'returned')

