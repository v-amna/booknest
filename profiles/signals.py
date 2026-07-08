"""Signals for the profiles app."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """On create, creates a new user profile instance."""
    if created:
        UserProfile.objects.create(
            user=instance
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """On save, saves the user profile."""
    if hasattr(instance, "userprofile"):
        instance.userprofile.save()
