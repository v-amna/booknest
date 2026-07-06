from django.urls import path
from . import views

urlpatterns = [
    path('newsletter', views.newsletters_subscribe,
         name='newsletter_subscribe'),
    path('newsletter/unsubscribe', views.newsletters_unsubscribe,
         name='newsletter_unsubscribe'),
]
