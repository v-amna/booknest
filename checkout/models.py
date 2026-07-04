from django.db import models
from django.contrib.auth.models import User
from profiles.models import UserProfile
from books.models import Book
from django.db.models import Sum
from django_countries.fields import CountryField


# Create your models here.


class Order(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    full_name = models.CharField(
        max_length=50
    )

    email = models.EmailField(
        max_length=254
    )

    phone_number = models.CharField(
        max_length=20
    )

    street_address1 = models.CharField(
        max_length=80
    )

    street_address2 = models.CharField(
        max_length=80,
        blank=True
    )

    town_or_city = models.CharField(
        max_length=40
    )

    postcode = models.CharField(
        max_length=20,
        blank=True
    )

    country = CountryField(
        blank_label="Select Country"
    )

    date = models.DateTimeField(
        auto_now_add=True
    )

    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    # STRIPE + WEBHOOK CORE

    stripe_pid = models.CharField(
        max_length=254,
        null=True,
        blank=True,
        unique=True
    )

    # Optional (debug / coursework evidence)
    original_cart = models.TextField(blank=True)

    def update_total(self):
        self.order_total = (
                self.lineitems.aggregate(
                    Sum('lineitem_total'))['lineitem_total__sum'] or 0
        )

        self.save()

    def __str__(self):
        return f"Order {self.id}"


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    lineitem_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )

    def save(self, *args, **kwargs):
        self.lineitem_total = (
                self.book.price * self.quantity
        )

        super().save(*args, **kwargs)
        self.order.update_total()

        # self.save()

    def __str__(self):
        return (
            f"{self.book.title} "
            f"on Order {self.order.id}"
        )
