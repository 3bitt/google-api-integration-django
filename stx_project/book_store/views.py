from django.http.request import QueryDict
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from requests.api import request
from .models import Book, Author

# Create your views here.


class BookListView(ListView):
    template_name = 'book_store/book_store_list.html'
    queryset = Book.objects.all().order_by('-id')[:10]
    context_object_name = 'book_list'


class BookSearchView(ListView):
    template_name = 'book_store/book_store_list.html'
    context_object_name = 'book_list'

    def get_queryset(self):

        query_params = self.request.GET

        q_is_year = Q(publish_date_type=Book.PARTIAL_YEAR)
        q_by_year = Q(publish_date__year=2015)

        q_is_month = Q(publish_date_type=Book.PARTIAL_MONTH)
        q_by_month = Q(publish_date__year=2105)
        q_by_month &= Q(publish_date__month=2)

        
        params = {k: query_params[k] for k in query_params if query_params[k]}
        
        filter = Q(title__contains=query_params['title'])
        
        if 'author' in params:
            filter.add(Q(author__full_name__contains=query_params['author']), Q.AND)
        if 'language' in params:
            filter.add(Q(language__contains=query_params['language']), Q.AND)
        if 'publish_date_gte' in params:
            filter.add(Q(publish_date__gte=params['publish_date_gte']), Q.AND)
        if 'publish_date_lte' in params:
            filter.add(Q(publish_date__lte=params['publish_date_lte']), Q.AND)
        
        q = Book.objects.filter(filter).order_by('-id')

        print(filter)

        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = {k: self.request.GET[k] for k in self.request.GET if self.request.GET[k]}
        for k, v in params.items():
            context[k] = v
        return context
