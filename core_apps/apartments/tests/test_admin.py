import pytest
from django.contrib import admin

from core_apps.apartments.admin import ApartmentAdmin
from core_apps.apartments.models import Apartment


def test_apartment_is_registered_with_admin():
    assert Apartment in admin.site._registry
    assert isinstance(admin.site._registry[Apartment], ApartmentAdmin)


def test_apartment_admin_configuration():
    admin_instance = admin.site._registry[Apartment]

    assert admin_instance.list_display == [
        "id",
        "unit_number",
        "building",
        "floor",
        "tenant",
    ]

    assert admin_instance.list_display_links == [
        "id",
        "unit_number",
    ]

    assert admin_instance.list_filter == [
        "building",
        "floor",
    ]

    assert admin_instance.search_fields == ["unit_number"]

    assert admin_instance.ordering == [
        "building",
        "floor",
    ]

    assert admin_instance.autocomplete_fields == ["tenant"]