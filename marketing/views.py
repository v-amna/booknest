from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from books.models import Category

from .forms import (
    CampaignForm,
    SubscriberAdminForm,
    SubscriberEditForm,
    SubscriberForm,
    UnsubscriberForm,
)
from .models import Campaign, EmailEvent, Subscriber


def send_campaign_emails(campaign):
    """
    Send a Campaign to all active Subscribers, using html_body if set,
    otherwise text_body. Records an EmailEvent per send.
    """
    is_html = bool(campaign.html_body)
    body = campaign.html_body if is_html else campaign.text_body

    subscribers = Subscriber.objects.filter(status=Subscriber.Status.ACTIVE)

    sent_count = 0

    for subscriber in subscribers:
        email = EmailMessage(
            subject=campaign.subject,
            body=body,
            to=[subscriber.email],
        )
        if is_html:
            email.content_subtype = "html"

        email.send()

        anymail_status = getattr(email, 'anymail_status', None)
        message_id = getattr(anymail_status, 'message_id', None) or ''

        EmailEvent.objects.create(
            campaign=campaign,
            subscriber=subscriber,
            event_type=EmailEvent.EventType.SENT,
            email_id=message_id,
        )

        sent_count += 1

    return sent_count


def send_subscription_confirmation_email(request, subscriber):
    """
    Send a confirmation email with an unsubscribe link to a new subscriber.
    """
    unsubscribe_url = request.build_absolute_uri(
        reverse('newsletter_unsubscribe')
    ) + f"?email={subscriber.email}"

    message = render_to_string(
        'marketing/emails/subscription_confirmation.txt',
        {'unsubscribe_url': unsubscribe_url},
    )

    send_mail(
        subject="Welcome to the BookNest Newsletter",
        message=message,
        from_email=None,
        recipient_list=[subscriber.email],
    )


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
                send_subscription_confirmation_email(request, subscriber)
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
        elif request.GET.get('email'):
            initial['email'] = request.GET.get('email')

        form = UnsubscriberForm(initial=initial)

    context = {
        'categories': Category.objects.all(),
        'is_unsubscribe': True,
        'form': form,
    }
    return render(request, 'marketing/newsletter.html', context)


@login_required
def campaign_list(request):
    """
    List and search Campaigns. Staff only.
    """
    if not request.user.is_staff:
        messages.error(
            request,
            "Sorry, only staff members can do that."
        )
        return redirect("home")

    campaigns = Campaign.objects.all().order_by('-created_at')

    query = request.GET.get('q', '').strip()
    if query:
        campaign_filter = Q(title__icontains=query)
        if query.isdigit():
            campaign_filter |= Q(id=int(query))
        campaigns = campaigns.filter(campaign_filter)

    paginator = Paginator(campaigns, 10)
    page_number = request.GET.get('page')
    campaigns_page = paginator.get_page(page_number)

    context = {
        'campaigns': campaigns_page,
        'query': query,
    }
    return render(request, 'marketing/campaign_list.html', context)


@login_required
def add_campaign(request):
    """
    Create a Campaign. Staff only.
    """
    if not request.user.is_staff:
        messages.error(
            request,
            "Sorry, only staff members can do that."
        )
        return redirect("home")

    if request.method == 'POST':
        form = CampaignForm(request.POST)

        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.created_by = request.user
            campaign.save()

            messages.success(
                request,
                "Campaign created successfully."
            )

            return redirect("campaign_list")
    else:
        form = CampaignForm()

    context = {
        'form': form,
    }
    return render(request, 'marketing/add_campaign.html', context)


@login_required
def edit_campaign(request, campaign_id):
    """
    Edit a Campaign. Staff only.
    """
    if not request.user.is_staff:
        messages.error(
            request,
            "Sorry, only staff members can do that."
        )
        return redirect("home")

    campaign = get_object_or_404(Campaign, pk=campaign_id)

    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Campaign updated successfully."
            )

            return redirect("campaign_list")
    else:
        form = CampaignForm(instance=campaign)

    context = {
        'form': form,
        'campaign': campaign,
    }
    return render(request, 'marketing/edit_campaign.html', context)


