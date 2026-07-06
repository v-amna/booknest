from django import forms
from .models import Subscriber, Campaign


class SubscriberForm(forms.ModelForm):
    """
    For email Subscriber, a users can subscribe to the newsletter by providing
    their email address. This form is used to collect the email address of the
    subscriber.
    """

    class Meta:
        model = Subscriber
        fields = ["email"]


class UnsubscriberForm(forms.ModelForm):
    """
    For email Subscriber, a users can unsubscribe from the newsletter by
    providing their email address and reason for unsubscribing.
    """

    class Meta:
        model = Subscriber
        fields = ["email", "unsubscribe_reason"]
        labels = {
            "unsubscribe_reason": "Reason (optional)",
        }
        widgets = {
            "unsubscribe_reason": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["unsubscribe_reason"].required = False


class CampaignForm(forms.ModelForm):
    """
    Form for email Campaign. A staff user should be able to manage a campaign.
    """

    class Meta:
        model = Campaign
        fields = [
            "title",
            "subject",
            "html_body",
            "text_body",
            "status"
        ]


class SubscriberAdminForm(forms.ModelForm):
    """
    For staff to manage a Subscriber record directly.
    """

    class Meta:
        model = Subscriber
        fields = ["email", "status"]


class SubscriberEditForm(SubscriberAdminForm):
    """
    Same as SubscriberAdminForm but email cannot be changed once created.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].disabled = True
