from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, timedelta


class Reader(models.Model):
    """Модель читателя библиотеки"""
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    date_of_birth = models.DateField("Дата рождения", null=True, blank=True)
    address = models.TextField("Адрес", blank=True)
    passport_number = models.CharField("Номер паспорта", max_length=20, unique=True)
    registration_date = models.DateTimeField("Дата регистрации", auto_now_add=True)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"
        ordering = ['-registration_date']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def active_borrowings_count(self):
        return self.borrowings.filter(status='active').count()


class Author(models.Model):
    """Модель автора книги"""
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    biography = models.TextField("Биография", blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    country = models.CharField("Страна", max_length=100, blank=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):
    """Модель издательства"""
    name = models.CharField("Название", max_length=200, unique=True)
    country = models.CharField("Страна", max_length=100)
    city = models.CharField("Город", max_length=100)
    foundation_year = models.PositiveIntegerField("Год основания", null=True, blank=True)
    website = models.URLField("Веб-сайт", blank=True)

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра книги"""
    name = models.CharField("Название", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """Модель книги"""
    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'Английский'),
        ('fr', 'Французский'),
        ('de', 'Немецкий'),
        ('es', 'Испанский'),
        ('other', 'Другой'),
    ]

    title = models.CharField("Название", max_length=200)
    isbn = models.CharField("ISBN", max_length=13, unique=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name="Автор"
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name="Издательство"
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='books',
        verbose_name="Жанры"
    )
    publication_year = models.PositiveIntegerField("Год издания")
    pages = models.PositiveIntegerField("Количество страниц", null=True, blank=True)
    language = models.CharField("Язык", max_length=10, choices=LANGUAGE_CHOICES, default='ru')
    description = models.TextField("Описание", blank=True)
    cover_image = models.ImageField("Обложка", upload_to='book_covers/', blank=True, null=True)
    total_copies = models.PositiveIntegerField("Всего экземпляров", default=1)
    available_copies = models.PositiveIntegerField("Доступно экземпляров", default=1)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.author.last_name})"

    @property
    def is_available(self):
        return self.available_copies > 0

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None


class Borrowing(models.Model):
    """Модель выдачи книги"""
    STATUS_CHOICES = [
        ('active', 'Активна'),
        ('returned', 'Возвращена'),
        ('overdue', 'Просрочена'),
    ]

    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        related_name='borrowings',
        verbose_name="Читатель"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrowings',
        verbose_name="Книга"
    )
    borrow_date = models.DateField("Дата выдачи", default=date.today)
    due_date = models.DateField("Планируемая дата возврата")
    return_date = models.DateField("Фактическая дата возврата", null=True, blank=True)
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default='active')
    fine_amount = models.DecimalField("Сумма штрафа", max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Выдача книги"
        verbose_name_plural = "Выдачи книг"
        ordering = ['-borrow_date']

    def __str__(self):
        return f"{self.reader.full_name} - {self.book.title}"

    def save(self, *args, **kwargs):
        # Устанавливаем due_date на 14 дней вперед, если не указано
        if not self.due_date:
            self.due_date = self.borrow_date + timedelta(days=14)
        
        # Проверяем просрочку
        if self.status == 'active' and date.today() > self.due_date:
            self.status = 'overdue'
        
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        return self.status == 'overdue' or (self.status == 'active' and date.today() > self.due_date)

    @property
    def days_overdue(self):
        if self.is_overdue:
            return (date.today() - self.due_date).days
        return 0


class Review(models.Model):
    """Модель отзыва на книгу"""
    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Читатель"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Книга"
    )
    rating = models.PositiveSmallIntegerField(
        "Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
        unique_together = ['reader', 'book']

    def __str__(self):
        return f"{self.reader.full_name} - {self.book.title} ({self.rating}/5)"

