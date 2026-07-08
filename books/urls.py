"""URLs for books app."""
from django.urls import path

from .views import add_book, book_detail, book_list, edit_book, delete_book, \
    add_review, edit_review, delete_review, manage_books

urlpatterns = [
    path('', book_list, name='books'),

    path('manage/', manage_books, name='manage_books'),
    path('add/', add_book, name='add_book'),
    path('edit/<int:book_id>/', edit_book, name='edit_book'),
    path('delete/<int:book_id>/', delete_book, name='delete_book'),
    path('<int:book_id>/', book_detail, name='book_detail'),
    path('<int:book_id>/add_review/', add_review, name='add_review'),
    path("review/<int:review_id>/edit/", edit_review, name="edit_review"),
    path("review/<int:review_id>/delete/", delete_review,
         name="delete_review"),

]
