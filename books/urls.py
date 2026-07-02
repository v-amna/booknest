from django.urls import path

from .views import add_book, book_detail, book_list, edit_book,delete_book,add_review


urlpatterns = [
    path('', book_list, name='books'),
    
    path('add/', add_book, name='add_book'),
    path('edit/<int:book_id>/',edit_book,name='edit_book'),
    path('delete/<int:book_id>/',delete_book,name='delete_book'),
    path('<int:book_id>/', book_detail, name='book_detail'),
    path('<int:book_id>/add_review/', add_review, name='add_review'),
    

]