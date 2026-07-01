from .widgets import CustomClearableFileInput
from django import forms
from .models import Book


class BookForm(forms.ModelForm):

    cover_image = forms.ImageField(
        label="Image",
        required=False,
        widget=CustomClearableFileInput()
    )

    class Meta:
        model = Book

        fields = "__all__"