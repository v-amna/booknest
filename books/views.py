
from django.contrib import messages
from .forms import ReviewForm
from .models import Review
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from django.shortcuts import get_object_or_404, render, redirect
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


@login_required
def add_book(request):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Sorry, only store administrators can do that."
        )

        return redirect("books")

    if request.method == "POST":

        form = BookForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Book added successfully."
            )

            return redirect("books")

    else:

        form = BookForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "books/add_book.html",
        context
    )

@login_required
def edit_book(request, book_id):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Sorry, only store administrators can do that."
        )

        return redirect("books")

    book = get_object_or_404(
        Book,
        pk=book_id
    )

    if request.method == "POST":

        form = BookForm(
            request.POST,
            request.FILES,
            instance=book
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Book updated successfully."
            )

            return redirect(
                "book_detail",
                book.id
            )

    else:

        form = BookForm(
            instance=book
        )

    context = {
        "form": form,
        "book": book,
    }

    return render(
        request,
        "books/edit_book.html",
        context
    )

@login_required
def delete_book(request, book_id):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Sorry, only store administrators can do that."
        )

        return redirect("books")

    book = get_object_or_404(
        Book,
        pk=book_id
    )

    book.delete()

    messages.success(
        request,
        "Book deleted successfully."
    )

    return redirect("books")

@login_required
def add_review(request, book_id):

    book = get_object_or_404(
        Book,
        pk=book_id
    )

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.user = request.user
            review.book = book

            review.save()

            messages.success(
                request,
                "Review added successfully."
            )

            return redirect(
                "book_detail",
                book_id=book.id
            )

    else:

        form = ReviewForm()

    context = {
        "book": book,
        "form": form,
    }

    return render(
        request,
        "books/add_review.html",
        context
    )