"""Widgets for books app."""

from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    """Custom ClearableFileInput for books app."""

    template_name = ("books/custom_widget_templates" +
                     "/custom_clearable_file_input.html")
