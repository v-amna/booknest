from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Book categories
    """

    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book information
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books"
    )

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)

    pages = models.PositiveIntegerField()

    language = models.CharField(
        max_length=50,
        default="English"
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    discount_rate = models.PositiveIntegerField(
        default=0
    )

    discounted_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True
    )

    cover = models.CharField(
        max_length=50
    )

    paper = models.CharField(
        max_length=100
    )

    isbn = models.CharField(
        max_length=20,
        unique=True
    )

    publication_date = models.DateField()

    book_url = models.URLField(
        blank=True,
        null=True
    )

    cover_image = models.ImageField(
        upload_to="books/",
        blank=True,
        null=True
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Customer reviews
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveIntegerField()

    comment = models.TextField()

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.book.title} - {self.user.username}"
