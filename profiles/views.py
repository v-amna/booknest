from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import UserProfileForm
from .models import UserProfile


@login_required
def profile_orders(request):
    profile = UserProfile.objects.get(user=request.user)
    orders = profile.order_set.all().order_by('-date')

    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    orders_page = paginator.get_page(page_number)

    return render(
        request,
        'profiles/orders.html',
        {'orders': orders_page},
    )

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        form = UserProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Profile updated successfully.'
            )

    else:

        form = UserProfileForm(
            instance=profile
        )

    context = {
        'form': form,
        'orders': profile.order_set.all(),
    }

    return render(
        request,
        'profiles/profile.html',
        context
    )
