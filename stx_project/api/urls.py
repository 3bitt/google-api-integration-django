from django.urls import path
from .views import BookViewSet


app_name = 'api'
urlpatterns = [
    path('', BookViewSet.as_view({'get':'list'}), name='books')
]
