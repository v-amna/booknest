from django.contrib import messages
from .forms import ReviewForm
from .models import Review
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from books.models import Book, Category


def book_list(request):
    books = Book.objects.all().order_by('title')
    categories = Category.objects.all()
    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )
    if category:
        books = books.filter(category__name=category)

    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    books_page = paginator.get_page(page_number)

    return render(request, 'books/book_list.html',
                  {'books': books_page, 'categories': categories})


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


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(
        Review,
        pk=review_id
    )

    if review.user != request.user:
        messages.error(
            request,
            "You can only edit your own reviews."
        )

        return redirect(
            "book_detail",
            book_id=review.book.id
        )

    if request.method == "POST":

        form = ReviewForm(
            request.POST,
            instance=review
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Review updated successfully."
            )

            return redirect(
                "book_detail",
                book_id=review.book.id
            )

    else:

        form = ReviewForm(
            instance=review
        )

    context = {
        "form": form,
        "book": review.book,
    }

    return render(
        request,
        "books/edit_review.html",
        context
    )


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(
        Review,
        pk=review_id
    )

    if review.user != request.user:
        messages.error(
            request,
            "You can only delete your own reviews."
        )

        return redirect(
            "book_detail",
            book_id=review.book.id
        )

    review.delete()

    messages.success(
        request,
        "Review deleted successfully."
    )

    return redirect(
        "book_detail",
        book_id=review.book.id
    )
