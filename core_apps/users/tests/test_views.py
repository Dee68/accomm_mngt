import pytest
from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from django.test import RequestFactory

from rest_framework.response import Response

from core_apps.users.views import set_auth_cookies
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate

#from core_apps.users.views import CustomTokenObtainPairView
from core_apps.users.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutAPIView,
    CustomProviderAuthView
)

User = get_user_model()


class TestSetAuthCookies:

    @patch.object(settings, "SIMPLE_JWT", {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    })
    @patch.object(settings, "COOKIE_PATH", "/")
    @patch.object(settings, "COOKIE_SECURE", False)
    @patch.object(settings, "COOKIE_HTTPONLY", True)
    @patch.object(settings, "COOKIE_SAMESITE", "Lax")
    def test_sets_access_and_logged_in_cookies(self):
        response = Response()

        set_auth_cookies(
            response,
            access_token="access-token",
        )

        assert response.cookies["access"].value == "access-token"
        assert response.cookies["access"]["httponly"] is True
        assert not response.cookies["access"]["secure"]
        assert response.cookies["access"]["samesite"] == "Lax"

        assert response.cookies["logged_in"].value == "true"
        assert not response.cookies["logged_in"]["httponly"]

        assert "refresh" not in response.cookies

    @patch.object(settings, "SIMPLE_JWT", {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    })
    @patch.object(settings, "COOKIE_PATH", "/")
    @patch.object(settings, "COOKIE_SECURE", False)
    @patch.object(settings, "COOKIE_HTTPONLY", True)
    @patch.object(settings, "COOKIE_SAMESITE", "Lax")
    def test_sets_refresh_cookie_when_refresh_token_provided(self):
        response = Response()

        set_auth_cookies(
            response,
            access_token="access-token",
            refresh_token="refresh-token",
        )

        assert response.cookies["access"].value == "access-token"
        assert response.cookies["refresh"].value == "refresh-token"
        assert response.cookies["logged_in"].value == "true"

        assert response.cookies["refresh"]["httponly"] is True
        assert not response.cookies["refresh"]["secure"]
        assert response.cookies["refresh"]["samesite"] == "Lax"


@pytest.mark.django_db
class TestCustomTokenObtainPairView:

    def test_successful_login(self):
        user = User.objects.create_user(
            username="john_doe",
            email="john@example.com",
            password="StrongPassword123!",
            first_name="John",
            last_name="Doe",
        )

        factory = APIRequestFactory()

        request = factory.post(
            "/api/token/",
            {
                "email": user.email,
                "password": "StrongPassword123!",
            },
            format="json",
        )

        response = CustomTokenObtainPairView.as_view()(request)

        assert response.status_code == 200
        assert response.data["message"] == "Login Successful."

        assert "access" not in response.data
        assert "refresh" not in response.data

        assert response.cookies["access"].value
        assert response.cookies["refresh"].value
        assert response.cookies["logged_in"].value == "true"

    @pytest.mark.django_db
    def test_login_with_invalid_password(self):
        user = User.objects.create_user(
            username="john_doe",
            email="john@example.com",
            password="StrongPassword123!",
            first_name="John",
            last_name="Doe",
        )

        factory = APIRequestFactory()

        request = factory.post(
            "/api/token/",
            {
                "email": user.email,
                "password": "WrongPassword123!",
            },
            format="json",
        )

        response = CustomTokenObtainPairView.as_view()(request)

        assert response.status_code == 401

        assert "access" not in response.cookies
        assert "refresh" not in response.cookies
        assert "logged_in" not in response.cookies

        assert response.data.get("message") != "Login Successful."

class TestCustomTokenRefreshView:

    def test_refresh_without_token(self):
        factory = APIRequestFactory()

        request = factory.post(
            "/api/token/refresh/",
            {},
            format="json",
        )

        response = CustomTokenRefreshView.as_view()(request)

        assert response.status_code == 400
        assert response.data == {
            "error": "No refresh token provided"
        }

    @pytest.mark.django_db
    def test_successful_token_refresh(self):
        user = User.objects.create_user(
            username="john_doe",
            email="john@example.com",
            password="StrongPassword123!",
            first_name="John",
            last_name="Doe",
        )

        factory = APIRequestFactory()

        # First obtain a valid refresh token.
        login_request = factory.post(
            "/api/token/",
            {
                "email": user.email,
                "password": "StrongPassword123!",
            },
            format="json",
        )

        login_response = CustomTokenObtainPairView.as_view()(login_request)

        refresh_token = login_response.cookies["refresh"].value

        # Use the refresh token to obtain new tokens.
        request = factory.post(
            "/api/token/refresh/",
            {"refresh": refresh_token},
            format="json",
        )

        response = CustomTokenRefreshView.as_view()(request)

        assert response.status_code == 200
        assert response.data["message"] == "Access tokens refreshed successfully."

        assert "access" not in response.data
        assert "refresh" not in response.data

        assert response.cookies["access"].value
        assert response.cookies["refresh"].value
        assert response.cookies["logged_in"].value == "true"

    @pytest.mark.django_db
    def test_refresh_with_invalid_token(self):
        factory = APIRequestFactory()

        request = factory.post(
            "/api/token/refresh/",
            {"refresh": "invalid-refresh-token"},
            format="json",
        )

        response = CustomTokenRefreshView.as_view()(request)

        assert response.status_code == 401
        assert "access" not in response.cookies
        assert "refresh" not in response.cookies
        assert "logged_in" not in response.cookies

class TestLogoutAPIView:
    @pytest.mark.django_db
    def test_logout_deletes_auth_cookies(self):
        user = User.objects.create_user(
            username="john_doe",
            email="john@example.com",
            password="StrongPassword123!",
            first_name="John",
            last_name="Doe",
        )

        factory = APIRequestFactory()

        request = factory.post(
            "/api/logout/",
            {},
            format="json",
        )

        force_authenticate(request, user=user)

        response = LogoutAPIView.as_view()(request)

        assert response.status_code == 204

        assert response.cookies["access"]["max-age"] == 0
        assert response.cookies["refresh"]["max-age"] == 0
        assert response.cookies["logged_in"]["max-age"] == 0

class TestCustomProviderAuthView:

    @patch("core_apps.users.views.ProviderAuthView.post")
    def test_successful_provider_login(self, mock_provider_post):
        provider_response = Response(
            {
                "access": "provider-access-token",
                "refresh": "provider-refresh-token",
            },
            status=201,
        )

        mock_provider_post.return_value = provider_response

        factory = APIRequestFactory()

        request = factory.post(
            "/api/o/google-oauth2/",
            {},
            format="json",
        )

        response = CustomProviderAuthView.as_view()(request)

        assert response.status_code == 201
        assert response.data["message"] == "You are logged in successfully."

        assert "access" not in response.data
        assert "refresh" not in response.data

        assert response.cookies["access"].value == "provider-access-token"
        assert response.cookies["refresh"].value == "provider-refresh-token"
        assert response.cookies["logged_in"].value == "true"

    @patch("core_apps.users.views.ProviderAuthView.post")
    def test_provider_login_without_tokens(self, mock_provider_post):
        provider_response = Response(
            {},
            status=201,
        )

        mock_provider_post.return_value = provider_response

        factory = APIRequestFactory()

        request = factory.post(
            "/api/o/google-oauth2/",
            {},
            format="json",
        )

        response = CustomProviderAuthView.as_view()(request)

        assert response.status_code == 201
        assert response.data["message"] == (
            "Access or Refresh token not found in provider response."
        )

        assert "access" not in response.cookies
        assert "refresh" not in response.cookies
        assert "logged_in" not in response.cookies