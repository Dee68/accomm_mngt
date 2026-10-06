import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model

from core_apps.ratings.admin import RatingAdmin
from core_apps.ratings.models import Rating
from core_apps.profiles.models import Profile

User = get_user_model()


def test_rating_is_registered_with_admin():
    assert Rating in admin.site._registry
    assert isinstance(admin.site._registry[Rating], RatingAdmin)


def test_rating_admin_list_display():
    assert RatingAdmin.list_display == [
        "rated_user",
        "rating_user",
        "comment",
        "rating",
        "get_average_rating",
    ]


def test_rating_admin_search_fields():
    assert RatingAdmin.search_fields == [
        "rated_user__username",
        "rating_user__username",
    ]


def test_rating_admin_list_filter():
    assert RatingAdmin.list_filter == ["rating", "created_at"]


def test_get_average_rating_short_description():
    assert RatingAdmin.get_average_rating.short_description == "Average Rating"


@pytest.mark.django_db
def test_get_queryset_annotates_average_rating():
    rated_user = User.objects.create_user(
        username="rated",
        email="rated@example.com",
        password="TestPassword123!",
    )
    rated_user.profile.occupation = Profile.Occupation.PLUMBER
    rated_user.profile.save()

    rater = User.objects.create_user(
        username="rater",
        email="rater@example.com",
        password="TestPassword123!",
    )

    Rating.objects.create(rated_user=rated_user, rating_user=rater, rating=4)

    admin_instance = RatingAdmin(Rating, admin.site)
    queryset = admin_instance.get_queryset(None)

    assert queryset.exists()
    assert hasattr(queryset.first(), "average_rating")


@pytest.mark.django_db
def test_get_average_rating_returns_rounded_average():
    rated_user = User.objects.create_user(
        username="rated",
        email="rated@example.com",
        password="TestPassword123!",
    )
    rated_user.profile.occupation = Profile.Occupation.PLUMBER
    rated_user.profile.save()

    rater1 = User.objects.create_user(
        username="rater1",
        email="rater1@example.com",
        password="TestPassword123!",
    )
    rater2 = User.objects.create_user(
        username="rater2",
        email="rater2@example.com",
        password="TestPassword123!",
    )

    Rating.objects.create(rated_user=rated_user, rating_user=rater1, rating=4)
    Rating.objects.create(rated_user=rated_user, rating_user=rater2, rating=5)

    admin_instance = RatingAdmin(Rating, admin.site)
    rating = admin_instance.get_queryset(None).first()

    assert admin_instance.get_average_rating(rating) == 4.5


@pytest.mark.django_db
def test_get_average_rating_rounds_to_two_decimals():
    rated_user = User.objects.create_user(
        username="rated",
        email="rated@example.com",
        password="TestPassword123!",
    )
    rated_user.profile.occupation = Profile.Occupation.PLUMBER
    rated_user.profile.save()

    # Create three raters giving 5, 4, 4 → average 4.333... → should round to 4.33
    for i, score in enumerate([5, 4, 4]):
        rater = User.objects.create_user(
            username=f"rater{i}",
            email=f"rater{i}@example.com",
            password="TestPassword123!",
        )
        Rating.objects.create(rated_user=rated_user, rating_user=rater, rating=score)

    admin_instance = RatingAdmin(Rating, admin.site)
    rating = admin_instance.get_queryset(None).first()

    assert admin_instance.get_average_rating(rating) == 4.33