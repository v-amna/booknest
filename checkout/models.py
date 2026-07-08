"""Models for the checkout app."""

from django.db import models
from profiles.models import UserProfile
from books.models import Book
from django.db.models import Sum
from django_countries.fields import CountryField


class Order(models.Model):
    """Order model."""

    class PaymentStatus(models.TextChoices):
        """
        Enum-like class for payment statuses.

        based on Ref: https://docs.stripe.com
           /payments/payment-intents/verifying-status#payment-status-mapping
        """

        pending = "PD", "Pending"
        succeeded = "IS", "Succeeded"
        failed = "FL", "Failed"

    class OrderStatus(models.TextChoices):
        """Enum-like class for order statuses."""

        pending = "PD", "Pending"
        shipped = "SH", "Shipped"
        processing = "PR", "Processing"
        returned = "RT", "Returned"
        delivered = "DR", "Delivered"

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

    payment_status = models.CharField(
        max_length=2,
        choices=PaymentStatus,
        default=PaymentStatus.pending
    )

    order_status = models.CharField(
        max_length=2,
        choices=OrderStatus,
        default=OrderStatus.pending
    )

    # STRIPE + WEBHOOK CORE
    stripe_pid = models.CharField(
        max_length=254,
        null=True,
        blank=True,
        unique=True
    )

    def update_total(self):
        """Update total based on order quantity."""
        self.order_total = (
                self.lineitems.aggregate(
                    Sum('lineitem_total'))['lineitem_total__sum'] or 0
        )

        self.save()

    def __str__(self):
        """Return string representation of the order."""
        return f"Order {self.id}"


class OrderLineItem(models.Model):
    """Model class for order items."""

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
        """On save update total based on quantity."""
        self.lineitem_total = (
                self.book.price * self.quantity
        )

        super().save(*args, **kwargs)
        self.order.update_total()

        # self.save()

    def __str__(self):
        """Return string representation of the order line item."""
        return (
            f"{self.book.title} "
            f"on Order {self.order.id}"
        )
