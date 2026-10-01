import pytest
from rest_framework.test import APIRequestFactory

from core_apps.users.models import User
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from core_apps.common.cookie_auth import CookieAuthentication


@pytest.mark.django_db
def test_cookie_authentication_returns_none_without_header_or_cookie():
    factory = APIRequestFactory()
    request = factory.get("/")

    authentication = CookieAuthentication()

    result = authentication.authenticate(request)

    assert result is None




@pytest.mark.django_db
def test_cookie_authentication_authenticates_user_from_cookie():
    user = User.objects.create_user(
        username="cookieuser",
        email="cookieuser@example.com",
        password="TestPassword123!",
    )

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    factory = APIRequestFactory()
    request = factory.get("/")

    request.COOKIES[settings.COOKIE_NAME] = access_token

    authentication = CookieAuthentication()

    result = authentication.authenticate(request)

    assert result is not None

    authenticated_user, validated_token = result

    assert authenticated_user == user
    assert str(validated_token) == access_token

@pytest.mark.django_db
def test_cookie_authentication_authenticates_user_from_authorization_header():
    user = User.objects.create_user(
        username="headeruser",
        email="headeruser@example.com",
        password="TestPassword123!",
    )

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    factory = APIRequestFactory()
    request = factory.get(
        "/",
        HTTP_AUTHORIZATION=f"Bearer {access_token}",
    )

    authentication = CookieAuthentication()

    result = authentication.authenticate(request)

    assert result is not None

    authenticated_user, validated_token = result

    assert authenticated_user == user
    assert str(validated_token) == access_token