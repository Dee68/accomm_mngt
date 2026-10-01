import pytest
from django.contrib.auth import get_user_model

from core_apps.profiles.models import Profile

from core_apps.ratings.models import Rating

from django.db import IntegrityError


User = get_user_model()


@pytest.mark.django_db
def test_profile_is_created_with_user_and_defaults():
    user = User.objects.create_user(
        username="profileuser",
        email="profile@example.com",
        password="TestPassword123!",
        first_name="Profile",
        last_name="User",
    )

    profile = user.profile

    assert isinstance(profile, Profile)
    assert profile.user == user
    assert profile.gender == Profile.Gender.MALE
    assert profile.occupation == Profile.Occupation.TENANT
    assert profile.phone_number == "+353877800112"
    assert profile.country_field == "IE"
    assert profile.city_of_origin == "Dublin"
    assert profile.report_count == 0
    assert profile.reputation == 100

@pytest.mark.django_db
def test_profile_is_banned_based_on_report_count():
    user = User.objects.create_user(
        username="banuser",
        email="ban@example.com",
        password="TestPassword123!",
        first_name="Ban",
        last_name="User",
    )

    profile = user.profile

    profile.report_count = 4
    assert profile.is_banned is False

    profile.report_count = 5
    assert profile.is_banned is True

    profile.report_count = 6
    assert profile.is_banned is True

@pytest.mark.django_db
def test_profile_update_reputation():
    user = User.objects.create_user(
        username="reputationuser",
        email="reputation@example.com",
        password="TestPassword123!",
        first_name="Reputation",
        last_name="User",
    )

    profile = user.profile

    test_cases = [
        (0, 100),
        (1, 80),
        (2, 60),
        (3, 40),
        (4, 20),
        (5, 0),
        (10, 0),
    ]

    for report_count, expected_reputation in test_cases:
        profile.report_count = report_count
        profile.update_reputation()

        assert profile.reputation == expected_reputation

@pytest.mark.django_db
def test_profile_save_updates_reputation():
    user = User.objects.create_user(
        username="saveuser",
        email="save@example.com",
        password="TestPassword123!",
        first_name="Save",
        last_name="User",
    )

    profile = user.profile

    profile.report_count = 3
    profile.reputation = 999

    profile.save()

    profile.refresh_from_db()

    assert profile.report_count == 3
    assert profile.reputation == 40

@pytest.mark.django_db
def test_profile_slug_is_generated_from_username():
    user = User.objects.create_user(
        username="john.doe",
        email="john@example.com",
        password="TestPassword123!",
        first_name="John",
        last_name="Doe",
    )

    profile = user.profile

    assert profile.slug == "johndoe"

@pytest.mark.django_db
def test_profile_slug_must_be_unique():
    user1 = User.objects.create_user(
        username="firstuser",
        email="first@example.com",
        password="TestPassword123!",
        first_name="First",
        last_name="User",
    )

    user2 = User.objects.create_user(
        username="seconduser",
        email="second@example.com",
        password="TestPassword123!",
        first_name="Second",
        last_name="User",
    )

    profile1 = user1.profile
    profile2 = user2.profile

    profile2.slug = profile1.slug

    with pytest.raises(IntegrityError):
        Profile.objects.filter(pk=profile2.pk).update(
            slug=profile1.slug
        )

@pytest.mark.django_db
def test_profile_average_rating_returns_zero_without_ratings():
    user = User.objects.create_user(
        username="noratings",
        email="noratings@example.com",
        password="TestPassword123!",
        first_name="No",
        last_name="Ratings",
    )

    profile = user.profile

    assert profile.get_average_rating() == 0.0

@pytest.mark.django_db
def test_profile_average_rating_returns_correct_average():
    rated_user = User.objects.create_user(
        username="rateduser",
        email="rated@example.com",
        password="TestPassword123!",
        first_name="Rated",
        last_name="User",
    )

    rating_user1 = User.objects.create_user(
        username="ratinguser1",
        email="rating1@example.com",
        password="TestPassword123!",
        first_name="Rating",
        last_name="User One",
    )

    rating_user2 = User.objects.create_user(
        username="ratinguser2",
        email="rating2@example.com",
        password="TestPassword123!",
        first_name="Rating",
        last_name="User Two",
    )

    Rating.objects.create(
        rated_user=rated_user,
        rating_user=rating_user1,
        rating=4,
    )

    Rating.objects.create(
        rated_user=rated_user,
        rating_user=rating_user2,
        rating=5,
    )

    profile = rated_user.profile

    assert profile.get_average_rating() == 4.5