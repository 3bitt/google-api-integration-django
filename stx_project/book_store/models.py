from django.db import models
from django.db.models.deletion import CASCADE


class Author(models.Model):
    full_name = models.CharField(max_length=255,
                            null=False,
                            blank=False
                            )


    def __str__(self):
        return f'{self.full_name}'


class Book(models.Model):
    PARTIAL_YEAR='%Y'
    PARTIAL_MONTH='%Y-%m'
    PARTIAL_DAY='%Y-%m-%d'
    PARTIAL_CHOICES = (
      (PARTIAL_YEAR, 'Year'),
      (PARTIAL_MONTH, 'Month'),
      (PARTIAL_DAY, 'Day'),
    )

    title = models.CharField(max_length=255, null=False, blank=False)
    publish_date = models.DateField(null=True, blank=True)
    publish_date_type = models.CharField('Date type', choices=PARTIAL_CHOICES, max_length=10, null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)
    thumbnail_url = models.URLField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=2)
    author = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        return f'{self.title}' 

    def get_ui_date_type(self):
        return str(self.publish_date_type).replace('%', '')        


class Isbn(models.Model):
    type = models.CharField(max_length=7)
    number = models.CharField(max_length=30)
    book = models.ForeignKey(Book, on_delete=CASCADE)

    def __str__(self):
        return f'{self.number}'