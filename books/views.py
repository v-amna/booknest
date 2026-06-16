from django.shortcuts import get_object_or_404, render


# Create your views here.
def book_list(request):
   
    return render(request, 'books/book_list.html')

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})