from django.urls import path
from . import views

urlpatterns = [
    path('newsletter', views.newsletters_subscribe,
         name='newsletter_subscribe'),
    path('newsletter/unsubscribe', views.newsletters_unsubscribe,
         name='newsletter_unsubscribe'),
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaigns/add/', views.add_campaign, name='add_campaign'),
    path('campaigns/<int:campaign_id>/edit/', views.edit_campaign, name='edit_campaign'),
    path('campaigns/<int:campaign_id>/delete/', views.delete_campaign, name='delete_campaign'),
]
