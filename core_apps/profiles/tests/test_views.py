import pytest

from io import BytesIO
from PIL import Image
from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from core_apps.profiles.models import Profile

from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


@pytest.mark.django_db
def test_profile_list_returns_tenant_profiles_only():
    client = APIClient()

    tenant = User.objects.create_user(
        username="tenant",
        email="tenant@example.com",
        password="TestPassword123!",
    )

    client.force_authenticate(user=tenant)

    non_tenant = User.objects.create_user(
        username="worker",
        email="worker@example.com",
        password="TestPassword123!",
    )
    non_tenant.profile.occupation = Profile.Occupation.PLUMBER
    non_tenant.profile.save()

    staff = User.objects.create_user(
        username="staff",
        email="staff@example.com",
        password="TestPassword123!",
        is_staff=True,
    )

    superuser = User.objects.create_superuser(
        username="superuser",
        email="superuser@example.com",
        password="TestPassword123!",
    )

    response = client.get("/api/v1/profiles/all/")

    assert response.status_code == 200
    #print(response.data)

    data = response.data

    usernames = [
        profile["username"]
        for profile in data["results"]
    ]

    assert "tenant" in usernames
    assert "worker" not in usernames
    assert "staff" not in usernames
    assert "superuser" not in usernames

@pytest.mark.django_db
def test_profile_list_searches_by_user_name():
    client = APIClient()

    user1 = User.objects.create_user(
        username="john",
        email="john@example.com",
        password="TestPassword123!",
        first_name="John",
        last_name="Smith",
    )

    User.objects.create_user(
        username="jane",
        email="jane@example.com",
        password="TestPassword123!",
        first_name="Jane",
        last_name="Doe",
    )

    client.force_authenticate(user=user1)

    response = client.get(
        "/api/v1/profiles/all/",
        {"search": "John"},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["username"] == "john"

@pytest.mark.django_db
def test_profile_list_filters_by_occupation():
    client = APIClient()

    tenant = User.objects.create_user(
        username="tenantfilter",
        email="tenantfilter@example.com",
        password="TestPassword123!",
    )

    plumber = User.objects.create_user(
        username="plumberfilter",
        email="plumberfilter@example.com",
        password="TestPassword123!",
    )
    plumber.profile.occupation = Profile.Occupation.PLUMBER
    plumber.profile.save()

    client.force_authenticate(user=tenant)

    response = client.get(
        "/api/v1/profiles/all/",
        {"occupation": Profile.Occupation.TENANT},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["username"] == "tenantfilter"

@pytest.mark.django_db
def test_profile_list_filters_by_gender():
    client = APIClient()

    male_user = User.objects.create_user(
        username="malefilter",
        email="malefilter@example.com",
        password="TestPassword123!",
    )

    female_user = User.objects.create_user(
        username="femalefilter",
        email="femalefilter@example.com",
        password="TestPassword123!",
    )
    female_user.profile.gender = Profile.Gender.FEMALE
    female_user.profile.save()

    client.force_authenticate(user=male_user)

    response = client.get(
        "/api/v1/profiles/all/",
        {"gender": Profile.Gender.FEMALE},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["username"] == "femalefilter"

@pytest.mark.django_db
def test_profile_list_filters_by_country():
    client = APIClient()

    ireland_user = User.objects.create_user(
        username="irelandfilter",
        email="irelandfilter@example.com",
        password="TestPassword123!",
    )

    uk_user = User.objects.create_user(
        username="ukfilter",
        email="ukfilter@example.com",
        password="TestPassword123!",
    )
    uk_user.profile.country_field = "GB"
    uk_user.profile.save()

    client.force_authenticate(user=ireland_user)

    response = client.get(
        "/api/v1/profiles/all/",
        {"country_field": "GB"},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["username"] == "ukfilter"

@pytest.mark.django_db
def test_profile_list_is_paginated():
    client = APIClient()

    users = []

    for i in range(10):
        user = User.objects.create_user(
            username=f"pagination{i}",
            email=f"pagination{i}@example.com",
            password="TestPassword123!",
        )
        users.append(user)

    client.force_authenticate(user=users[0])

    response = client.get("/api/v1/profiles/all/")

    assert response.status_code == 200
    assert response.data["count"] == 10
    assert len(response.data["results"]) == 9
    assert response.data["next"] is not None
    assert response.data["previous"] is None

@pytest.mark.django_db
def test_profile_detail_returns_authenticated_users_profile():
    client = APIClient()

    user = User.objects.create_user(
        username="detailuser",
        email="detail@example.com",
        password="TestPassword123!",
        first_name="Detail",
        last_name="User",
    )

    client.force_authenticate(user=user)

    response = client.get("/api/v1/profiles/user/my-profile/")

    assert response.status_code == 200
    assert response.data["username"] == "detailuser"
    assert response.data["first_name"] == "Detail"
    assert response.data["last_name"] == "User"
    assert response.data["id"] == str(user.profile.id)

@pytest.mark.django_db
def test_profile_detail_requires_authentication():
    client = APIClient()

    response = client.get("/api/v1/profiles/user/my-profile/")

    assert response.status_code == 401

@pytest.mark.django_db
def test_profile_detail_returns_authenticated_users_profile_only():
    client = APIClient()

    first_user = User.objects.create_user(
        username="firstuser",
        email="first@example.com",
        password="TestPassword123!",
        first_name="First",
        last_name="User",
    )

    second_user = User.objects.create_user(
        username="seconduser",
        email="second@example.com",
        password="TestPassword123!",
        first_name="Second",
        last_name="User",
    )

    client.force_authenticate(user=second_user)

    response = client.get("/api/v1/profiles/user/my-profile/")

    assert response.status_code == 200
    assert response.data["username"] == "seconduser"
    assert response.data["first_name"] == "Second"
    assert response.data["id"] == str(second_user.profile.id)
    assert response.data["id"] != str(first_user.profile.id)

@pytest.mark.django_db
def test_profile_update_updates_authenticated_users_profile():
    client = APIClient()

    user = User.objects.create_user(
        username="viewupdate",
        email="viewupdate@example.com",
        password="TestPassword123!",
        first_name="Old",
        last_name="Name",
    )

    client.force_authenticate(user=user)

    response = client.patch(
        "/api/v1/profiles/user/update/",
        {
            "first_name": "Updated",
            "last_name": "User",
            "username": "updatedusername",
            "gender": Profile.Gender.FEMALE,
            "country_field": "IE",
            "city_of_origin": "Cork",
            "bio": "Updated through the view",
            "occupation": Profile.Occupation.PLUMBER,
            "phone_number": "+353871234567",
        },
        format="json",
    )

    assert response.status_code == 200

    user.refresh_from_db()
    profile = user.profile
    profile.refresh_from_db()

    assert user.first_name == "Updated"
    assert user.last_name == "User"
    assert user.username == "updatedusername"
    assert profile.gender == Profile.Gender.FEMALE
    assert profile.country_field == "IE"
    assert profile.city_of_origin == "Cork"
    assert profile.bio == "Updated through the view"
    assert profile.occupation == Profile.Occupation.PLUMBER
    assert str(profile.phone_number) == "+353871234567"

@pytest.mark.django_db
def test_profile_update_requires_authentication():
    client = APIClient()

    response = client.patch(
        "/api/v1/profiles/user/update/",
        {
            "first_name": "Updated",
        },
        format="json",
    )

    assert response.status_code == 401

@pytest.mark.django_db
def test_avatar_upload_starts_successfully():
    client = APIClient()

    user = User.objects.create_user(
        username="avatarview",
        email="avatarview@example.com",
        password="TestPassword123!",
    )

    client.force_authenticate(user=user)

    image_file = BytesIO()
    Image.new("RGB", (1, 1), color="white").save(
        image_file,
        format="JPEG",
    )
    image_file.seek(0)

    image = SimpleUploadedFile(
        "avatar.jpg",
        image_file.read(),
        content_type="image/jpeg",
    )

    with patch(
        "core_apps.profiles.views.upload_avatar_to_cloudinary.delay"
    ) as mock_delay:
        response = client.patch(
            "/api/v1/profiles/user/avatar/",
            {"avatar": image},
            format="multipart",
        )

    assert response.status_code == 202
    assert response.data["message"] == "Avatar upload started"

    mock_delay.assert_called_once()

    args = mock_delay.call_args.args
    image_content = image_file.getvalue()

    assert args[0] == str(user.profile.id)
    assert args[1] == image_content

@pytest.mark.django_db
def test_avatar_upload_rejects_invalid_data():
    client = APIClient()

    user = User.objects.create_user(
        username="invalidavatar",
        email="invalidavatar@example.com",
        password="TestPassword123!",
    )

    client.force_authenticate(user=user)

    with patch(
        "core_apps.profiles.views.upload_avatar_to_cloudinary.delay"
    ) as mock_delay:
        response = client.patch(
            "/api/v1/profiles/user/avatar/",
            {"avatar": ""},
            format="multipart",
        )

    assert response.status_code == 400
    assert "avatar" in response.data
    mock_delay.assert_not_called()

@pytest.mark.django_db
def test_avatar_upload_rejects_invalid_file():
    client = APIClient()

    user = User.objects.create_user(
        username="invalidfileavatar",
        email="invalidfileavatar@example.com",
        password="TestPassword123!",
    )

    client.force_authenticate(user=user)

    invalid_file = SimpleUploadedFile(
        "avatar.txt",
        b"this is not an image",
        content_type="text/plain",
    )

    with patch(
        "core_apps.profiles.views.upload_avatar_to_cloudinary.delay"
    ) as mock_delay:
        response = client.patch(
            "/api/v1/profiles/user/avatar/",
            {"avatar": invalid_file},
            format="multipart",
        )

    assert response.status_code == 400
    assert "avatar" in response.data
    mock_delay.assert_not_called()

@pytest.mark.django_db
def test_avatar_upload_requires_authentication():
    client = APIClient()

    image = SimpleUploadedFile(
        "avatar.jpg",
        b"fake-image-content",
        content_type="image/jpeg",
    )

    with patch(
        "core_apps.profiles.views.upload_avatar_to_cloudinary.delay"
    ) as mock_delay:
        response = client.patch(
            "/api/v1/profiles/user/avatar/",
            {"avatar": image},
            format="multipart",
        )

    assert response.status_code == 401
    mock_delay.assert_not_called()

@pytest.mark.django_db
def test_non_tenant_profile_list_returns_non_tenant_profiles_only():
    client = APIClient()

    tenant = User.objects.create_user(
        username="tenantuser",
        email="tenant@example.com",
        password="TestPassword123!",
    )

    plumber = User.objects.create_user(
        username="plumberuser",
        email="plumber@example.com",
        password="TestPassword123!",
    )
    plumber.profile.occupation = Profile.Occupation.PLUMBER
    plumber.profile.save()

    electrician = User.objects.create_user(
        username="electricianuser",
        email="electrician@example.com",
        password="TestPassword123!",
    )
    electrician.profile.occupation = Profile.Occupation.ELECTRICIAN
    electrician.profile.save()

    client.force_authenticate(user=tenant)

    response = client.get(
        "/api/v1/profiles/non-tenant-profiles/"
    )

    assert response.status_code == 200
    assert response.data["count"] == 2
    assert len(response.data["results"]) == 2

    usernames = {
        profile["username"]
        for profile in response.data["results"]
    }

    assert "plumberuser" in usernames
    assert "electricianuser" in usernames
    assert "tenantuser" not in usernames

@pytest.mark.django_db
def test_non_tenant_profile_list_excludes_staff_and_superusers():
    client = APIClient()

    regular_user = User.objects.create_user(
        username="regularuser",
        email="regular@example.com",
        password="TestPassword123!",
    )
    regular_user.profile.occupation = Profile.Occupation.PLUMBER
    regular_user.profile.save()

    staff_user = User.objects.create_user(
        username="staffuser",
        email="staff@example.com",
        password="TestPassword123!",
        is_staff=True,
    )
    staff_user.profile.occupation = Profile.Occupation.PLUMBER
    staff_user.profile.save()

    superuser = User.objects.create_superuser(
        username="superuser",
        email="superuser@example.com",
        password="TestPassword123!",
    )
    superuser.profile.occupation = Profile.Occupation.ELECTRICIAN
    superuser.profile.save()

    client.force_authenticate(user=regular_user)

    response = client.get(
        "/api/v1/profiles/non-tenant-profiles/"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1

    usernames = {
        profile["username"]
        for profile in response.data["results"]
    }

    assert "regularuser" in usernames
    assert "staffuser" not in usernames
    assert "superuser" not in usernames

@pytest.mark.django_db
def test_non_tenant_profile_list_filters_by_occupation():
    client = APIClient()

    plumber = User.objects.create_user(
        username="plumberfilter",
        email="plumberfilter@example.com",
        password="TestPassword123!",
    )
    plumber.profile.occupation = Profile.Occupation.PLUMBER
    plumber.profile.save()

    electrician = User.objects.create_user(
        username="electricianfilter",
        email="electricianfilter@example.com",
        password="TestPassword123!",
    )
    electrician.profile.occupation = Profile.Occupation.ELECTRICIAN
    electrician.profile.save()

    client.force_authenticate(user=plumber)

    response = client.get(
        "/api/v1/profiles/non-tenant-profiles/",
        {"occupation": Profile.Occupation.PLUMBER},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["username"] == "plumberfilter"

@pytest.mark.django_db
def test_non_tenant_profile_list_filters_by_gender():
    client = APIClient()

    male_user = User.objects.create_user(
        username="malefilter",
        email="malefilter@example.com",
        password="TestPassword123!",
    )
    male_user.profile.gender = Profile.Gender.MALE
    male_user.profile.occupation = Profile.Occupation.PLUMBER
    male_user.profile.save()

    female_user = User.objects.create_user(
        username="femalefilter",
        email="femalefilter@example.com",
        password="TestPassword123!",
    )
    female_user.profile.gender = Profile.Gender.FEMALE
    female_user.profile.occupation = Profile.Occupation.ELECTRICIAN
    female_user.profile.save()

    client.force_authenticate(user=male_user)

    response = client.get(
        "/api/v1/profiles/non-tenant-profiles/",
        {"gender": Profile.Gender.FEMALE},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["username"] == "femalefilter"

@pytest.mark.django_db
def test_non_tenant_profile_list_filters_by_country():
    client = APIClient()

    ireland_user = User.objects.create_user(
        username="irelandfilter",
        email="irelandfilter@example.com",
        password="TestPassword123!",
    )
    ireland_user.profile.country_field = "IE"
    ireland_user.profile.occupation = Profile.Occupation.PLUMBER
    ireland_user.profile.save()

    nigeria_user = User.objects.create_user(
        username="nigeriafilter",
        email="nigeriafilter@example.com",
        password="TestPassword123!",
    )
    nigeria_user.profile.country_field = "NG"
    nigeria_user.profile.occupation = Profile.Occupation.ELECTRICIAN
    nigeria_user.profile.save()

    client.force_authenticate(user=ireland_user)

    response = client.get(
        "/api/v1/profiles/non-tenant-profiles/",
        {"country_field": "NG"},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["username"] == "nigeriafilter"

@pytest.mark.django_db
def test_non_tenant_profile_list_is_paginated():
    client = APIClient()

    users = []

    for i in range(10):
        user = User.objects.create_user(
            username=f"nontenant{i}",
            email=f"nontenant{i}@example.com",
            password="TestPassword123!",
        )
        user.profile.occupation = Profile.Occupation.PLUMBER
        user.profile.save()
        users.append(user)

    client.force_authenticate(user=users[0])

    response = client.get(
        "/api/v1/profiles/non-tenant-profiles/"
    )

    assert response.status_code == 200
    assert response.data["count"] == 10
    assert len(response.data["results"]) == 9
    assert response.data["next"] is not None
    assert response.data["previous"] is None

@pytest.mark.django_db
def test_non_tenant_profile_list_searches_by_user_name():
    client = APIClient()

    john = User.objects.create_user(
        username="johnplumber",
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        password="TestPassword123!",
    )
    john.profile.occupation = Profile.Occupation.PLUMBER
    john.profile.save()

    peter = User.objects.create_user(
        username="peterelectrician",
        first_name="Peter",
        last_name="Jones",
        email="peter@example.com",
        password="TestPassword123!",
    )
    peter.profile.occupation = Profile.Occupation.ELECTRICIAN
    peter.profile.save()

    client.force_authenticate(user=john)

    response = client.get(
        "/api/v1/profiles/non-tenant-profiles/",
        {"search": "John"},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["username"] == "johnplumber"

@pytest.mark.django_db
def test_profile_list_requires_authentication():
    client = APIClient()

    response = client.get("/api/v1/profiles/all/")

    assert response.status_code == 401