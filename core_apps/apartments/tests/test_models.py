import pytest

from core_apps.apartments.models import Apartment
from core_apps.users.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_apartment_can_be_created():
    tenant = User.objects.create_user(
        username="apartmenttenant",
        email="tenant@example.com",
        password="TestPassword123!",
    )

    apartment = Apartment.objects.create(
        unit_number="A101",
        building="Oak House",
        floor=1,
        tenant=tenant,
    )

    assert apartment.pkid is not None
    assert apartment.id is not None
    assert apartment.unit_number == "A101"
    assert apartment.building == "Oak House"
    assert apartment.floor == 1
    assert apartment.tenant == tenant
    assert apartment.created_at is not None
    assert apartment.updated_at is not None

@pytest.mark.django_db
def test_apartment_string_representation():
    apartment = Apartment.objects.create(
        unit_number="B205",
        building="Maple House",
        floor=2,
    )

    assert str(apartment) == "Unit: B205 - Building: Maple House - Floor: 2"




@pytest.mark.django_db
def test_apartment_unit_number_must_be_unique():
    Apartment.objects.create(
        unit_number="C301",
        building="Pine House",
        floor=3,
    )

    with pytest.raises(IntegrityError):
        Apartment.objects.create(
            unit_number="C301",
            building="Oak House",
            floor=1,
        )

@pytest.mark.django_db
def test_apartment_can_have_no_tenant():
    apartment = Apartment.objects.create(
        unit_number="D402",
        building="Cedar House",
        floor=4,
        tenant=None,
    )

    assert apartment.tenant is None

@pytest.mark.django_db
def test_tenant_can_have_only_one_apartment():
    tenant = User.objects.create_user(
        username="onetenant",
        email="onetenant@example.com",
        password="TestPassword123!",
    )

    Apartment.objects.create(
        unit_number="G801",
        building="Oak House",
        floor=8,
        tenant=tenant,
    )

    with pytest.raises(IntegrityError):
        Apartment.objects.create(
            unit_number="G802",
            building="Oak House",
            floor=8,
            tenant=tenant,
        )

@pytest.mark.django_db
def test_deleting_tenant_sets_apartment_tenant_to_null():
    tenant = User.objects.create_user(
        username="deletetenant",
        email="delete@example.com",
        password="TestPassword123!",
    )

    apartment = Apartment.objects.create(
        unit_number="E503",
        building="Elm House",
        floor=5,
        tenant=tenant,
    )

    tenant.delete()

    apartment.refresh_from_db()

    assert apartment.tenant is None
@pytest.mark.django_db
def test_apartment_floor_cannot_be_negative():
    apartment = Apartment(
        unit_number="F604",
        building="Birch House",
        floor=-1,
    )

    with pytest.raises(ValidationError):
        apartment.full_clean()