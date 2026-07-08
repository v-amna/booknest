"""Admin app registration for the profiles' app."""

from django.contrib import admin
from .models import UserProfile

# Register your models here.
admin.site.register(UserProfile)
