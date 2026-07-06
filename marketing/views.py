from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from books.models import Category

from .forms import CampaignForm, SubscriberForm, UnsubscriberForm
from .models import Campaign, Subscriber


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
