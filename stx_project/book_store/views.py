from datetime import date
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from .forms import BookCreateForm, DateSelectorWidget
from django.http.request import QueryDict
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, DetailView, DeleteView
from django.db.models import Q
from requests.api import request
from .models import Book, Author, Isbn
from django.forms.models import modelform_factory
from dateutil import parser as date_parser

# Create your views here.


class BookListView(ListView):
    template_name = 'book_store/book_store_list.html'
    queryset = Book.objects.all().order_by('-created_date')[:20]
    context_object_name = 'book_list'


class BookSearchView(ListView):
    template_name = 'book_store/book_store_list.html'
    context_object_name = 'book_list'

    def get_queryset(self):

        query_params = self.request.GET
        filter = Q()
        for key, value in query_params.items():
            if value and key == 'title':
                filter.add(Q(title__contains=value), Q.AND)
            if value and key == 'author':
                filter.add(Q(author__full_name__contains=value), Q.AND)
            if value and key == 'language':
                filter.add(Q(language__contains=value), Q.AND)
            if value and key == 'publish_date_gte':
                filter.add(Q(publish_date__gte=value), Q.AND)
            if value and key == 'publish_date_lte':
                filter.add(Q(publish_date__lte=value), Q.AND)

        queryset = Book.objects.filter(filter).order_by('-created_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for key, value in self.request.GET.items():
            if value:
                context[key] = value
        return context


class BookCreateView(CreateView):
    template_name = 'book_store/book_store_create.html'
    model = Book
    form_class = BookCreateForm
    success_url = reverse_lazy('book:book-list')

    def form_valid(self, form: BookCreateForm):

        params = self.request.POST

        year = int(params['publish_date_0'])
        month = int(params['publish_date_1'])
        day = int(params['publish_date_2'])

        new_book = Book.objects.create(
            title=params['title'].strip(),
            publish_date=date(year=year, month=month, day=day),
            publish_date_type=params['date_type'],
            page_count=params['page_count'],
            thumbnail_url=params['thumbnail_url'],
            language=params['language']
        )

        authors = [author.strip()
                   for author in params['authors'].split(',') if author.strip()]
        for author in authors:
            a = Author.objects.create(full_name=author)
            new_book.author.add(a)

        ident_types = params.getlist('identifier_type')
        idents = params.getlist('identifier')
        identifiers = [item for item in zip(
            ident_types, idents) if item[0] and item[1]]

        for identifier in identifiers:
            Isbn.objects.create(
                type=identifier[0],
                number=identifier[1],
                book=new_book
            )

        return redirect('book:book-list')


class BookDetailView(DetailView):
    template_name = 'book_store/book_store_detail.html'
    model = Book
    context_object_name = 'book'


class BookUpdateView(UpdateView):
    template_name = 'book_store/book_store_update.html'
    model = Book
    form_class = BookCreateForm
    context_object_name = 'book'

    def form_valid(self, form: BookCreateForm):

        params = self.request.POST

        year = int(params['publish_date_0'])
        month = int(params['publish_date_1'])
        day = int(params['publish_date_2'])

        Book.objects.filter(id=self.object.id).update(
            title=params['title'].strip(),
            publish_date=date(year=year, month=month, day=day),
            publish_date_type=params['date_type'],
            page_count=params['page_count'],
            thumbnail_url=params['thumbnail_url'],
            language=params['language']
        )
        authors = [author.strip()
                   for author in params['authors'].split(',') if author.strip()]

        authors_of_book = Author.objects.filter(books=self.object)
        if authors_of_book:
            authors_of_book.delete()

        for author in authors:
            new_author = Author.objects.create(full_name=author)
            self.object.author.add(new_author)

        ident_types = params.getlist('identifier_type')
        idents = params.getlist('identifier')
        identifiers = [item for item in zip(
            ident_types, idents) if item[0] and item[1]]

        book_identifiers = Isbn.objects.filter(book=self.object)

        if book_identifiers:
            book_identifiers.delete()

        for identifier in identifiers:
            new_ident = Isbn.objects.create(
                type=identifier[0],
                number=identifier[1],
                book=self.object
            )

        return redirect('book:book-detail', self.kwargs['pk'])


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('book:book-list')
