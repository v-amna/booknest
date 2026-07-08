"""AppConfig for profiles app."""

from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """AppConfig for profiles app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "profiles"

    def ready(self):
        """Import signal handler for the profiles' app."""
        import profiles.signals  # noqa :F401
