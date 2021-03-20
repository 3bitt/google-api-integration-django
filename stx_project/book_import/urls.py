from .views import FetchBooksFromAPI, SaveBooksInDB
from django.urls import path

app_name = 'book_import'
urlpatterns = [
    path('', FetchBooksFromAPI.as_view(), name='import'),
    path('success/', FetchBooksFromAPI.as_view(success_import=True), name='import-success'),
    path('save/<path:resource>/', SaveBooksInDB.as_view(), name='save-resource'),
    # path('save/', SaveBooksInDB.as_view(), name='save-resource')
]
