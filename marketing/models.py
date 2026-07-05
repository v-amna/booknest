import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Subscriber(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        UNSUBSCRIBED = "unsubscribed", "Unsubscribed"
        BOUNCED = "bounced", "Bounced"
        COMPLAINED = "complained", "Complained"

    # Identity
    email = models.EmailField(unique=True)
    user = models.OneToOneField(
        User,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="newsletter_subscriber",
    )

    # Status & unsubscribe
    status = models.CharField(max_length=20, choices=Status,
                              default=Status.ACTIVE)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    unsubscribe_reason = models.TextField(blank=True)

    # Confirmation (double opt-in)
    is_confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False,
                                          unique=True)

    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return self.email

    def unsubscribe(self, reason=""):
        self.status = self.Status.UNSUBSCRIBED
        self.unsubscribed_at = timezone.now()
        self.unsubscribe_reason = reason
        self.save(
            update_fields=["status", "unsubscribed_at", "unsubscribe_reason"])


class Campaign(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SCHEDULED = "scheduled", "Scheduled"
        SENDING = "sending", "Sending"
        SENT = "sent", "Sent"
        CANCELLED = "cancelled", "Cancelled"

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    preheader = models.CharField(max_length=200, blank=True)
    html_body = models.TextField()
    text_body = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=Status,
                              default=Status.DRAFT)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                                   related_name="campaigns")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} [{self.status}]"


class EmailEvent(models.Model):
    class EventType(models.TextChoices):
        SENT = "sent", "Sent"
        OPENED = "opened", "Opened"
        CLICKED = "clicked", "Clicked"
        BOUNCED = "bounced", "Bounced"
        COMPLAINED = "complained", "Complained"
        UNSUBSCRIBED = "unsubscribed", "Unsubscribed"

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE,
                                 related_name="events")
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE,
                                   related_name="events")

    event_type = models.CharField(max_length=20, choices=EventType)
    occurred_at = models.DateTimeField(auto_now_add=True)
    clicked_url = models.URLField(blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["campaign", "event_type"]),
            models.Index(fields=["subscriber", "event_type"]),
        ]

    def __str__(self):
        return (f"{self.subscriber.email}" +
                f"→ {self.event_type} ({self.campaign.title})")
