import pytest

from django.urls import resolve

from core_apps.apartments.views import (
    ApartmentCreateAPIView,
    ApartmentDetailAPIView,
)


@pytest.mark.parametrize(
    "url, expected_view",
    [
        ("add/", ApartmentCreateAPIView),
        ("my-apartment/", ApartmentDetailAPIView),
    ],
)
def test_apartment_urls_resolve_to_correct_views(url, expected_view):
    resolved = resolve(f"/api/v1/apartments/{url}")

    assert resolved.func.view_class == expected_view