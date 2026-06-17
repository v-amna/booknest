from django.urls import path
from .views import book_detail, book_list

urlpatterns = [
    path('', book_list, name='books'),
     path('<int:book_id>/', book_detail, name='book_detail'),
]