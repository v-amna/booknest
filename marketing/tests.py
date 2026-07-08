"""Tests for marketing app models and views."""

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from .models import Subscriber, Campaign, EmailEvent


@pytest.mark.django_db
class TestSubscriberModel:
    """Subscriber model tests."""

    def test_subscriber_creation(self):
        """Test subscriber creation with default values."""
        sub = Subscriber.objects.create(email="test@example.com")
        assert sub.email == "test@example.com"
        assert sub.status == Subscriber.Status.ACTIVE
        assert not sub.is_confirmed
        assert str(sub) == "test@example.com"

    def test_subscriber_email_unique(self):
        """Test email uniqueness constraint."""
        Subscriber.objects.create(email="test@example.com")
        with pytest.raises(Exception):
            Subscriber.objects.create(email="test@example.com")

    def test_subscriber_with_user(self):
        """Test subscriber creation with associated user."""
        user = User.objects.create_user(
            username="testuser", email="user@example.com", password="pass123"
        )
        sub = Subscriber.objects.create(email="test@example.com", user=user)
        assert sub.user == user

    def test_subscriber_unsubscribe(self):
        """Test subscriber unsubscribe method."""
        sub = Subscriber.objects.create(email="test@example.com")
        sub.unsubscribe(reason="Not interested")
        sub.refresh_from_db()
        assert sub.status == Subscriber.Status.UNSUBSCRIBED
        assert sub.unsubscribed_at is not None
        assert sub.unsubscribe_reason == "Not interested"

    def test_subscriber_confirmation_token(self):
        """Test confirmation token uniqueness."""
        sub1 = Subscriber.objects.create(email="test1@example.com")
        sub2 = Subscriber.objects.create(email="test2@example.com")
        assert sub1.confirmation_token != sub2.confirmation_token

    def test_subscriber_cascade_on_user_delete(self):
        """Test subscriber cascades on user deletion."""
        user = User.objects.create_user(username="testuser",
                                        password="pass123")
        sub = Subscriber.objects.create(email="test@example.com", user=user)
        user.delete()
        sub.refresh_from_db()
        assert sub.user is None


@pytest.mark.django_db
class TestCampaignModel:
    """Campaign model tests. After staff user login."""

    @pytest.fixture
    def user(self):
        """Staff user fixture."""
        return User.objects.create_user(
            username="staff", password="pass123", is_staff=True
        )

    def test_campaign_creation(self, user):
        """Test campaign creation with default values."""
        campaign = Campaign.objects.create(
            title="Test Campaign",
            subject="Test Subject",
            html_body="<p>Test</p>",
            created_by=user,
        )
        assert campaign.title == "Test Campaign"
        assert campaign.status == Campaign.Status.DRAFT
        assert campaign.created_by == user
        assert campaign.sent_at is None

    def test_campaign_str(self, user):
        """Test campaign string representation."""
        campaign = Campaign.objects.create(
            title="Test", subject="Test", html_body="<p>Test</p>",
            created_by=user
        )
        assert str(campaign) == "Test [draft]"

    def test_campaign_status_choices(self, user):
        """Test campaign status choices."""
        campaign = Campaign.objects.create(
            title="Test",
            subject="Test",
            html_body="<p>Test</p>",
            created_by=user,
            status=Campaign.Status.READY,
        )
        assert campaign.status == Campaign.Status.READY

    def test_campaign_cascade_on_user_delete(self):
        """Test campaign cascades on user deletion."""
        user = User.objects.create_user(
            username="staff", password="pass123", is_staff=True
        )
        campaign = Campaign.objects.create(
            title="Test", subject="Test", html_body="<p>Test</p>",
            created_by=user
        )
        user.delete()
        campaign.refresh_from_db()
        assert campaign.created_by is None


