import pytest

from core_apps.ratings.models import Rating
from core_apps.ratings.serializers import RatingSerializer
from core_apps.users.models import User


@pytest.mark.django_db
def test_rating_serializer_accepts_rated_user_username():

    data = {
        "rated_user_username": "rateduser",
        "rating": 5,
        "comment": "Excellent!",
    }

    serializer = RatingSerializer(data=data)

    assert serializer.is_valid()

    assert serializer.validated_data["rated_user_username"] == "rateduser"


@pytest.mark.django_db
def test_rating_serializer_creates_rating():

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

    data = {
        "rated_user_username": "rateduser",
        "rating": 5,
        "comment": "Excellent!",
    }

    serializer = RatingSerializer(data=data)

    assert serializer.is_valid()

    rating = serializer.save(
        rated_user=rated_user,
        rating_user=rating_user,
    )

    assert rating.rated_user == rated_user
    assert rating.rating_user == rating_user
    assert rating.rating == 5
    assert rating.comment == "Excellent!"


@pytest.mark.django_db
def test_rating_serializer_id_is_read_only():

    data = {
        "id": 999,
        "rated_user_username": "rateduser",
        "rating": 4,
        "comment": "Good.",
    }

    serializer = RatingSerializer(data=data)

    assert serializer.is_valid()

    assert "id" not in serializer.validated_data


@pytest.mark.django_db
def test_rating_serializer_output_fields():

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
        comment="Good tenant.",
    )

    serializer = RatingSerializer(rating)

    assert set(serializer.data.keys()) == {
        "id",
        "rating",
        "comment",
    }

    assert serializer.data["rating"] == 4
    assert serializer.data["comment"] == "Good tenant."