from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from books.models import Book
from .forms import OrderForm
from .models import Order, OrderLineItem


def checkout(request):

    cart=request.session.get('cart', {})
    if request.method == "POST":

        form = OrderForm(request.POST)

        if form.is_valid():

            order = form.save()

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

            messages.success(
                request,
                "Order created successfully."
            )

            return redirect("home")

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