"""Tests for user profile model."""

import pytest
import pytest
from django.contrib.auth.models import User
from .models import UserProfile


@pytest.mark.django_db
class TestUserProfileModel:
    """User profile model tests."""

    @pytest.fixture
    def user(self):
        """Fixture for creating a user."""
        return User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

    def test_user_profile_auto_creation(self, user):
        """Test user profile creation on user create."""
        profile = user.userprofile
        assert profile.user == user
        assert profile.default_phone_number == ""

    def test_user_profile_update_fields(self, user):
        """Test user profile update fields."""
        profile = user.userprofile
        profile.default_phone_number = "1234567890"
        profile.default_street_address1 = "123 Main St"
        profile.default_street_address2 = "Apt 4B"
        profile.default_town_or_city = "New York"
        profile.default_postcode = "10001"
        profile.default_country = "US"
        profile.save()
        profile.refresh_from_db()
        assert profile.default_phone_number == "1234567890"
        assert profile.default_street_address1 == "123 Main St"

    def test_user_profile_blank_fields(self, user):
        """User profile with blank fields."""
        profile = user.userprofile
        assert profile.default_phone_number == ""
        assert profile.default_street_address1 == ""

    def test_user_profile_one_to_one(self, user):
        """Test user profile creation on user create."""
        profile = user.userprofile
        assert profile is not None
        with pytest.raises(Exception):
            UserProfile.objects.create(user=user)

    def test_user_profile_cascade_delete(self):
        """Test user profile deletion on user delete."""
        user = User.objects.create_user(
            username="deletetest",
            password="pass123"
        )
        profile = user.userprofile
        profile_id = profile.id
        user.delete()
        with pytest.raises(UserProfile.DoesNotExist):
            UserProfile.objects.get(id=profile_id)
