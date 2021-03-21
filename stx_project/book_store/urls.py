from .views import BookCreateView, BookListView, BookSearchView,BookDetailView,BookUpdateView,BookDeleteView
from django.urls import path, include

app_name = 'book_store'
urlpatterns = [
    path('list/', BookListView.as_view(), name='book-list' ),
    path('list/search/', BookSearchView.as_view(), name='book-search'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:pk>/detail/', BookDetailView.as_view(), name='book-detail'),
    path('<int:id>/detail/update', BookUpdateView.as_view(edit_mode=True), name='book-detail-update'),
    path('<int:id>/delete/', BookDeleteView.as_view(), name='book-delete'),

]
id