from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta
from .models import Reader, Author, Publisher, Genre, Book, Borrowing, Review


class ReaderModelTest(TestCase):
    def setUp(self):
        self.reader = Reader.objects.create(
            first_name="Иван",
            last_name="Иванов",
            email="ivan@example.com",
            passport_number="1234567890"
        )

    def test_reader_creation(self):
        self.assertEqual(self.reader.full_name, "Иван Иванов")
        self.assertTrue(self.reader.is_active)

    def test_reader_str(self):
        self.assertEqual(str(self.reader), "Иван Иванов")


class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="Лев",
            last_name="Толстой"
        )
        self.book = Book.objects.create(
            title="Война и мир",
            isbn="9785170123456",
            author=self.author,
            publication_year=1869,
            total_copies=3,
            available_copies=3
        )

    def test_book_creation(self):
        self.assertTrue(self.book.is_available)
        self.assertEqual(self.book.available_copies, 3)

    def test_book_str(self):
        self.assertEqual(str(self.book), "Война и мир (Толстой)")


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.reader = Reader.objects.create(
            first_name="Петр",
            last_name="Петров",
            email="petr@example.com",
            passport_number="0987654321"
        )
        self.author = Author.objects.create(
            first_name="Александр",
            last_name="Пушкин"
        )
        self.book = Book.objects.create(
            title="Евгений Онегин",
            isbn="9785170123457",
            author=self.author,
            publication_year=1833,
            total_copies=2,
            available_copies=2
        )

    def test_borrowing_creation(self):
        borrowing = Borrowing.objects.create(
            reader=self.reader,
            book=self.book,
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14)
        )
        self.assertEqual(borrowing.status, 'active')
        self.assertFalse(borrowing.is_overdue)

    def test_overdue_borrowing(self):
        past_date = date.today() - timedelta(days=20)
        borrowing = Borrowing.objects.create(
            reader=self.reader,
            book=self.book,
            borrow_date=past_date,
            due_date=past_date + timedelta(days=14)
        )
        borrowing.save()  # Это должно обновить статус на 'overdue'
        self.assertTrue(borrowing.is_overdue)

