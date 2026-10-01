import pytest

from core_apps.profiles.models import Profile
from core_apps.users.models import User


@pytest.mark.django_db
def test_create_user_profile_creates_profile():
    user = User.objects.create_user(
        username="signaluser",
        email="signaluser@example.com",
        password="TestPassword123!",
    )

    profile = Profile.objects.get(user=user)

    assert profile.user == user

@pytest.mark.django_db
def test_create_user_profile_does_not_create_duplicate_profile():
    user = User.objects.create_user(
        username="existinguser",
        email="existinguser@example.com",
        password="TestPassword123!",
    )

    profile = user.profile

    user.first_name = "Updated"
    user.save()

    assert Profile.objects.filter(user=user).count() == 1
    assert Profile.objects.get(user=user).pk == profile.pk