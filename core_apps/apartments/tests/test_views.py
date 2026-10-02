import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from core_apps.apartments.models import Apartment
from core_apps.apartments.views import ApartmentCreateAPIView, ApartmentDetailAPIView
from core_apps.users.models import User


@pytest.mark.django_db
def test_tenant_can_create_apartment():
    user = User.objects.create_user(
        username="tenantcreator",
        email="tenantcreator@example.com",
        password="TestPassword123!",
    )

    request = APIRequestFactory().post(
        "/apartments/",
        {
            "unit_number": "J1001",
            "building": "Oak House",
            "floor": 10,
        },
        format="json",
    )

    force_authenticate(request, user=user)

    view = ApartmentCreateAPIView.as_view()
    response = view(request)

    assert response.status_code == 201

    apartment = Apartment.objects.get(unit_number="J1001")

    assert apartment.building == "Oak House"
    assert apartment.floor == 10
    assert apartment.tenant == user

from core_apps.profiles.models import Profile


@pytest.mark.django_db
def test_non_tenant_cannot_create_apartment():
    user = User.objects.create_user(
        username="nontenant",
        email="nontenant@example.com",
        password="TestPassword123!",
    )

    user.profile.occupation = Profile.Occupation.PLUMBER
    user.profile.save()

    request = APIRequestFactory().post(
        "/apartments/",
        {
            "unit_number": "K1102",
            "building": "Pine House",
            "floor": 11,
        },
        format="json",
    )

    force_authenticate(request, user=user)

    view = ApartmentCreateAPIView.as_view()
    response = view(request)

    assert response.status_code == 403
    assert response.data["message"] == (
        "You are not allowed to create an apartment,you are not a tenant."
    )

    assert not Apartment.objects.filter(unit_number="K1102").exists()

@pytest.mark.django_db
def test_superuser_can_create_apartment():
    user = User.objects.create_superuser(
        username="admincreator",
        email="admincreator@example.com",
        password="TestPassword123!",
    )

    user.profile.occupation = Profile.Occupation.PLUMBER
    user.profile.save()

    request = APIRequestFactory().post(
        "/apartments/",
        {
            "unit_number": "L1203",
            "building": "Cedar House",
            "floor": 12,
        },
        format="json",
    )

    force_authenticate(request, user=user)

    view = ApartmentCreateAPIView.as_view()
    response = view(request)

    assert response.status_code == 201

    apartment = Apartment.objects.get(unit_number="L1203")

    assert apartment.building == "Cedar House"
    assert apartment.floor == 12
    assert apartment.tenant == user

@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_apartment():
    request = APIRequestFactory().post(
        "/apartments/",
        {
            "unit_number": "M1304",
            "building": "Birch House",
            "floor": 13,
        },
        format="json",
    )

    view = ApartmentCreateAPIView.as_view()
    response = view(request)

    assert response.status_code == 401
    assert not Apartment.objects.filter(unit_number="M1304").exists()

@pytest.mark.django_db
def test_tenant_can_retrieve_own_apartment():
    user = User.objects.create_user(
        username="detailtenant",
        email="detailtenant@example.com",
        password="TestPassword123!",
    )

    apartment = Apartment.objects.create(
        unit_number="N1405",
        building="Oak House",
        floor=14,
        tenant=user,
    )

    request = APIRequestFactory().get(
        f"/apartments/{apartment.pkid}/"
    )

    force_authenticate(request, user=user)

    view = ApartmentDetailAPIView.as_view()
    response = view(request)

    assert response.status_code == 200
    assert response.data["unit_number"] == "N1405"
    assert response.data["building"] == "Oak House"
    assert response.data["floor"] == 14

@pytest.mark.django_db
def test_user_without_apartment_gets_404():
    user = User.objects.create_user(
        username="noapartment",
        email="noapartment@example.com",
        password="TestPassword123!",
    )

    request = APIRequestFactory().get("/apartments/999/")

    force_authenticate(request, user=user)

    view = ApartmentDetailAPIView.as_view()
    response = view(request)

    assert response.status_code == 404

@pytest.mark.django_db
def test_unauthenticated_user_cannot_retrieve_apartment():
    apartment = Apartment.objects.create(
        unit_number="N1501",
        building="Oak House",
        floor=15,
    )

    request = APIRequestFactory().get(
        f"/apartments/{apartment.pkid}/"
    )

    view = ApartmentDetailAPIView.as_view()
    response = view(request)

    assert response.status_code == 401

