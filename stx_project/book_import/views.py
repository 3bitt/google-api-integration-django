import requests
import json
from types import MappingProxyType
from django.http.request import QueryDict
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin, View
from dateutil import parser as date_parser
from .helpers import get_date_format
from book_store.models import Book, Author, Isbn


class FetchBooksFromAPI(TemplateView):

    http_method_names = ['get', 'post']
    template_name = 'book_import/fetch_books.html'

    API_URL = 'https://www.googleapis.com/books/v1/volumes?q='
    FILTERS = [
        'intext',
        'intitle',
        'inauthor',
        'inpublisher',
        'subject',
        'isbn',
        'lccn',
        'oclc',
    ]
    success_import = False

    def post(self, request):

        request_dict = QueryDict.copy(request.POST)
        del request_dict['csrfmiddlewaretoken']

        api_query = request_dict['intext'].strip()

        for key, val in request_dict.dict().items():

            if (key in self.FILTERS and key != 'intext' and val.strip()):

                api_query += f'+{key}:{val}'

        api_response = requests.get(self.API_URL + api_query)
        books_data = json.loads(api_response.content)

        return render(request, 'book_import/fetch_books.html',
                      context={
                          'data': books_data,
                          'user_input': request_dict,
                          'api_resource': api_query,
                          'success_import': self.success_import})


class SaveBooksInDB(View, ContextMixin):
    API_URL = 'https://www.googleapis.com/books/v1/volumes?q='
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        api_resource = self.kwargs['resource']

        api_data = requests.get(self.API_URL + api_resource).content
        mapped_data = json.loads(
            api_data, object_hook=lambda d: MappingProxyType(d))

        existing_isbns = Isbn.objects.values_list('number', flat=True)
        existing_book_titles = Book.objects.values_list('title', flat=True)
        authors_created = []

        for book in mapped_data['items']:
            book = book['volumeInfo']

            if 'industryIdentifiers' in book:
                for isbn in book['industryIdentifiers']:
                    if isbn['identifier'] in existing_isbns:
                        break

            if book['title'] in existing_book_titles:
                break

            if 'authors' in book:
                for author_name in book['authors']:
                    new_author = Author.objects.create(
                        full_name=author_name
                    )
                    authors_created.append(new_author)

            new_book = Book(
                title=book.get('title'),
            )

            if 'pageCount' in book:
                new_book.page_count = book.get('pageCount')
            if 'language' in book:
                new_book.language = book.get('language')
            if 'publishedDate' in book:
                date_parser.parserinfo(yearfirst=True)

                new_book.publish_date = date_parser.isoparse(
                    book.get('publishedDate'))

                new_book.publish_date_type = get_date_format(
                    book.get('publishedDate'))

            if 'imageLinks' in book:
                new_book.thumbnail_url = book.get(
                    'imageLinks').get('thumbnail')

            new_book.save()

            if authors_created:
                new_book.author.set(objs=authors_created)

            if 'industryIdentifiers' in book:
                for isbn in book['industryIdentifiers']:
                    new_isbn = Isbn(
                        type=isbn['type'],
                        number=isbn['identifier'],
                        book=new_book
                    )
                    new_isbn.save()

            authors_created.clear()

        return redirect('import:import-success')
