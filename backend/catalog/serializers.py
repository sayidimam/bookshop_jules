from rest_framework import serializers
from .models import Book, Author, Publisher, Category

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'slug', 'image']

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'authors', 'publisher',
            'regular_price', 'sale_price', 'cover_image', 'is_featured'
        ]

class BookDetailSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    publisher = PublisherSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    related_books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'description', 'authors', 'publisher',
            'categories', 'isbn', 'edition', 'language', 'page_count',
            'regular_price', 'sale_price', 'stock', 'cover_image',
            'related_books', 'is_bundle'
        ]
