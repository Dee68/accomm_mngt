import pytest
from rest_framework.test import APIRequestFactory

from core_apps.apartments.serializers import ApartmentSerializer
from core_apps.apartments.models import Apartment
from core_apps.users.models import User
from rest_framework import serializers


@pytest.mark.django_db
def test_apartment_serializer_fields():
    user = User.objects.create_user(
        username="serializertest",
        email="serializer@example.com",
        password="TestPassword123!",
    )

    request = APIRequestFactory().post("/")
    request.user = user

    serializer = ApartmentSerializer(
        context={"request": request}
    )

    assert set(serializer.fields.keys()) == {
        "id",
        "created_at",
        "unit_number",
        "building",
        "floor",
        "tenant",
    }

    assert "pkid" not in serializer.fields
    assert "updated_at" not in serializer.fields

@pytest.mark.django_db
def test_apartment_serializer_tenant_is_hidden_field():
    serializer = ApartmentSerializer()

    assert isinstance(
        serializer.fields["tenant"],
        serializers.HiddenField,
    )

@pytest.mark.django_db
def test_apartment_serializer_sets_current_user_as_tenant():
    user = User.objects.create_user(
        username="currenttenant",
        email="currenttenant@example.com",
        password="TestPassword123!",
    )

    request = APIRequestFactory().post("/")
    request.user = user

    serializer = ApartmentSerializer(
        data={
            "unit_number": "G701",
            "building": "Willow House",
            "floor": 7,
        },
        context={"request": request},
    )

    assert serializer.is_valid(), serializer.errors

    assert serializer.validated_data["tenant"] == user

@pytest.mark.django_db
def test_apartment_serializer_creates_apartment():
    user = User.objects.create_user(
        username="createapartment",
        email="createapartment@example.com",
        password="TestPassword123!",
    )

    request = APIRequestFactory().post("/")
    request.user = user

    serializer = ApartmentSerializer(
        data={
            "unit_number": "H802",
            "building": "Ash House",
            "floor": 8,
        },
        context={"request": request},
    )

    assert serializer.is_valid(), serializer.errors

    apartment = serializer.save()

    assert apartment.unit_number == "H802"
    assert apartment.building == "Ash House"
    assert apartment.floor == 8
    assert apartment.tenant == user

@pytest.mark.django_db
def test_apartment_serializer_rejects_duplicate_unit_number():
    user = User.objects.create_user(
        username="duplicateunit",
        email="duplicateunit@example.com",
        password="TestPassword123!",
    )

    Apartment.objects.create(
        unit_number="I903",
        building="Pine House",
        floor=9,
        tenant=user,
    )

    request = APIRequestFactory().post("/")
    request.user = user

    serializer = ApartmentSerializer(
        data={
            "unit_number": "I903",
            "building": "Oak House",
            "floor": 1,
        },
        context={"request": request},
    )

    assert not serializer.is_valid()
    assert "unit_number" in serializer.errors

@pytest.mark.django_db
def test_apartment_serializer_rejects_tenant_with_existing_apartment():
    tenant = User.objects.create_user(
        username="existingtenant",
        email="existingtenant@example.com",
        password="TestPassword123!",
    )

    Apartment.objects.create(
        unit_number="R801",
        building="Oak House",
        floor=8,
        tenant=tenant,
    )

    serializer = ApartmentSerializer(
        data={
            "unit_number": "R802",
            "building": "Oak House",
            "floor": 8,
        },
        context={"request": type(
            "Request",
            (),
            {"user": tenant}
        )()},
    )

    assert not serializer.is_valid()
    assert "tenant" in serializer.errors