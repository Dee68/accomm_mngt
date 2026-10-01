from unittest.mock import patch

import pytest

from core_apps.profiles.models import Profile
from core_apps.profiles.tasks import (
    upload_avatar_to_cloudinary,
    update_all_reputations,
)
from core_apps.users.models import User


@pytest.mark.django_db
def test_upload_avatar_to_cloudinary():
    user = User.objects.create_user(
        username="avataruser",
        email="avataruser@example.com",
        password="TestPassword123!",
    )

    profile = user.profile
    image_content = b"fake-image-content"

    with patch(
        "core_apps.profiles.tasks.cloudinary.uploader.upload"
    ) as mock_upload:
        mock_upload.return_value = {
            "url": "https://res.cloudinary.com/example/avatar.jpg"
        }

        upload_avatar_to_cloudinary(
            profile.id,
            image_content,
        )

    mock_upload.assert_called_once_with(image_content)

    profile.refresh_from_db()

    assert str(profile.avatar) == (
        "https://res.cloudinary.com/example/avatar"
    )

@pytest.mark.django_db
def test_update_all_reputations():
    user1 = User.objects.create_user(
        username="reputationuser1",
        email="reputationuser1@example.com",
        password="TestPassword123!",
    )

    user2 = User.objects.create_user(
        username="reputationuser2",
        email="reputationuser2@example.com",
        password="TestPassword123!",
    )

    profile1 = user1.profile
    profile2 = user2.profile

    profile1.report_count = 2
    profile1.save()

    profile2.report_count = 4
    profile2.save()

    # Deliberately set incorrect reputations.
    profile1.reputation = 10
    profile1.save(update_fields=["reputation"])

    profile2.reputation = 10
    profile2.save(update_fields=["reputation"])

    update_all_reputations()

    profile1.refresh_from_db()
    profile2.refresh_from_db()

    assert profile1.reputation == 60
    assert profile2.reputation == 20