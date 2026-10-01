from unittest.mock import patch

import pytest

from core_apps.profiles.models import Profile
from core_apps.profiles.pipeline import save_profile
from core_apps.users.models import User


@pytest.mark.django_db
def test_save_profile_google_oauth_with_avatar():
    user = User.objects.create_user(
        username="googleuser",
        email="googleuser@example.com",
        password="TestPassword123!",
    )

    backend = type("Backend", (), {"name": "google-oauth2"})()

    response = {
        "picture": "https://example.com/avatar.jpg",
    }

    with patch(
        "core_apps.profiles.pipeline.cloudinary.uploader.upload"
    ) as mock_upload:
        mock_upload.return_value = {
            "public_id": "avatars/googleuser",
        }

        save_profile(
            backend=backend,
            user=user,
            response=response,
        )

    mock_upload.assert_called_once_with(
        "https://example.com/avatar.jpg"
    )

    profile = Profile.objects.get(user=user)

    assert str(profile.avatar) == "avatars/googleuser"

@pytest.mark.django_db
def test_save_profile_google_oauth_without_avatar():
    user = User.objects.create_user(
        username="googleuser2",
        email="googleuser2@example.com",
        password="TestPassword123!",
    )

    backend = type("Backend", (), {"name": "google-oauth2"})()

    response = {}

    with patch(
        "core_apps.profiles.pipeline.cloudinary.uploader.upload"
    ) as mock_upload:
        save_profile(
            backend=backend,
            user=user,
            response=response,
        )

    mock_upload.assert_not_called()
    profile = Profile.objects.get(user=user)
    assert profile.user == user
    assert not profile.avatar

@pytest.mark.django_db
def test_save_profile_non_google_backend():
    user = User.objects.create_user(
        username="otheruser",
        email="otheruser@example.com",
        password="TestPassword123!",
    )

    profile = user.profile

    backend = type("Backend", (), {"name": "facebook"})()

    response = {
        "picture": "https://example.com/avatar.jpg",
    }

    with patch(
        "core_apps.profiles.pipeline.cloudinary.uploader.upload"
    ) as mock_upload:
        save_profile(
            backend=backend,
            user=user,
            response=response,
        )

    mock_upload.assert_not_called()

    profile.refresh_from_db()

    assert not profile.avatar