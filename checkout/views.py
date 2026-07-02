from profiles.models import UserProfile
from django.shortcuts import render, redirect,get_object_or_404
from .models import Order
from django.contrib import messages
from books.models import Book
from .forms import OrderForm
from .models import Order, OrderLineItem



def checkout(request):

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

    context = {
        "form": form,
        "stripe_public_key": "pk_test_51TeumHIkXOU5Pgli1nTQaUkh3NyaCDEGcfCuc6MbEotjg0uH5VDdxsq9Ur28rQo5lfMBYruOaiUqeUz5rkQlKKHn00BDOlTyAn",
        "client_secret": "sk_test_your_secret_key",
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