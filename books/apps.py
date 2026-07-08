"""Book App config."""

from django.apps import AppConfig


class BooksConfig(AppConfig):
    """Books app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "books"
