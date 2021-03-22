from .views import BookCreateView, BookListView, BookSearchView, \
    BookDetailView, BookUpdateView, BookDeleteView
from django.urls import path


app_name = 'book_store'
urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('search/', BookSearchView.as_view(), name='book-search'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:pk>/detail/', BookDetailView.as_view(), name='book-detail'),
    path('<int:pk>/detail/update',BookUpdateView.as_view(), name='book-update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
