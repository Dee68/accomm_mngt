import pytest
from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from core_apps.posts.permissions import CanCreateEditPost
from core_apps.profiles.models import Profile

User = get_user_model()


@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_or_edit_post():
    factory = APIRequestFactory()
    request = factory.post("/api/v1/posts/create/")
    request.user = AnonymousUser()

    permission = CanCreateEditPost()

    assert permission.has_permission(request, None) is False
    assert permission.message == "Authentication is required to view this resource."


@pytest.mark.django_db
def test_regular_authenticated_user_cannot_create_or_edit_post():
    user = User.objects.create_user(
        username="regularuser",
        email="regular@example.com",
        password="TestPassword123!",
    )

    profile = user.profile
    profile.occupation = Profile.Occupation.MASON
    profile.save()

    factory = APIRequestFactory()
    request = factory.post("/api/v1/posts/create/")
    request.user = user

    permission = CanCreateEditPost()

    assert permission.has_permission(request, None) is False


@pytest.mark.django_db
def test_tenant_can_create_or_edit_post():
    user = User.objects.create_user(
        username="tenantuser",
        email="tenant@example.com",
        password="TestPassword123!",
    )

    profile = user.profile
    profile.occupation = Profile.Occupation.TENANT
    profile.save()

    factory = APIRequestFactory()
    request = factory.post("/api/v1/posts/create/")
    request.user = user

    permission = CanCreateEditPost()

    assert permission.has_permission(request, None) is True


@pytest.mark.django_db
def test_staff_user_can_create_or_edit_post():
    user = User.objects.create_user(
        username="staffuser",
        email="staff@example.com",
        password="TestPassword123!",
        is_staff=True,
    )

    factory = APIRequestFactory()
    request = factory.post("/api/v1/posts/create/")
    request.user = user

    permission = CanCreateEditPost()

    assert permission.has_permission(request, None) is True


@pytest.mark.django_db
def test_superuser_can_create_or_edit_post():
    user = User.objects.create_superuser(
        username="adminuser",
        email="admin@example.com",
        password="TestPassword123!",
    )

    factory = APIRequestFactory()
    request = factory.post("/api/v1/posts/create/")
    request.user = user

    permission = CanCreateEditPost()

    assert permission.has_permission(request, None) is True