@login_required
def send_campaign(request, campaign_id):
    """
    Send a Campaign to all active Subscribers. Staff only.
    """
    if not request.user.is_staff:
        messages.error(
            request,
            "Sorry, only staff members can do that."
        )
        return redirect("home")

    campaign = get_object_or_404(Campaign, pk=campaign_id)

    sent_count = send_campaign_emails(campaign)

    campaign.status = Campaign.Status.SENT
    campaign.sent_at = timezone.now()
    campaign.save(update_fields=['status', 'sent_at'])

    messages.success(
        request,
        f"Campaign sent to {sent_count} subscriber(s)."
    )

    return redirect("campaign_list")


@login_required
def delete_campaign(request, campaign_id):
    """
    Delete a Campaign. Staff only.
    """
    if not request.user.is_staff:
        messages.error(
            request,
            "Sorry, only staff members can do that."
        )
        return redirect("home")

    campaign = get_object_or_404(Campaign, pk=campaign_id)
    campaign.delete()

    messages.success(
        request,
        "Campaign deleted successfully."
    )

    return redirect("campaign_list")


@login_required
def subscriber_list(request):
    """
    List and search Subscribers. Staff only.
    """
    if not request.user.is_staff:
        messages.error(
            request,
            "Sorry, only staff members can do that."
        )
        return redirect("home")

    subscribers = Subscriber.objects.all().order_by('-subscribed_at')

    query = request.GET.get('q', '').strip()
    if query:
        subscriber_filter = Q(email__icontains=query)
        if query.isdigit():
            subscriber_filter |= Q(id=int(query))
        subscribers = subscribers.filter(subscriber_filter)

    paginator = Paginator(subscribers, 10)
    page_number = request.GET.get('page')
    subscribers_page = paginator.get_page(page_number)

    context = {
        'subscribers': subscribers_page,
        'query': query,
    }
    return render(request, 'marketing/subscriber_list.html', context)


@login_required
def add_subscriber(request):
    """
    Create a Subscriber. Staff only.
    """
    if not request.user.is_staff:
        messages.error(
            request,
            "Sorry, only staff members can do that."
        )
        return redirect("home")

    if request.method == 'POST':
        form = SubscriberAdminForm(request.POST)

        if form.is_valid():
            subscriber = form.save()
            send_subscription_confirmation_email(request, subscriber)

            messages.success(
                request,
                "Subscriber created successfully."
            )

            return redirect("subscriber_list")
    else:
        form = SubscriberAdminForm()

    context = {
        'form': form,
    }
    return render(request, 'marketing/add_subscriber.html', context)


@login_required
def edit_subscriber(request, subscriber_id):
    """
    Edit a Subscriber. Staff only. Email cannot be changed.
    """
    if not request.user.is_staff:
        messages.error(
            request,
            "Sorry, only staff members can do that."
        )
        return redirect("home")

    subscriber = get_object_or_404(Subscriber, pk=subscriber_id)

    if request.method == 'POST':
        form = SubscriberEditForm(request.POST, instance=subscriber)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Subscriber updated successfully."
            )

            return redirect("subscriber_list")
    else:
        form = SubscriberEditForm(instance=subscriber)

    context = {
        'form': form,
        'subscriber': subscriber,
    }
    return render(request, 'marketing/edit_subscriber.html', context)


@login_required
def delete_subscriber(request, subscriber_id):
    """
    Delete a Subscriber. Staff only.
    """
    if not request.user.is_staff:
        messages.error(
            request,
            "Sorry, only staff members can do that."
        )
        return redirect("home")

    subscriber = get_object_or_404(Subscriber, pk=subscriber_id)
    subscriber.delete()

    messages.success(
        request,
        "Subscriber deleted successfully."
    )

    return redirect("subscriber_list")
