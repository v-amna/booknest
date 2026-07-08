"""Forms for checkout app."""

from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """Order form for checkout process."""

    class Meta:
        """Meta class."""

        model = Order

        fields = [
            'full_name',
            'email',
            'phone_number',
            'street_address1',
            'street_address2',
            'town_or_city',
            'postcode',
            'country',
            'stripe_pid',
        ]

        widgets = {
            'stripe_pid': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form with default bootstrap class."""
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields["country"].widget.attrs["class"] = "form-select"
