from .views import BookListView, BookSearchView
from django.urls import path, include

app_name = 'book_store'
urlpatterns = [
    path('list/', BookListView.as_view(), name='book-list' ),
    path('list/search/', BookSearchView.as_view(), name='book-search')

]
