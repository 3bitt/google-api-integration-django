from django.db.models import fields
from django.utils.regex_helper import flatten_result
from rest_framework.fields import ModelField, SerializerMethodField
from rest_framework.routers import flatten
from book_store.models import Book, Author, Isbn
from rest_framework import serializers
from datetime import date


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']


class IsbnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Isbn
        fields = ['type', 'number']


class BookSerializer(serializers.ModelSerializer):
    identifiers = IsbnSerializer(many=True, source='isbn_set')
    authors = SerializerMethodField()
    publishDate = SerializerMethodField()
    thumbnailUrl = SerializerMethodField()

    class Meta:
        model = Book
        fields = ['title', 'authors', 'publishDate', 'identifiers',
                  'page_count', 'language', 'thumbnailUrl']

    def get_authors(self, obj):
        authors = Author.objects.filter(id__in=obj.author.all().values(
            'id')).values_list('full_name', flat=True)
        return authors

    def get_publishDate(self, obj):
        if obj.publish_date:
            return obj.publish_date.strftime(obj.publish_date_type)
    
    def get_thumbnailUrl(self, obj):
        if obj.thumbnail_url:
            return obj.thumbnail_url
