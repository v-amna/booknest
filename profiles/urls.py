"""URLs for UserProfile."""

from django.urls import path

from .views import profile, profile_orders

urlpatterns = [
    path(
        '',
        profile,
        name='profile'
    ),
    path(
        'orders/',
        profile_orders,
        name='profile_orders'
    ),
]
