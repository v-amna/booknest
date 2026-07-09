"""Configuration for pytest fixtures."""

import os
import django
from django.conf import settings  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "booknest.settings")


def pytest_configure():
    """Configure pytest-django."""
    django.setup()
