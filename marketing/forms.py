"""Forms for marketing app."""

from django import forms
from .models import Subscriber, Campaign


class SubscriberForm(forms.ModelForm):
    """
    Subscriber form for email Subscriber.

    For email Subscriber, a users can subscribe to the newsletter by providing
    their email address. This form is used to collect the email address of the
    subscriber.
    """

    class Meta:
        """Meta class."""

        model = Subscriber
        fields = ["email"]


class UnsubscriberForm(forms.ModelForm):
    """
    Unsubscriber form for email Unsubscriber.

    For email Subscriber, a users can unsubscribe from the newsletter by
    providing their email address and reason for unsubscribing.
    """

    class Meta:
        """Meta class."""

        model = Subscriber
        fields = ["email", "unsubscribe_reason"]
        labels = {
            "unsubscribe_reason": "Reason (optional)",
        }
        widgets = {
            "unsubscribe_reason": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        """Make unsubscribe not required reason."""
        super().__init__(*args, **kwargs)
        self.fields["unsubscribe_reason"].required = False


class CampaignForm(forms.ModelForm):
    """
    Campaign form for email campaign.

    Form for email Campaign. A staff user should be able to manage a campaign.
    """

    class Meta:
        """Meta class."""

        model = Campaign
        fields = [
            "title",
            "subject",
            "html_body",
            "text_body",
            "status"
        ]

    def __init__(self, *args, **kwargs):
        """Make both html/text body non-required."""
        super().__init__(*args, **kwargs)
        # Either one of them required, Checked on validation.
        self.fields["html_body"].required = False
        self.fields["text_body"].required = False

    def clean(self):
        """
        Validate the campaign data.

        Either html_body or text_body must be provided.
        """
        cleaned_data = super().clean()

        has_html = bool(cleaned_data.get("html_body"))
        has_text = bool(cleaned_data.get("text_body"))

        if not has_html and not has_text:
            raise forms.ValidationError(
                "Provide either an HTML body or a text body for the campaign."
            )

        if has_html and has_text:
            raise forms.ValidationError(
                "Provide either an HTML body or a text body for the "
                "campaign, not both."
            )

        return cleaned_data


class SubscriberAdminForm(forms.ModelForm):
    """For staff to manage a Subscriber record directly."""

    class Meta:
        """Meta class."""

        model = Subscriber
        fields = ["email", "status"]


class SubscriberEditForm(SubscriberAdminForm):
    """Same as SubscriberAdminForm but email cannot be changed once created."""

    def __init__(self, *args, **kwargs):
        """Make email readonly."""
        super().__init__(*args, **kwargs)
        self.fields["email"].disabled = True
