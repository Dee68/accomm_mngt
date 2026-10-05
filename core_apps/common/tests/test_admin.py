import pytest
from django.contrib import admin

from core_apps.common.admin import ContentViewAdmin
from core_apps.common.models import ContentView



@pytest.mark.django_db
def test_content_view_admin_is_registered():
    assert admin.site._registry[ContentView].__class__ is ContentViewAdmin


def test_content_view_admin_list_display():
    assert ContentViewAdmin.list_display == [
        "content_object",
        "user",
        "viewer_ip",
        "created_at",
    ]

