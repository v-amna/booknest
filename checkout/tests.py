"""Test for checkout app."""

import pytest
from decimal import Decimal
from datetime import date
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from books.models import Book, Category
from .models import Order, OrderLineItem


@pytest.mark.django_db
class TestOrderModel:
    """Order model tests."""

    @pytest.fixture
    def user(self):
        """User fixture."""
        return User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    @pytest.fixture
    def user_profile(self, user):
        """User profile fixtures."""
        profile = user.userprofile
        profile.default_phone_number = "1234567890"
        profile.default_street_address1 = "123 Berlin Str"
        profile.default_town_or_city = "Yorkstr"
        profile.default_country = "DE"
        profile.save()
        return profile

    def test_order_creation(self, user_profile):
        """Test order creation."""
        order = Order.objects.create(
            user_profile=user_profile,
            full_name="Test User",
            email="test@example.com",
            phone_number="1234567890",
            street_address1="123 Berlin Str",
            town_or_city="Yorkstr",
            country="DE",
            stripe_pid="test_pid_123",
        )
        assert order.full_name == "Test User"
        assert order.payment_status == Order.PaymentStatus.pending
        assert order.order_status == Order.OrderStatus.pending

    def test_order_str(self, user_profile):
        """Test order str display."""
        order = Order.objects.create(
            user_profile=user_profile,
            full_name="Test User",
            email="test@example.com",
            phone_number="1234567890",
            street_address1="123 Berlin Str",
            town_or_city="Yorkstr",
            country="DE",
        )
        assert str(order) == f"Order {order.id}"

    def test_order_update_total(self, user_profile):
        """Test order update total."""
        category = Category.objects.create(name="Fiction")
        book = Book.objects.create(
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

        order = Order.objects.create(
            user_profile=user_profile,
            full_name="Test User",
            email="test@example.com",
            phone_number="1234567890",
            street_address1="123 Berlin Str",
            town_or_city="Yorkstr",
            country="DE",
        )

        OrderLineItem.objects.create(order=order, book=book, quantity=2)

        assert order.order_total == Decimal("39.98")

    def test_stripe_pid_unique(self, user_profile):
        """Test stripe pid unique constraint."""
        Order.objects.create(
            user_profile=user_profile,
            full_name="Test User",
            email="test@example.com",
            phone_number="1234567890",
            street_address1="123 Berlin Str",
            town_or_city="Yorkstr",
            country="DE",
            stripe_pid="unique_pid",
        )

        with pytest.raises(Exception):
            Order.objects.create(
                user_profile=user_profile,
                full_name="Another User",
                email="another@example.com",
                phone_number="9876543210",
                street_address1="403 BERLIn",
                town_or_city="Boston",
                country="DE",
                stripe_pid="unique_pid",
            )


@pytest.mark.django_db
class TestOrderLineItemModel:
    """Test Order item model."""

    @pytest.fixture
    def user_profile(self):
        """User profile fixtures."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        return user.userprofile

    @pytest.fixture
    def order(self, user_profile):
        """Order fixture."""
        return Order.objects.create(
            user_profile=user_profile,
            full_name="Test User",
            email="test@example.com",
            phone_number="1234567890",
            street_address1="123 Berlin Str",
            town_or_city="Yorkstr",
            country="DE",
        )

    @pytest.fixture
    def book(self):
        """Book fixtures."""
        category = Category.objects.create(name="Fiction")
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

    def test_line_item_creation(self, order, book):
        """Item creation test."""
        item = OrderLineItem.objects.create(order=order, book=book, quantity=2)
        assert item.quantity == 2
        assert item.lineitem_total == Decimal("39.98")

    def test_line_item_str(self, order, book):
        """Test line item string display."""
        item = OrderLineItem.objects.create(order=order, book=book, quantity=1)
        assert str(item) == f"{book.title} on Order {order.id}"

    def test_line_item_cascade_on_order_delete(self, order, book):
        """Test item cascade on order delete."""
        item = OrderLineItem.objects.create(order=order, book=book, quantity=1)
        order.delete()
        with pytest.raises(OrderLineItem.DoesNotExist):
            OrderLineItem.objects.get(id=item.id)

    def test_line_item_cascade_on_book_delete(self, order, book):
        """Test item cascade delete on book delete."""
        item = OrderLineItem.objects.create(order=order, book=book, quantity=1)
        book.delete()
        with pytest.raises(OrderLineItem.DoesNotExist):
            OrderLineItem.objects.get(id=item.id)


@pytest.mark.django_db
class TestCheckoutSuccessView:
    """Checkout success view."""

    @pytest.fixture
    def user_profile(self):
        """User Profile fixture."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        return user.userprofile

    @pytest.fixture
    def order(self, user_profile):
        """Order fixture."""
        return Order.objects.create(
            user_profile=user_profile,
            full_name="Test User",
            email="test@example.com",
            phone_number="1234567890",
            street_address1="123 Berlin Str",
            town_or_city="Yorkstr",
            country="DE",
        )

    def test_checkout_success_view(self, order):
        """Test checkout success view."""
        client = Client()
        response = client.get(reverse("checkout_success", args=[order.id]))
        assert response.status_code == 200
        assert response.context["order"] == order

    def test_checkout_success_404(self):
        """Test checkout success view with 404."""
        client = Client()
        response = client.get(reverse("checkout_success", args=[999]))
        assert response.status_code == 404


@pytest.mark.django_db
class TestCacheCheckoutDataView:
    """Test Cache Checkout Data View."""

    @pytest.fixture
    def user(self):
        """User fixture."""
        return User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_cache_checkout_data_anonymous_user(self):
        """Test cache_checkout_data with anonymous user."""
        client = Client()
        session = client.session
        session["cart"] = {"1": 2}
        session.save()

        response = client.post(
            reverse("cache_checkout_data"),
            {"client_secret": "test_secret_123"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        assert response.status_code in [200, 400]

    def test_cache_checkout_data_authenticated_user(self, user):
        """Test cache_checkout_data with authenticated user."""
        client = Client()
        client.login(username="testuser", password="testpass123")
        session = client.session
        session["cart"] = {"1": 2}
        session.save()

        response = client.post(
            reverse("cache_checkout_data"),
            {"client_secret": "test_secret_123"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        assert response.status_code in [200, 400]
