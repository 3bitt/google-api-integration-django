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
        params = {k: query_params[k] for k in query_params if query_params[k]}
        filter = Q(title__contains=query_params['title'])

        if 'author' in params:
            filter.add(
                Q(author__full_name__contains=query_params['author']), Q.AND)
        if 'language' in params:
            filter.add(Q(language__contains=query_params['language']), Q.AND)
        if 'publish_date_gte' in params:
            filter.add(Q(publish_date__gte=params['publish_date_gte']), Q.AND)
        if 'publish_date_lte' in params:
            filter.add(Q(publish_date__lte=params['publish_date_lte']), Q.AND)

        q = Book.objects.filter(filter).order_by('-created_date')

        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = {k: self.request.GET[k]
                  for k in self.request.GET if self.request.GET[k]}
        for k, v in params.items():
            context[k] = v
        return context


class BookCreateView(CreateView):
    template_name = 'book_store/book_store_create.html'
    model = Book
    form_class = BookCreateForm
    success_url = reverse_lazy('book:book-list')

    def form_valid(self, form: BookCreateForm):

        params = self.request.POST
        print(params)

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
    edit_mode = False

class BookUpdateView(UpdateView):
    template_name = 'book_store/book_store_detail_update.html'
    model = Book    
    context_object_name = 'book'
    edit_mode = True

    def get_success_url(self):
        return reverse_lazy('book:book-detail', kwargs={'id': self.kwargs['pk']})

class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('book:book-list')

