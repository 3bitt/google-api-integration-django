from django.db import models
from rest_framework import serializers


class IsbnInterface(serializers.Serializer):
    type = serializers.CharField(max_length=7, allow_blank=True)
    identifier = serializers.CharField(max_length=30, allow_blank=True)

class AuthorInterface(serializers.Serializer):
    full_name = serializers.CharField(max_length=255, allow_blank=True)

class ImageLinkInterface(serializers.Serializer):
    smallThumbnail = serializers.CharField(max_length=255, allow_blank=True)
    thumbnail = serializers.CharField(max_length=255, allow_blank=True)

class BookInterface(serializers.Serializer):
    title = serializers.CharField(max_length=255, allow_blank=True)
    publishedDate = serializers.CharField(max_length=10, allow_blank=True)
    page_count = serializers.IntegerField()
    imageLinks = ImageLinkInterface()
    language = serializers.CharField(max_length=2, allow_blank=True)
    authors = AuthorInterface(many=True)
    industryIdentifiers = IsbnInterface(many=True)

class BookVolumeInfoInterface(serializers.Serializer):
    volumeInfo = BookInterface()

class BookParentInterface(serializers.Serializer):
    items = BookVolumeInfoInterface(many=True)