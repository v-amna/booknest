from django.shortcuts import redirect, render , get_object_or_404
from django.contrib import messages

from books.models import Book

# Create your views here.
def view_cart(request):

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

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(
        request,
        'cart/cart.html',
        context
    )
def add_to_cart(request, item_id):

    book = get_object_or_404(Book, pk=item_id)

    cart = request.session.get('cart', {})

    item_id = str(item_id)

    if item_id in cart:
        cart[item_id] += 1
    else:
        cart[item_id] = 1

    request.session['cart'] = cart

    messages.success(
        request,
        f'{book.title} added to your cart.'
    )

    return redirect('view_cart')
def update_cart(request, item_id):

    quantity = int(request.POST.get('quantity'))

    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[str(item_id)] = quantity

    request.session['cart'] = cart

    messages.success(
        request,
        'Cart updated successfully.'
    )

    return redirect('view_cart')

def remove_from_cart(request, item_id):

    cart = request.session.get('cart', {})

    item_id = str(item_id)

    if item_id in cart:
        del cart[item_id]

    request.session['cart'] = cart

    messages.success(
        request,
        'Item removed from cart.'
    )

    return redirect('view_cart')