"""Book app test."""

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from decimal import Decimal
from datetime import date

from .models import Category, Book, Review


@pytest.mark.django_db
class TestCategoryModel:
    """
    Test Category Model functionality.

    Includes creation, unique, and string display.
    """

    def test_category_creation(self):
        """Test the creation of a Category instance and its string display."""
        cat = Category.objects.create(name="Fiction")
        assert cat.name == "Fiction"
        assert str(cat) == "Fiction"

    def test_category_unique_name(self):
        """Test the creation of a Category instance and its string display."""
        Category.objects.create(name="Fiction")
        with pytest.raises(Exception):
            Category.objects.create(name="Fiction")


@pytest.mark.django_db
class TestBookModel:
    """
    Test Book Model functionality create, isbn unique, and string display.

    Includes category relation.
    """

    @pytest.fixture
    def category(self):
        """Fixture to create a Category instance for testing."""
        return Category.objects.create(name="Fiction")

    @pytest.fixture
    def book(self, category):
        """Fixture to create a Book instance for testing."""
        return Book.objects.create(
            category=category,
            title="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            description="Test description",
            meta_keywords="test, keywords",
            pages=300,
            language="English",
            price=Decimal("19.99"),
            discount_rate=10,
            discounted_price=Decimal("17.99"),
            cover="hardcover",
            paper="white",
            isbn="978-3-16-148410-0",
            publication_date=date(2020, 1, 1),
        )

    def test_book_creation(self, book):
        """Test book fields and it's type."""
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.price == Decimal("19.99")
        assert str(book) == "Test Book"

    def test_book_isbn_unique(self, book):
        """Test ISBN is unique constraint."""
        with pytest.raises(Exception):
            Book.objects.create(
                title="Another Book",
                author="Another Author",
                publisher="Publisher",
                pages=200,
                language="English",
                price=Decimal("15.00"),
                cover="paperback",
                paper="white",
                isbn=book.isbn,
                publication_date=date(2021, 1, 1),
            )

    def test_book_category_nullable(self):
        """Test book-category is relation."""
        book = Book.objects.create(
            title="No Category Book",
            author="Author",
            publisher="Publisher",
            pages=100,
            language="English",
            price=Decimal("10.00"),
            cover="hardcover",
            paper="white",
            isbn="123-456-789",
            publication_date=date(2022, 1, 1),
        )
        assert book.category is None

    def test_book_timestamps(self, book):
        """Test auto-timestamps created_on and updated_on."""
        assert book.created_on is not None
        assert book.updated_on is not None


@pytest.mark.django_db
class TestReviewModel:
    """
    Tests for Review models.

    - Create Review objects
    - Type of Review model fields
    - Cascade delete of review on user/book delete
    """

    @pytest.fixture
    def user(self):
        """Test user fixture."""
        return User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    @pytest.fixture
    def category(self):
        """Test category fixture."""
        return Category.objects.create(name="Fiction")

    @pytest.fixture
    def book(self, category):
        """Test book fixture."""
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

    @pytest.fixture
    def review(self, user, book):
        """Test review fixture object."""
        return Review.objects.create(
            user=user,
            book=book,
            rating=5,
            comment="Great book!"
        )

    def test_review_creation(self, review):
        """Test review object creation."""
        assert review.rating == 5
        assert review.comment == "Great book!"

    def test_review_str(self, review, user, book):
        """Test review object string display."""
        expected = f"{book.title} - {user.username}"
        assert str(review) == expected

    def test_review_cascade_on_user_delete(self, review, user):
        """Review cascade delete on user delete."""
        user.delete()
        with pytest.raises(Review.DoesNotExist):
            Review.objects.get(id=review.id)

    def test_review_cascade_on_book_delete(self, review, book):
        """Review cascade delete on book delete."""
        book.delete()
        with pytest.raises(Review.DoesNotExist):
            Review.objects.get(id=review.id)


@pytest.mark.django_db
class TestBookListView:
    """
    Test for book list view.

    - List,pagination
    - Search by title
    - Filter category
    """

    @pytest.fixture
    def category(self):
        """Fixture to create a Category instance for testing."""
        return Category.objects.create(name="Fiction")

    @pytest.fixture
    def books(self, category):
        """Fixture to create a books instance for testing."""
        books = []
        for i in range(15):
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

    def test_book_list_view(self, books):
        """Book list view test."""
        client = Client()
        response = client.get(reverse('books'))
        assert response.status_code == 200
        assert 'books' in response.context
        assert 'categories' in response.context

    def test_book_list_pagination(self, books):
        """Book list pagination, 10 item per page."""
        client = Client()
        response = client.get(reverse('books'))
        assert len(response.context['books']) == 10

    def test_book_list_search_by_title(self, books):
        """Book list search by title."""
        client = Client()
        response = client.get(reverse('books'), {'q': 'Book 1'})
        assert response.status_code == 200
        assert len(response.context['books']) > 0

    def test_book_list_filter_by_category(self, category, books):
        """Test book list filter by category."""
        client = Client()
        response = client.get(reverse('books'), {'category': category.name})
        assert response.status_code == 200
        assert len(response.context['books']) > 0


@pytest.mark.django_db
class TestBookDetailView:
    """
    Detailed book view test.

    - Book detail view
    """

    @pytest.fixture
    def category(self):
        """Fixture to create a Category instance for testing."""
        return Category.objects.create(name="Fiction")

    @pytest.fixture
    def book(self, category):
        """Fixture to create a Book instance for testing."""
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

    def test_book_detail_view(self, book):
        """Test book detail view."""
        client = Client()
        response = client.get(reverse('book_detail', args=[book.id]))
        assert response.status_code == 200
        assert response.context['book'] == book

    def test_book_detail_404(self):
        """Test book detail view 404."""
        client = Client()
        response = client.get(reverse('book_detail', args=[999]))
        assert response.status_code == 404
