"""Book App forms."""
from .widgets import CustomClearableFileInput
from django import forms
from .models import Book, Review
import django.utils.timezone as timezone


class BookForm(forms.ModelForm):
    """Book model form, fixes publication_date field."""

    cover_image = forms.ImageField(
        label="Image",
        required=False,
        widget=CustomClearableFileInput()
    )

    class Meta:
        """Metaclass to fix fields attributes."""

        model = Book
        fields = "__all__"
        widgets = {
            "publication_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "max": timezone.now().date().isoformat()
                })
        }

    def clean(self):
        """Validate the book form."""
        cleaned_data = super().clean()

        price = cleaned_data.get("price")
        discounted_price = cleaned_data.get("discounted_price")

        if (
                price is not None and
                discounted_price is not None and
                discounted_price >= price
        ):
            raise forms.ValidationError(
                "Discounted price must be lower than the normal price."
            )

        publication_date = self.cleaned_data.get("publication_date")
        if publication_date and publication_date > timezone.now().date():
            raise forms.ValidationError(
                "Publication date cannot be in the future.")

        return cleaned_data


class ReviewForm(forms.ModelForm):
    """Review model form, fixes rating field."""

    class Meta:
        """Metaclass to fix fields attributes."""

        model = Review

        fields = [
            "rating",
            "comment",
        ]

    # Limit rating to 1-5 stars
    widgets = {
        "rating": forms.NumberInput(
            attrs={
                "min": 1,
                "max": 5,
            }
        ),
        "comment": forms.Textarea(
            attrs={
                "rows": 4,
            }
        ),
    }
