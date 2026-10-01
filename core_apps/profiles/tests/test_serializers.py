import pytest
from unittest.mock import patch

from io import BytesIO

from PIL import Image

from django.contrib.auth import get_user_model

from core_apps.profiles.models import Profile
from core_apps.ratings.models import Rating
from core_apps.apartments.models import Apartment

from core_apps.profiles.serializers import (
    ProfileSerializer,
    UpdateProfileSerializer,
    AvatarUploadSerializer
)

from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


@pytest.mark.django_db
def test_profile_serializer_returns_profile_and_user_fields():
    user = User.objects.create_user(
        username="serializeruser",
        email="serializer@example.com",
        password="TestPassword123!",
        first_name="John",
        last_name="Doe",
    )

    profile = user.profile

    serializer = ProfileSerializer(profile)
    data = serializer.data

    assert data["id"] == str(profile.id)
    assert data["slug"] == profile.slug
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["full_name"] == "John Doe"
    assert data["username"] == "serializeruser"
    assert data["gender"] == Profile.Gender.MALE
    assert data["country_field"] == "IE"
    assert data["city_of_origin"] == "Dublin"
    assert data["reputation"] == 100

@pytest.mark.django_db
def test_profile_serializer_returns_average_rating():
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

    serializer = ProfileSerializer(rated_user.profile)

    assert serializer.data["average_rating"] == 4.5

@pytest.mark.django_db
def test_profile_serializer_returns_none_when_avatar_is_not_set():
    user = User.objects.create_user(
        username="noavatar",
        email="noavatar@example.com",
        password="TestPassword123!",
        first_name="No",
        last_name="Avatar",
    )

    serializer = ProfileSerializer(user.profile)

    assert serializer.data["avatar"] is None

@pytest.mark.django_db
def test_profile_serializer_returns_avatar_url():
    user = User.objects.create_user(
        username="avataruser",
        email="avatar@example.com",
        password="TestPassword123!",
        first_name="Avatar",
        last_name="User",
    )

    profile = user.profile

    image_file = BytesIO()

    Image.new("RGB", (1, 1), color="white").save(
        image_file,
        format="JPEG",
    )

    image_file.seek(0)

    image = SimpleUploadedFile(
        "avatar.jpg",
        image_file.getvalue(),
        content_type="image/jpeg",
    )

    with patch("cloudinary.uploader.upload") as mock_upload:
        mock_upload.return_value = {
            "public_id": "avatars/test-avatar",
            "version": 123456,
            "format": "jpg",
            "type": "upload",
            "resource_type": "image",
        }

        profile.avatar = image
        profile.save()
    profile.refresh_from_db()

    serializer = ProfileSerializer(profile)

    assert serializer.data["avatar"] is not None

@pytest.mark.django_db
def test_profile_serializer_returns_none_when_user_has_no_apartment():
    user = User.objects.create_user(
        username="noapartment",
        email="noapartment@example.com",
        password="TestPassword123!",
        first_name="No",
        last_name="Apartment",
    )

    serializer = ProfileSerializer(user.profile)

    assert serializer.data["apartment"] is None

@pytest.mark.django_db
def test_profile_serializer_returns_user_apartment():
    user = User.objects.create_user(
        username="tenantuser",
        email="tenant@example.com",
        password="TestPassword123!",
        first_name="Tenant",
        last_name="User",
    )

    apartment = Apartment.objects.create(
        unit_number="A101",
        building="Main Building",
        floor=1,
        tenant=user,
    )

    serializer = ProfileSerializer(user.profile)
    apartment_data = serializer.data["apartment"]

    assert apartment_data is not None
    assert apartment_data["id"] == str(apartment.id)
    assert apartment_data["unit_number"] == "A101"
    assert apartment_data["building"] == "Main Building"
    assert apartment_data["floor"] == 1
    assert "tenant" not in apartment_data

@pytest.mark.django_db
def test_update_profile_serializer_accepts_valid_data():
    user = User.objects.create_user(
        username="updateuser",
        email="update@example.com",
        password="TestPassword123!",
        first_name="Old",
        last_name="Name",
    )

    profile = user.profile

    serializer = UpdateProfileSerializer(
        profile,
        data={
            "first_name": "New",
            "last_name": "Name",
            "username": "newusername",
            "gender": Profile.Gender.FEMALE,
            "country_field": "IE",
            "city_of_origin": "Cork",
            "bio": "Updated profile bio",
            "occupation": Profile.Occupation.PLUMBER,
            "phone_number": "+353871234567",
        },
    )

    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_update_profile_serializer_updates_profile_and_user():
    user = User.objects.create_user(
        username="updateuser2",
        email="update2@example.com",
        password="TestPassword123!",
        first_name="Old",
        last_name="Name",
    )

    profile = user.profile

    serializer = UpdateProfileSerializer(
        profile,
        data={
            "first_name": "New",
            "last_name": "Name",
            "username": "newusername",
            "gender": Profile.Gender.FEMALE,
            "country_field": "IE",
            "city_of_origin": "Cork",
            "bio": "Updated profile bio",
            "occupation": Profile.Occupation.PLUMBER,
            "phone_number": "+353871234567",
        },
    )

    assert serializer.is_valid(), serializer.errors
    serializer.save()

    user.refresh_from_db()
    profile.refresh_from_db()

    assert user.first_name == "New"
    assert user.last_name == "Name"
    assert user.username == "newusername"

    assert profile.gender == Profile.Gender.FEMALE
    assert profile.country_field == "IE"
    assert profile.city_of_origin == "Cork"
    assert profile.bio == "Updated profile bio"
    assert profile.occupation == Profile.Occupation.PLUMBER
    assert str(profile.phone_number) == "+353871234567"

@pytest.mark.django_db
def test_avatar_upload_serializer_accepts_valid_image():
    user = User.objects.create_user(
        username="avatarupload",
        email="avatarupload@example.com",
        password="TestPassword123!",
    )
    profile = user.profile

    image_file = BytesIO()

    Image.new("RGB", (1, 1), color="white").save(
        image_file,
        format="JPEG",
    )

    image_file.seek(0)

    image_file = BytesIO()

    Image.new("RGB", (1, 1), color="white").save(
        image_file,
        format="JPEG",
    )

    image_file.seek(0)

    image_file = BytesIO()

    Image.new("RGB", (1, 1), color="white").save(
        image_file,
        format="JPEG",
    )

    image_file.seek(0)

    image = SimpleUploadedFile(
        "avatar.jpg",
        image_file.getvalue(),
        content_type="image/jpeg",
    )
    serializer = AvatarUploadSerializer(
        profile,
        data={"avatar": image},
    )

    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_avatar_upload_serializer_saves_avatar():
    user = User.objects.create_user(
        username="avatarupload2",
        email="avatarupload2@example.com",
        password="TestPassword123!",
    )
    profile = user.profile

    image_file = BytesIO()

    Image.new("RGB", (1, 1), color="white").save(
        image_file,
        format="JPEG",
    )

    image_file.seek(0)

    image = SimpleUploadedFile(
        "avatar.jpg",
        image_file.getvalue(),
        content_type="image/jpeg",
    )

    with patch("cloudinary.uploader.upload") as mock_upload:
        mock_upload.return_value = {
            "public_id": "avatars/avatarupload2",
            "version": 123456,
            "format": "jpg",
            "type": "upload",
            "resource_type": "image",
        }

        serializer = AvatarUploadSerializer(
            profile,
            data={"avatar": image},
        )

        assert serializer.is_valid(), serializer.errors
        serializer.save()

    profile.refresh_from_db()

    assert profile.avatar is not None