@pytest.mark.django_db
class TestEmailEventModel:
    """Email event model tests. After staff user login."""

    @pytest.fixture
    def subscriber(self):
        """Fixture for subscriber model."""
        return Subscriber.objects.create(email="test@example.com")

    @pytest.fixture
    def campaign(self):
        """Campaign fixture."""
        user = User.objects.create_user(
            username="staff", password="pass123", is_staff=True
        )
        return Campaign.objects.create(
            title="Test", subject="Test", html_body="<p>Test</p>",
            created_by=user
        )

    def test_email_event_creation(self, campaign, subscriber):
        """Test email event creation."""
        event = EmailEvent.objects.create(
            campaign=campaign,
            subscriber=subscriber,
            event_type=EmailEvent.EventType.SENT,
        )
        assert event.campaign == campaign
        assert event.subscriber == subscriber
        assert event.event_type == EmailEvent.EventType.SENT

    def test_email_event_str(self, campaign, subscriber):
        """Test email event string representation."""
        event = EmailEvent.objects.create(
            campaign=campaign,
            subscriber=subscriber,
            event_type=EmailEvent.EventType.OPENED,
        )
        assert "test@example.com" in str(event)
        assert "opened" in str(event)

    def test_email_event_cascade_on_campaign_delete(self, campaign,
                                                    subscriber):
        """Test email event cascades on campaign deletion."""
        event = EmailEvent.objects.create(
            campaign=campaign,
            subscriber=subscriber,
            event_type=EmailEvent.EventType.SENT,
        )
        campaign.delete()
        with pytest.raises(EmailEvent.DoesNotExist):
            EmailEvent.objects.get(id=event.id)

    def test_email_event_cascade_on_subscriber_delete(self, campaign,
                                                      subscriber):
        """Test email event cascades on subscriber deletion."""
        event = EmailEvent.objects.create(
            campaign=campaign,
            subscriber=subscriber,
            event_type=EmailEvent.EventType.SENT,
        )
        subscriber.delete()
        with pytest.raises(EmailEvent.DoesNotExist):
            EmailEvent.objects.get(id=event.id)


