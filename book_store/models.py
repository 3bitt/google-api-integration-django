from django.db import models
from django.db.models.deletion import CASCADE


class Author(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    surname = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Book(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    published_date = models.DateField()
    page_count = models.IntegerField(null=False, blank=False)
    thumbnail_url = models.URLField(max_length=255)
    language = models.CharField(max_length=2)
    author = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        return f'{self.title}'


class Isbn(models.Model):
    type = models.CharField(max_length=7)
    number = models.CharField(max_length=30)
    book = models.ForeignKey(Book, on_delete=CASCADE)

    def __str__(self):
        return f'{self.number}'