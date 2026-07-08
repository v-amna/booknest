from .widgets import CustomClearableFileInput
from django import forms
from .models import Book, Review


class BookForm(forms.ModelForm):
    cover_image = forms.ImageField(
        label="Image",
        required=False,
        widget=CustomClearableFileInput()
    )

    class Meta:
        model = Book
        fields = "__all__"

    def clean(self):
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

        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review

        fields = [
            "rating",
            "comment",
        ]

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
