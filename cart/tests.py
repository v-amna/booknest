"""Tests for Cart app."""

import pytest
from decimal import Decimal
from datetime import date
from django.test import Client
from django.urls import reverse
from books.models import Book, Category


@pytest.mark.django_db
class TestViewCartView:
    """Test for cart views."""

    @pytest.fixture
    def category(self):
        """Category fixture."""
        return Category.objects.create(name="Fiction")

    @pytest.fixture
    def book(self, category):
        """Book fixture."""
        return Book.objects.create(
            category=category,
            title="Test Book",
            author="Author",
            publisher="Publisher",
            pages=300,
            language="English",
            price=Decimal("19.99"),
            cover="hardcover",
            paper="white",
            isbn="978-3-16-148410-0",
            publication_date=date(2020, 1, 1),
        )

    def test_view_empty_cart(self):
        """Test for empty cart."""
        client = Client()
        response = client.get(reverse('view_cart'))
        assert response.status_code == 200
        assert response.context['cart_items'] == []
        assert response.context['total'] == 0

    def test_view_cart_with_items(self, book):
        """Test cart view with items."""
        client = Client()
        session = client.session
        session['cart'] = {str(book.id): 2}
        session.save()

        response = client.get(reverse('view_cart'))
        assert response.status_code == 200
        assert len(response.context['cart_items']) == 1
        assert response.context['cart_items'][0]['quantity'] == 2
        assert response.context['total'] == Decimal("39.98")


@pytest.mark.django_db
class TestAddToCartView:
    """Test for add to cart view."""

    @pytest.fixture
    def category(self):
        """Category fixture."""
        return Category.objects.create(name="Fiction")

    @pytest.fixture
    def book(self, category):
        """Book fixture."""
        return Book.objects.create(
            category=category,
            title="Test Book",
            author="Author",
            publisher="Publisher",
            pages=300,
            language="English",
            price=Decimal("19.99"),
            cover="hardcover",
            paper="white",
            isbn="978-3-16-148410-0",
            publication_date=date(2020, 1, 1),
        )

    def test_add_to_cart(self, book):
        """Test adding a book to the cart."""
        client = Client()
        response = client.get(reverse('add_to_cart', args=[book.id]), follow=True)
        assert response.status_code == 200
        cart = response.wsgi_request.session.get('cart', {})
        assert str(book.id) in cart
        assert cart[str(book.id)] == 1

    def test_add_to_cart_increment(self, book):
        """Test for adding a book to the cart with quantity increment."""
        client = Client()
        session = client.session
        session['cart'] = {str(book.id): 1}
        session.save()

        response = client.get(reverse('add_to_cart', args=[book.id]), follow=True)
        cart = response.wsgi_request.session.get('cart', {})
        assert cart[str(book.id)] == 2

    def test_add_to_cart_nonexistent_book(self):
        """Test error for non-existing book add."""
        client = Client()
        response = client.get(reverse('add_to_cart', args=[999]))
        assert response.status_code == 404


@pytest.mark.django_db
class TestAddToCartAjaxView:
    """Test for Ajax cart view."""

    @pytest.fixture
    def category(self):
        """Fiction category fixture."""
        return Category.objects.create(name="Fiction")

    @pytest.fixture
    def book(self, category):
        """Book fixture."""
        return Book.objects.create(
            category=category,
            title="Test Book",
            author="Author",
            publisher="Publisher",
            pages=300,
            language="English",
            price=Decimal("19.99"),
            cover="hardcover",
            paper="white",
            isbn="978-3-16-148410-0",
            publication_date=date(2020, 1, 1),
        )

    def test_add_to_cart_ajax(self, book):
        """Test adding a book to the cart via Ajax."""
        client = Client()
        response = client.get(reverse('add_to_cart_ajax', args=[book.id]))
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'message' in data
        assert data['cart_count'] == 1

    def test_add_to_cart_ajax_increment(self, book):
        """Test adding to cart via Ajax with increment."""
        client = Client()
        session = client.session
        session['cart'] = {str(book.id): 2}
        session.save()

        response = client.get(reverse('add_to_cart_ajax', args=[book.id]))
        data = response.json()
        assert data['cart_count'] == 3


@pytest.mark.django_db
class TestUpdateCartView:
    """Test for update cart view."""

    @pytest.fixture
    def category(self):
        """Category fixture."""
        return Category.objects.create(name="Fiction")

    @pytest.fixture
    def book(self, category):
        """Book fixture."""
        return Book.objects.create(
            category=category,
            title="Test Book",
            author="Author",
            publisher="Publisher",
            pages=300,
            language="English",
            price=Decimal("19.99"),
            cover="hardcover",
            paper="white",
            isbn="978-3-16-148410-0",
            publication_date=date(2020, 1, 1),
        )

    def test_update_cart_quantity(self, book):
        """Test updating cart quantity."""
        client = Client()
        session = client.session
        session['cart'] = {str(book.id): 1}
        session.save()

        response = client.post(
            reverse('update_cart', args=[book.id]),
            {'quantity': 5},
            follow=True
        )
        cart = response.wsgi_request.session.get('cart', {})
        assert cart[str(book.id)] == 5

    def test_update_cart_zero_quantity(self, book):
        """Test updating cart quantity to zero."""
        client = Client()
        session = client.session
        session['cart'] = {str(book.id): 5}
        session.save()

        response = client.post(
            reverse('update_cart', args=[book.id]),
            {'quantity': 0},
            follow=True
        )
        cart = response.wsgi_request.session.get('cart', {})
        assert cart.get(str(book.id)) == 5


@pytest.mark.django_db
class TestRemoveFromCartView:
    """Test remove from cart view."""

    @pytest.fixture
    def category(self):
        """Fiction category fixture."""
        return Category.objects.create(name="Fiction")

    @pytest.fixture
    def book(self, category):
        """Book fixture."""
        return Book.objects.create(
            category=category,
            title="Test Book",
            author="Author",
            publisher="Publisher",
            pages=300,
            language="English",
            price=Decimal("19.99"),
            cover="hardcover",
            paper="white",
            isbn="978-3-16-148410-0",
            publication_date=date(2020, 1, 1),
        )

    def test_remove_from_cart(self, book):
        """Test remove from cart."""
        client = Client()
        session = client.session
        session['cart'] = {str(book.id): 2}
        session.save()

        response = client.get(reverse('remove_from_cart', args=[book.id]), follow=True)
        cart = response.wsgi_request.session.get('cart', {})
        assert str(book.id) not in cart

    def test_remove_nonexistent_item(self):
        """Test remove from cart with nonexistent item."""
        client = Client()
        session = client.session
        session['cart'] = {}
        session.save()

        response = client.get(reverse('remove_from_cart', args=[999]), follow=True)
        assert response.status_code == 200
