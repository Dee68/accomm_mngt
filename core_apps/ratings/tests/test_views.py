# core_apps/ratings/tests/test_views.py
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from core_apps.profiles.models import Profile
from core_apps.ratings.models import Rating

User = get_user_model()


@pytest.mark.django_db
def test_tenant_can_rate_technician():
    tenant = User.objects.create_user(
        username="tenant", email="tenant@example.com", password="TestPassword123!",
    )
    technician = User.objects.create_user(
        username="plumber", email="plumber@example.com", password="TestPassword123!",
    )
    technician.profile.occupation = Profile.Occupation.PLUMBER
    technician.profile.save()

    client = APIClient()
    client.force_authenticate(user=tenant)

    response = client.post(
        "/api/v1/ratings/create/",
        {
            "rated_user_username": technician.username,
            "rating": 5,
            "comment": "Great work",
        },
        format="json",
    )

    assert response.status_code == 201
    assert Rating.objects.filter(rated_user=technician, rating_user=tenant).exists()


@pytest.mark.django_db
def test_tenant_cannot_rate_another_tenant():
    tenant1 = User.objects.create_user(
        username="tenant1", email="t1@example.com", password="TestPassword123!",
    )
    tenant2 = User.objects.create_user(
        username="tenant2", email="t2@example.com", password="TestPassword123!",
    )

    client = APIClient()
    client.force_authenticate(user=tenant1)

    response = client.post(
        "/api/v1/ratings/create/",
        {"rated_user_username": tenant2.username, "rating": 5},
        format="json",
    )

    assert response.status_code == 403
    assert not Rating.objects.filter(rated_user=tenant2).exists()


@pytest.mark.django_db
def test_user_cannot_rate_themselves():
    tenant = User.objects.create_user(
        username="tenant", email="tenant@example.com", password="TestPassword123!",
    )

    client = APIClient()
    client.force_authenticate(user=tenant)

    response = client.post(
        "/api/v1/ratings/create/",
        {"rated_user_username": tenant.username, "rating": 5},
        format="json",
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_technician_cannot_rate_anyone():
    plumber = User.objects.create_user(
        username="plumber", email="plumber@example.com", password="TestPassword123!",
    )
    plumber.profile.occupation = Profile.Occupation.PLUMBER
    plumber.profile.save()

    electrician = User.objects.create_user(
        username="electrician", email="electrician@example.com", password="TestPassword123!",
    )
    electrician.profile.occupation = Profile.Occupation.ELECTRICIAN
    electrician.profile.save()

    client = APIClient()
    client.force_authenticate(user=plumber)

    response = client.post(
        "/api/v1/ratings/create/",
        {"rated_user_username": electrician.username, "rating": 5},
        format="json",
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_rating_nonexistent_user_returns_404():
    tenant = User.objects.create_user(
        username="tenant", email="tenant@example.com", password="TestPassword123!",
    )

    client = APIClient()
    client.force_authenticate(user=tenant)

    response = client.post(
        "/api/v1/ratings/create/",
        {"rated_user_username": "ghost", "rating": 5},
        format="json",
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_duplicate_rating_is_rejected():
    # Only if you added the unique constraint we discussed
    tenant = User.objects.create_user(
        username="tenant", email="tenant@example.com", password="TestPassword123!",
    )
    plumber = User.objects.create_user(
        username="plumber", email="plumber@example.com", password="TestPassword123!",
    )
    plumber.profile.occupation = Profile.Occupation.PLUMBER
    plumber.profile.save()

    client = APIClient()
    client.force_authenticate(user=tenant)

    payload = {"rated_user_username": plumber.username, "rating": 5}

    first = client.post("/api/v1/ratings/create/", payload, format="json")
    second = client.post("/api/v1/ratings/create/", payload, format="json")

    assert first.status_code == 201
    assert second.status_code == 400  # or 403
    assert Rating.objects.filter(rated_user=plumber, rating_user=tenant).count() == 1


@pytest.mark.django_db
def test_unauthenticated_user_cannot_rate():
    client = APIClient()

    response = client.post(
        "/api/v1/ratings/create/",
        {"rated_user_username": "someone", "rating": 5},
        format="json",
    )

    assert response.status_code == 401