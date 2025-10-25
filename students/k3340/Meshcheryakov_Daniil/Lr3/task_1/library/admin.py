from django.contrib import admin
from .models import Reader, Author, Publisher, Genre, Book, Borrowing, Review


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'passport_number', 'registration_date', 'is_active']
    list_filter = ['is_active', 'registration_date']
    search_fields = ['first_name', 'last_name', 'email', 'passport_number']
    readonly_fields = ['registration_date']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Дополнительная информация', {
            'fields': ('date_of_birth', 'address', 'passport_number')
        }),
        ('Статус', {
            'fields': ('is_active', 'registration_date')
        }),
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'country', 'birth_date']
    list_filter = ['country']
    search_fields = ['first_name', 'last_name', 'country']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'city', 'foundation_year', 'website']
    list_filter = ['country', 'city']
    search_fields = ['name', 'country', 'city']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'publication_year', 'language', 'available_copies', 'total_copies']
    list_filter = ['language', 'publication_year', 'genres', 'author']
    search_fields = ['title', 'isbn', 'author__first_name', 'author__last_name']
    filter_horizontal = ['genres']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'isbn', 'author', 'publisher')
        }),
        ('Издание', {
            'fields': ('publication_year', 'pages', 'language', 'genres')
        }),
        ('Описание', {
            'fields': ('description', 'cover_image')
        }),
        ('Наличие', {
            'fields': ('total_copies', 'available_copies')
        }),
    )


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ['reader', 'book', 'borrow_date', 'due_date', 'return_date', 'status', 'fine_amount']
    list_filter = ['status', 'borrow_date', 'due_date']
    search_fields = ['reader__first_name', 'reader__last_name', 'book__title']
    date_hierarchy = 'borrow_date'
    
    fieldsets = (
        ('Выдача', {
            'fields': ('reader', 'book', 'borrow_date', 'due_date')
        }),
        ('Возврат', {
            'fields': ('return_date', 'status', 'fine_amount')
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reader', 'book', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['reader__first_name', 'reader__last_name', 'book__title', 'comment']
    readonly_fields = ['created_at', 'updated_at']

