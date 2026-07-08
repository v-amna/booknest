"""Webhook handler for stripe."""

import json
import stripe
from django.http import HttpResponse
from checkout.models import Order, OrderLineItem
from books.models import Book
from django.contrib.auth.models import User


def handle_payment_intent_payment_failed(event):
    """Handle the payment_intent.payment_failed webhook from Stripe."""
    pid = event.data.object.id
    order = Order.objects.filter(stripe_pid=pid).first()
    if order:
        order.payment_status = Order.PaymentStatus.failed
        order.save()
    return HttpResponse(
        content=f'Webhook received: {event["type"]} | Order payment failed',
        status=200
    )


class StripeWHHandler:
    """Handle Stripe webhooks."""

    def __init__(self, request):
        """Init request for Stripe webhook handler."""
        self.request = request

    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event."""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """Handle successful Stripe payment_intent.succeeded webhook."""
        intent = event.data.object
        pid = intent.id

        # Check if already exists
        order = Order.objects.filter(stripe_pid=pid).first()

        if order and order.payment_status != Order.PaymentStatus.succeeded:
            order.payment_status = Order.PaymentStatus.succeeded
            order.save()
            return HttpResponse(
                content=f'Webhook received: {event["type"]}' +
                        ' | Order payment succeeded',
                status=200
            )

        if order:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | Order exists',
                status=200
            )

        # Load cart from Stripe metadata
        cart = json.loads(intent.metadata.cart)

        # Load user from metadata by username
        username = intent.metadata.username
        user = User.objects.get(username=username)

        # Get charge object (modern Stripe approach)
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details
        shipping = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # Clean empty shipping fields
        for field, value in shipping.address.to_dict().items():
            if value == "":
                shipping.address[field] = None

        # Creates order
        try:
            order = Order.objects.create(
                user_profile=user.userprofile,
                full_name=shipping.name,
                email=billing_details.email,
                phone_number=billing_details.phone,
                country=shipping.address.country,
                postcode=shipping.address.postal_code,
                town_or_city=shipping.address.city,
                street_address1=shipping.address.line1,
                street_address2=shipping.address.line2,
                order_total=grand_total,
                stripe_pid=pid,
            )

            for item_id, quantity in cart.items():

                try:
                    book = Book.objects.get(pk=item_id)

                    OrderLineItem.objects.create(
                        order=order,
                        book=book,
                        quantity=quantity,
                    )

                except Book.DoesNotExist:
                    order.delete()
                    return HttpResponse(
                        content=f'Webhook ERROR: Book {item_id} not found',
                        status=400
                    )

        except Exception as e:
            if order:
                order.delete()

            return HttpResponse(
                content=f'Webhook ERROR: {e}',
                status=500
            )

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | Order created',
            status=200
        )
