import pytest
from django.urls import resolve,reverse

from core_apps.profiles.views import (
    ProfileListAPIView,
    ProfileDetailAPIView,
    ProfileUpdateAPIView,
    AvatarUploadView,
    NonTenantProfileListView
)

@pytest.mark.parametrize(
    "url, expected_view",
    [
        ("all/", ProfileListAPIView),
        ("non-tenant-profiles/", NonTenantProfileListView),
        ( "user/my-profile/", ProfileDetailAPIView),
        ("user/update/", ProfileUpdateAPIView),
        ( "user/avatar/", AvatarUploadView)

    ]
)
def test_users_urls_resolve_to_correct_views(url, expected_view):
    resolved = resolve(f"/api/v1/profiles/{url}")
    assert resolved.func.view_class == expected_view