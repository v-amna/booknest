import json
from urllib import request
import cart
from profiles.models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404

from profiles.views import profile
from .models import Order
from django.contrib import messages
from books.models import Book
from django.conf import settings
import stripe
from .forms import OrderForm
from .models import Order, OrderLineItem
from django.http import HttpResponse
from django.views.decorators.http import require_POST


@require_POST
def cache_checkout_data(request):
    """Attach checkout metadata to the Stripe PaymentIntent."""

    try:
        pid = request.POST.get("client_secret").split("_secret")[0]

        stripe.api_key = settings.STRIPE_SECRET_KEY

        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "cart": json.dumps(request.session.get("cart", {})),
                "save_info": request.POST.get("save_info", ""),
                "username": (
                    request.user.username
                    if request.user.is_authenticated
                    else "AnonymousUser"
                ),
            },
        )

        return HttpResponse(status=200)

    except Exception as e:
        messages.error(
            request,
            "Sorry, your payment cannot be processed right now." +
            " Please try again later."
        )
        return HttpResponse(content=str(e), status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for item_id, quantity in cart.items():
        book = get_object_or_404(Book, pk=item_id)

        subtotal = book.price * quantity
        total += subtotal

        cart_items.append({
            'book': book,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    delivery = 0
    grand_total = total + delivery
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect("view_cart")

    # Create Stripe PaymentIntent
    stripe_total = round(grand_total * 100)
    stripe.api_key = stripe_secret_key

    if request.method == "POST":

        form = OrderForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            if request.user.is_authenticated:

                profile = UserProfile.objects.filter(user=request.user).first()

                if profile:
                    order.user_profile = profile

            order.save()

            for item_id, quantity in cart.items():
                book = get_object_or_404(
                    Book,
                    pk=item_id
                )

                OrderLineItem.objects.create(
                    order=order,
                    book=book,
                    quantity=quantity
                )
            request.session['cart'] = {}

            messages.success(
                request,
                "Order created successfully."
            )

            return redirect(
                'checkout_success',
                order_id=order.id
            )

    else:
        # Create a new payment intent on GET
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        form = OrderForm()
        form.fields['stripe_pid'].initial = intent.id
    if not stripe_public_key:
        messages.warning(
            request,
            'Stripe public key is missing.'
            + 'Please set it in your environment variables.'
        )

    context = {
        "form": form,
        "stripe_public_key": stripe_public_key,
        "client_secret": intent.client_secret,
        "cart_items": cart_items,
        "total": total,
        "delivery": delivery,
        "grand_total": grand_total
    }

    return render(
        request,
        'checkout/checkout.html',
        context
    )


def checkout_success(request, order_id):
    order = get_object_or_404(
        Order,
        pk=order_id
    )

    context = {
        'order': order,
    }

    return render(
        request,
        'checkout/checkout_success.html',
        context
    )
