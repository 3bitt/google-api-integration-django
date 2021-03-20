from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('book_store.urls', namespace='book')),
    path('import/', include('book_import.urls', namespace='import'))
]
