"""Home app views."""

from django.http import HttpResponse
from django.shortcuts import render
from books.models import Book, Category
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from booknest import settings


def index(request):
    """Home index view."""
    featured_books = Book.objects.all()[:3]

    context = {
        'featured_books': featured_books,
        'categories': Category.objects.all(),
    }
    return render(request, 'home/index.html', context)


def robots_txt(request):
    """robots.txt view."""
    domain = Site.objects.get_current().domain
    content = render_to_string("robots.txt", {
        "debug": settings.DEBUG,
        "domain": domain,
    })
    return HttpResponse(content, content_type="text/plain")
