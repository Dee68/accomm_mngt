from django.contrib import admin

from core_apps.profiles.admin import ProfileAdmin
from core_apps.profiles.models import Profile


def test_profile_is_registered_with_admin():
    assert Profile in admin.site._registry
    assert isinstance(admin.site._registry[Profile], ProfileAdmin)


def test_profile_admin_configuration():
    profile_admin = admin.site._registry[Profile]

    assert profile_admin.list_display == [
        "id",
        "user",
        "gender",
        "occupation",
        "slug",
    ]

    assert profile_admin.list_display_links == [
        "id",
        "user",
    ]

    assert profile_admin.list_filter == [
        "occupation",
        "gender",
    ]