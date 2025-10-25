from rest_framework import serializers
from .models import Reader, Author, Publisher, Genre, Book, Borrowing, Review


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Author"""
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'full_name', 'biography', 'birth_date', 'country']


class PublisherSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Publisher"""
    
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'country', 'city', 'foundation_year', 'website']


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""
    
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']


class ReaderSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Reader"""
    full_name = serializers.ReadOnlyField()
    active_borrowings_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Reader
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
            'date_of_birth', 'address', 'passport_number', 'registration_date',
            'is_active', 'active_borrowings_count'
        ]
        read_only_fields = ['registration_date']


class BookListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка книг"""
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    publisher_name = serializers.CharField(source='publisher.name', read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'author', 'author_name', 'publisher',
            'publisher_name', 'genres', 'publication_year', 'language',
            'available_copies', 'total_copies', 'is_available'
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для книги"""
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    publisher = PublisherSerializer(read_only=True)
    publisher_id = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.all(),
        source='publisher',
        write_only=True,
        required=False,
        allow_null=True
    )
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        source='genres',
        write_only=True
    )
    is_available = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'author', 'author_id', 'publisher',
            'publisher_id', 'genres', 'genre_ids', 'publication_year',
            'pages', 'language', 'description', 'cover_image',
            'total_copies', 'available_copies', 'is_available', 'average_rating'
        ]


class BorrowingListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка выдач"""
    reader_name = serializers.CharField(source='reader.full_name', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    is_overdue = serializers.ReadOnlyField()
    days_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Borrowing
        fields = [
            'id', 'reader', 'reader_name', 'book', 'book_title',
            'borrow_date', 'due_date', 'return_date', 'status',
            'fine_amount', 'is_overdue', 'days_overdue'
        ]


class BorrowingDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для выдачи"""
    reader = ReaderSerializer(read_only=True)
    reader_id = serializers.PrimaryKeyRelatedField(
        queryset=Reader.objects.all(),
        source='reader',
        write_only=True
    )
    book = BookListSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source='book',
        write_only=True
    )
    is_overdue = serializers.ReadOnlyField()
    days_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Borrowing
        fields = [
            'id', 'reader', 'reader_id', 'book', 'book_id',
            'borrow_date', 'due_date', 'return_date', 'status',
            'fine_amount', 'is_overdue', 'days_overdue'
        ]
    
    def validate(self, data):
        """Проверка данных при создании выдачи"""
        book = data.get('book')
        
        # Проверяем доступность книги
        if book and book.available_copies <= 0:
            raise serializers.ValidationError({
                'book': 'Эта книга в данный момент недоступна'
            })
        
        return data
    
    def create(self, validated_data):
        """Создание выдачи с уменьшением количества доступных книг"""
        borrowing = super().create(validated_data)
        
        # Уменьшаем количество доступных копий
        book = borrowing.book
        book.available_copies -= 1
        book.save()
        
        return borrowing


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов"""
    reader_name = serializers.CharField(source='reader.full_name', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'reader', 'reader_name', 'book', 'book_title',
            'rating', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_rating(self, value):
        """Проверка оценки"""
        if value < 1 or value > 5:
            raise serializers.ValidationError('Оценка должна быть от 1 до 5')
        return value

