from django.contrib import messages
from django.shortcuts import render
from books.models import Category

from .forms import SubscriberForm, UnsubscriberForm
from .models import Subscriber


def newsletters_subscribe(request):
    """
    View for subscribing to newsletters if the user is not already subscribed.
    If the user is already subscribed, it will show a message indicating that
    they are already subscribed.
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        instance = Subscriber.objects.filter(email__iexact=email).first()

        form = SubscriberForm(request.POST, instance=instance)

        if form.is_valid():
            subscriber = form.save(commit=False)
            subscriber.status = Subscriber.Status.ACTIVE
            subscriber.unsubscribed_at = None
            subscriber.unsubscribe_reason = ""
            subscriber.save()

            if instance is not None:
                messages.success(
                    request,
                    "You already subscribed!"
                )
            elif instance is None:
                messages.success(
                    request,
                    "You've been subscribed to our newsletter."
                )
            form = SubscriberForm()
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['email'] = request.user.email

        form = SubscriberForm(initial=initial)

    context = {
        'categories': Category.objects.all(),
        'is_subscribe': True,
        'form': form,
    }
    return render(request, 'marketing/newsletter.html', context)


def newsletters_unsubscribe(request):
    """
    View for unsubscribing from newsletters.
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        instance = Subscriber.objects.filter(email__iexact=email).first()

        if instance is None:
            messages.error(
                request,
                "We couldn't find a subscription for that email."
            )
            form = UnsubscriberForm()
        else:
            form = UnsubscriberForm(request.POST, instance=instance)

            if form.is_valid():
                instance.unsubscribe(
                    reason=form.cleaned_data.get('unsubscribe_reason', '')
                )

                messages.warning(
                    request,
                    "You've been unsubscribed from our newsletter."
                )
                form = UnsubscriberForm()
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['email'] = request.user.email

        form = UnsubscriberForm(initial=initial)

    context = {
        'categories': Category.objects.all(),
        'is_unsubscribe': True,
        'form': form,
    }
    return render(request, 'marketing/newsletter.html', context)
