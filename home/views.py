from django.shortcuts import render
from books.models import Book, Category


# Create your views here.
def index(request):
    featured_books = Book.objects.all()[:3]

    context = {
        'featured_books': featured_books,
        'categories': Category.objects.all(),
    }
    return render(request, 'home/index.html', context)
