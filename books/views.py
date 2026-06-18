from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from books.models import Book,Category



# Create your views here.
def book_list(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('q')
    category=request.GET.get('category')

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )
    if category:
        books = books.filter(category__name=category    )
    
    return render(request, 'books/book_list.html', {'books': books, 'categories': categories})

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})