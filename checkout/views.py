from profiles.models import UserProfile
from django.shortcuts import render, redirect,get_object_or_404
from .models import Order
from django.contrib import messages
from books.models import Book
from django.conf import settings
import stripe
from .forms import OrderForm
from .models import Order, OrderLineItem




def checkout(request):

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart=request.session.get('cart', {})
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
    # Create Stripe PaymentIntent
    stripe_total = round(grand_total * 100)
    stripe.api_key = stripe_secret_key

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.method == "POST":

        form = OrderForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            if request.user.is_authenticated:

                profile = UserProfile.objects.get(
                    user=request.user
            )

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

        form = OrderForm()
    if not stripe_public_key:
        messages.warning(
            request,
            'Stripe public key is missing. Please set it in your environment variables.'
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