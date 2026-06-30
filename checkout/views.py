from profiles.models import UserProfile
from django.shortcuts import render, redirect,get_object_or_404
from .models import Order
from django.contrib import messages
from books.models import Book
from .forms import OrderForm
from .models import Order, OrderLineItem



def checkout(request):

    cart=request.session.get('cart', {})
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