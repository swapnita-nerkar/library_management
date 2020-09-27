# api/serializers.py
from rest_framework import serializers
from management.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'isbn', 'department', 'language', 'total_copies', 'available_copies')
