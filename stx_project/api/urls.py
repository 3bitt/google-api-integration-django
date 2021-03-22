from django.urls import include, path
from rest_framework import routers
from .views import BookViewSet


app_name = 'api'
# router = routers.SimpleRouter()
# router.register('books', BookViewSet, basename='books')

urlpatterns = [
    path('', BookViewSet.as_view({'get':'list'}), name='books')
]

