from django.db.models import Q
from django_filters import rest_framework as filters
import django_filters
from django_filters.filters import DateFromToRangeFilter
from django_filters.filterset import FilterSet
from rest_framework import mixins, views, viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework.generics import ListAPIView
from .serializers import BookSerializer
from dateutil import parser as date_parser
from book_store.models import Book, Author


class BookViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        query = self.request.query_params
        if query:
            filter = Q()
            for key, value in query.items():
                if value and key == 'title':
                    filter.add(Q(title__contains=value), Q.AND)
                if value and key == 'authors':
                    filter.add(Q(author__full_name__contains=value), Q.AND)
                if value and key == 'language':
                    filter.add(Q(language__contains=value), Q.AND)
                if value and key == 'publishDateFrom':
                    try:
                        value_parsed = date_parser.isoparse(value)
                        filter.add(Q(publish_date__gte=value_parsed), Q.AND)
                    except ValueError:
                        pass
                if value and key == 'publishDateTo':
                    try:
                        value_parsed = date_parser.isoparse(value)
                        filter.add(Q(publish_date__lte=value_parsed), Q.AND)
                    except ValueError:
                        pass

            queryset = queryset.filter(filter)
        return queryset

    def get_renderer_context(self):
        context = super().get_renderer_context()
        context['indent'] = 2
        return context