@pytest.mark.django_db
class TestNewslettersSubscribeView:
    """Newsletter subscribe view tests. After staff user login."""

    def test_subscribe_view_get(self):
        """Test GET request to subscribe view."""
        client = Client()
        response = client.get(reverse("newsletter_subscribe"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_subscribe_post_new_subscriber(self):
        """Test POST request to subscribe new subscriber."""
        client = Client()
        client.post(reverse("newsletter_subscribe"),
                    {"email": "new@example.com"})
        assert Subscriber.objects.filter(email="new@example.com").exists()

    def test_subscribe_post_existing_subscriber(self):
        """Test POST request with existing subscriber email."""
        Subscriber.objects.create(email="existing@example.com")
        client = Client()
        client.post(reverse("newsletter_subscribe"),
                    {"email": "existing@example.com"})
        assert Subscriber.objects.filter(
            email="existing@example.com").count() == 1

    def test_subscribe_view_authenticated_user(self):
        """Test subscribe view with authenticated user."""
        User.objects.create_user(
            username="testuser", email="user@example.com", password="pass123"
        )
        client = Client()
        client.login(username="testuser", password="pass123")
        response = client.get(reverse("newsletter_subscribe"))
        assert response.status_code == 200


@pytest.mark.django_db
class TestNewslettersUnsubscribeView:
    """Newsletter unsubscribe view tests. After staff user login."""

    def test_unsubscribe_view_get(self):
        """Test GET request to unsubscribe view."""
        client = Client()
        response = client.get(reverse("newsletter_unsubscribe"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_unsubscribe_post_existing_subscriber(self):
        """Test POST request to unsubscribe existing subscriber."""
        sub = Subscriber.objects.create(
            email="test@example.com", status=Subscriber.Status.ACTIVE
        )
        client = Client()
        client.post(
            reverse("newsletter_unsubscribe"),
            {"email": "test@example.com",
             "unsubscribe_reason": "Not interested"},
        )
        sub.refresh_from_db()
        assert sub.status == Subscriber.Status.UNSUBSCRIBED

    def test_unsubscribe_post_nonexistent_subscriber(self):
        """Test POST request with nonexistent subscriber."""
        client = Client()
        response = client.post(
            reverse("newsletter_unsubscribe"),
            {"email": "notfound@example.com"}
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestCampaignListView:
    """Campaign list view tests. After staff user login."""

    @pytest.fixture
    def staff_user(self):
        """Staff user fixture."""
        return User.objects.create_user(
            username="staff", password="pass123", is_staff=True
        )

    @pytest.fixture
    def regular_user(self):
        """Regular user fixture."""
        return User.objects.create_user(username="regular", password="pass123")

    def test_campaign_list_staff_only(self, staff_user):
        """Test campaign list view is staff only."""
        client = Client()
        client.login(username="staff", password="pass123")
        response = client.get(reverse("campaign_list"))
        assert response.status_code == 200
        assert "campaigns" in response.context

    def test_campaign_list_regular_user_redirect(self, regular_user):
        """Test campaign list redirects non-staff users."""
        client = Client()
        client.login(username="regular", password="pass123")
        response = client.get(reverse("campaign_list"), follow=True)
        assert len(response.redirect_chain) > 0

    def test_campaign_list_not_logged_in(self):
        """Test campaign list redirects unauthenticated users."""
        client = Client()
        response = client.get(reverse("campaign_list"))
        assert response.status_code == 302


@pytest.mark.django_db
class TestAddCampaignView:
    """Add campaign view tests. After staff user login."""

    @pytest.fixture
    def staff_user(self):
        """Staff user fixture."""
        return User.objects.create_user(
            username="staff", password="pass123", is_staff=True
        )

    def test_add_campaign_get(self, staff_user):
        """Test GET request to add campaign view."""
        client = Client()
        client.login(username="staff", password="pass123")
        response = client.get(reverse("add_campaign"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_add_campaign_post(self, staff_user):
        """Test POST request to add campaign view."""
        client = Client()
        client.login(username="staff", password="pass123")
        data = {
            "title": "New Campaign",
            "subject": "Test Subject",
            "html_body": "<p>Test</p>",
            "status": Campaign.Status.DRAFT,
        }
        client.post(reverse("add_campaign"), data)
        assert Campaign.objects.filter(title="New Campaign").exists()


@pytest.mark.django_db
class TestEditCampaignView:
    """Edit campaign view tests. After staff user login."""

    @pytest.fixture
    def staff_user(self):
        """Staff user fixture."""
        return User.objects.create_user(
            username="staff", password="pass123", is_staff=True
        )

    @pytest.fixture
    def campaign(self, staff_user):
        """Campaign fixture."""
        return Campaign.objects.create(
            title="Original",
            subject="Test",
            html_body="<p>Test</p>",
            created_by=staff_user,
        )

    def test_edit_campaign_get(self, staff_user, campaign):
        """Test GET request to edit campaign view."""
        client = Client()
        client.login(username="staff", password="pass123")
        response = client.get(reverse("edit_campaign", args=[campaign.id]))
        assert response.status_code == 200
        assert response.context["campaign"] == campaign

    def test_edit_campaign_post(self, staff_user, campaign):
        """Test POST request to edit campaign view."""
        client = Client()
        client.login(username="staff", password="pass123")
        data = {
            "title": "Updated",
            "subject": "Test",
            "html_body": "<p>Updated</p>",
            "status": Campaign.Status.DRAFT,
        }
        client.post(reverse("edit_campaign", args=[campaign.id]),
                    data)
        campaign.refresh_from_db()
        assert campaign.title == "Updated"


@pytest.mark.django_db
class TestDeleteCampaignView:
    """Delete campaign view tests. After staff user login."""

    @pytest.fixture
    def staff_user(self):
        """Staff user fixture."""
        return User.objects.create_user(
            username="staff", password="pass123", is_staff=True
        )

    @pytest.fixture
    def campaign(self, staff_user):
        """Campaign fixture."""
        return Campaign.objects.create(
            title="Test", subject="Test", html_body="<p>Test</p>",
            created_by=staff_user
        )

    def test_delete_campaign(self, staff_user, campaign):
        """Test campaign deletion."""
        client = Client()
        client.login(username="staff", password="pass123")
        campaign_id = campaign.id
        client.post(reverse("delete_campaign", args=[campaign.id]))
        with pytest.raises(Campaign.DoesNotExist):
            Campaign.objects.get(id=campaign_id)


@pytest.mark.django_db
class TestSubscriberListView:
    """Subscriber list view tests. After staff user login."""

    @pytest.fixture
    def staff_user(self):
        """Staff user fixture."""
        return User.objects.create_user(
            username="staff", password="pass123", is_staff=True
        )

    def test_subscriber_list_staff_only(self, staff_user):
        """Test subscriber list view is staff only."""
        client = Client()
        client.login(username="staff", password="pass123")
        response = client.get(reverse("subscriber_list"))
        assert response.status_code == 200
        assert "subscribers" in response.context

    def test_subscriber_list_not_logged_in(self):
        """Test subscriber list redirects unauthenticated users."""
        client = Client()
        response = client.get(reverse("subscriber_list"))
        assert response.status_code == 302


@pytest.mark.django_db
class TestAddSubscriberView:
    """Add subscriber view tests. After staff user login."""

    @pytest.fixture
    def staff_user(self):
        """Staff user fixture."""
        return User.objects.create_user(
            username="staff", password="pass123", is_staff=True
        )

    def test_add_subscriber_get(self, staff_user):
        """Test GET request to add subscriber view."""
        client = Client()
        client.login(username="staff", password="pass123")
        response = client.get(reverse("add_subscriber"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_add_subscriber_post(self, staff_user):
        """Test POST request to add subscriber view."""
        client = Client()
        client.login(username="staff", password="pass123")
        data = {
            "email": "new@example.com",
            "status": Subscriber.Status.ACTIVE,
        }
        client.post(reverse("add_subscriber"), data)
        assert Subscriber.objects.filter(email="new@example.com").exists()
