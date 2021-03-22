from django.urls import path, include


urlpatterns = [
    path('', include('book_store.urls', namespace='book')),
    path('import/', include('book_import.urls', namespace='import')),
    path('api/', include('api.urls', namespace='api')),
]
