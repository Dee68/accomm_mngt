import pytest

from django.db import IntegrityError

from core_apps.ratings.models import Rating

from core_apps.users.models import User


@pytest.mark.django_db
def test_rating_can_be_created():

    rated_user = User.objects.create_user(
        username="rateduser",
        email="rated@example.com",
        password="TestPassword123!",
    )

    rating_user = User.objects.create_user(
        username="ratinguser",
        email="rating@example.com",
        password="TestPassword123!",
    )

    rating = Rating.objects.create(
        rated_user=rated_user,
        rating_user=rating_user,
        rating=5,
        comment="Excellent!",
    )

    assert rating.rated_user == rated_user
    assert rating.rating_user == rating_user
    assert rating.rating == 5
    assert rating.comment == "Excellent!"


@pytest.mark.django_db
def test_rating_string_representation():

    rated_user = User.objects.create_user(
        username="rateduser",
        email="rated@example.com",
        password="TestPassword123!",
    )

    rating_user = User.objects.create_user(
        username="ratinguser",
        email="rating@example.com",
        password="TestPassword123!",
    )

    rating = Rating.objects.create(
        rated_user=rated_user,
        rating_user=rating_user,
        rating=4,
    )

    assert str(rating) == f"{rating_user} rates {rated_user} 4/5"


@pytest.mark.django_db
def test_rating_comment_is_optional():

    rated_user = User.objects.create_user(
        username="rateduser",
        email="rated@example.com",
        password="TestPassword123!",
    )

    rating_user = User.objects.create_user(
        username="ratinguser",
        email="rating@example.com",
        password="TestPassword123!",
    )

    rating = Rating.objects.create(
        rated_user=rated_user,
        rating_user=rating_user,
        rating=3,
    )

    assert rating.comment == ""


def test_rating_choices():

    assert Rating.RatingChoices.ONE == 1
    assert Rating.RatingChoices.TWO == 2
    assert Rating.RatingChoices.THREE == 3
    assert Rating.RatingChoices.FOUR == 4
    assert Rating.RatingChoices.FIVE == 5


@pytest.mark.django_db
def test_duplicate_rating_by_same_user_is_not_allowed():

    rated_user = User.objects.create_user(
        username="rateduser",
        email="rated@example.com",
        password="TestPassword123!",
    )

    rating_user = User.objects.create_user(
        username="ratinguser",
        email="rating@example.com",
        password="TestPassword123!",
    )

    Rating.objects.create(
        rated_user=rated_user,
        rating_user=rating_user,
        rating=5,
    )

    with pytest.raises(IntegrityError):
        Rating.objects.create(
            rated_user=rated_user,
            rating_user=rating_user,
            rating=3,
        )


@pytest.mark.django_db
def test_different_users_can_rate_same_user():

    rated_user = User.objects.create_user(
        username="rateduser",
        email="rated@example.com",
        password="TestPassword123!",
    )

    rating_user_one = User.objects.create_user(
        username="ratinguser1",
        email="rating1@example.com",
        password="TestPassword123!",
    )

    rating_user_two = User.objects.create_user(
        username="ratinguser2",
        email="rating2@example.com",
        password="TestPassword123!",
    )

    Rating.objects.create(
        rated_user=rated_user,
        rating_user=rating_user_one,
        rating=5,
    )

    Rating.objects.create(
        rated_user=rated_user,
        rating_user=rating_user_two,
        rating=4,
    )

    assert Rating.objects.filter(rated_user=rated_user).count() == 2


@pytest.mark.django_db
def test_same_user_can_rate_different_users():

    rating_user = User.objects.create_user(
        username="ratinguser",
        email="rating@example.com",
        password="TestPassword123!",
    )

    rated_user_one = User.objects.create_user(
        username="rateduser1",
        email="rated1@example.com",
        password="TestPassword123!",
    )

    rated_user_two = User.objects.create_user(
        username="rateduser2",
        email="rated2@example.com",
        password="TestPassword123!",
    )

    Rating.objects.create(
        rated_user=rated_user_one,
        rating_user=rating_user,
        rating=5,
    )

    Rating.objects.create(
        rated_user=rated_user_two,
        rating_user=rating_user,
        rating=4,
    )

    assert Rating.objects.filter(rating_user=rating_user).count() == 2