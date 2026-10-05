from unittest.mock import MagicMock

import pytest

from core_apps.reports.emails import (
    send_deactivation_email,
    send_warning_email,
)
from django.utils.html import strip_tags
from config.settings.local import DEFAULT_FROM_EMAIL, SITE_NAME


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(
        username="reported",
        email="reported@example.com",
        password="TestPass123!",
        first_name="Jane",
        last_name="Reported",
    )


@pytest.fixture
def mock_email_dependencies(monkeypatch):
    html_content = """
        <html>
            <body>
                <h1>Test Email</h1>
                <p>This is a test email.</p>
            </body>
        </html>
    """

    render_to_string = MagicMock(return_value=html_content)
    email_class = MagicMock()

    email_instance = email_class.return_value
    email_instance.send.return_value = 1

    monkeypatch.setattr(
        "core_apps.reports.emails.render_to_string",
        render_to_string,
    )
    monkeypatch.setattr(
        "core_apps.reports.emails.EmailMultiAlternatives",
        email_class,
    )

    return {
        "render_to_string": render_to_string,
        "email_class": email_class,
        "email_instance": email_instance,
        "html_content": html_content,
    }


def test_send_warning_email(
    user,
    mock_email_dependencies,
):
    send_warning_email(
        user,
        "Broken Window",
        "The bedroom window has been broken.",
    )

    render_to_string = mock_email_dependencies["render_to_string"]
    email_class = mock_email_dependencies["email_class"]
    email_instance = mock_email_dependencies["email_instance"]
    html_content = mock_email_dependencies["html_content"]

    render_to_string.assert_called_once_with(
        "emails/warning_email.html",
        {
            "user": user,
            "title": "Broken Window",
            "description": "The bedroom window has been broken.",
            "site_name": SITE_NAME,
        },
    )

    email_class.assert_called_once_with(
        f"Warning: {user.get_full_name}, you have been reported!",
        strip_tags(html_content),
        DEFAULT_FROM_EMAIL,
        [user.email],
    )

    email_instance.attach_alternative.assert_called_once_with(
        html_content,
        "text/html",
    )

    email_instance.send.assert_called_once_with()


def test_send_deactivation_email(
    user,
    mock_email_dependencies,
):
    send_deactivation_email(
        user,
        "Repeated Noise Complaint",
        "The tenant has repeatedly caused excessive noise.",
    )

    render_to_string = mock_email_dependencies["render_to_string"]
    email_class = mock_email_dependencies["email_class"]
    email_instance = mock_email_dependencies["email_instance"]
    html_content = mock_email_dependencies["html_content"]

    render_to_string.assert_called_once_with(
        "emails/deactivation_email.html",
        {
            "user": user,
            "title": "Repeated Noise Complaint",
            "description": "The tenant has repeatedly caused excessive noise.",
            "site_name": SITE_NAME,
        },
    )

    email_class.assert_called_once_with(
        f"Account Deactivation and Eviction Notice!: {user.get_full_name}",
        strip_tags(html_content),
        DEFAULT_FROM_EMAIL,
        [user.email],
    )

    email_instance.attach_alternative.assert_called_once_with(
        html_content,
        "text/html",
    )

    email_instance.send.assert_called_once_with()