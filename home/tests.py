"""Tests for home page."""

import pytest
from decimal import Decimal
from datetime import date
from django.test import Client
from django.urls import reverse
from books.models import Book, Category


@pytest.mark.django_db
class TestIndexView:
    """Home index view tess."""

    @pytest.fixture
    def books(self):
        """Fixture for books view."""
        category = Category.objects.create(name="Fiction")
        books = []
        for i in range(5):
            book = Book.objects.create(
                category=category,
                title=f"Book {i}",
                author="Author",
                publisher="Publisher",
                pages=200,
                language="English",
                price=Decimal("10.00"),
                cover="hardcover",
                paper="white",
                isbn=f"978-3-16-14841{i:04d}",
                publication_date=date(2020, 1, 1),
            )
            books.append(book)
        return books

    def test_index_view_empty(self):
        """Test home page view with no books."""
        client = Client()
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert 'featured_books' in response.context
        assert 'categories' in response.context

    def test_index_view_with_books(self, books):
        """Test home page with books view."""
        client = Client()
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert len(response.context['featured_books']) <= 3

    def test_index_view_categories(self, books):
        """Test home page categories view."""
        client = Client()
        response = client.get(reverse('home'))
        assert len(response.context['categories']) > 0

    def test_index_view_featured_books_limit(self, books):
        """Test featured books pages limit."""
        client = Client()
        response = client.get(reverse('home'))
        featured = response.context['featured_books']
        assert len(featured) <= 3
