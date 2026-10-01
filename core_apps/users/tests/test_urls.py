import pytest
from django.urls import resolve, reverse

from core_apps.users.views import (
    CustomProviderAuthView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutAPIView,
)


@pytest.mark.parametrize(
    "url, expected_view",
    [
        ("login/", CustomTokenObtainPairView),
        ("refresh/", CustomTokenRefreshView),
        ("logout/", LogoutAPIView),
        ("o/google-oauth2/", CustomProviderAuthView),
    ],
)
def test_users_urls_resolve_to_correct_views(url, expected_view):
    resolved = resolve(f"/api/v1/auth/{url}")

    assert resolved.func.view_class == expected_view

def test_provider_auth_url_name():
    url = reverse("provider-auth", kwargs={"provider": "google-oauth2"})

    assert url == "/api/v1/auth/o/google-oauth2/"