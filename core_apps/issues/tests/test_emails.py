import pytest
from unittest.mock import MagicMock, patch

from core_apps.apartments.models import Apartment
from core_apps.issues.emails import (
    send_issue_confirmation_email,
    send_resolution_email,
)
from core_apps.issues.models import Issue


@pytest.fixture
def issue_for_email(db, django_user_model):
    reporter = django_user_model.objects.create_user(
        username="reporter",
        email="reporter@example.com",
        password="TestPass123!",
        first_name="Test",
        last_name="Reporter",
    )

    apartment = Apartment.objects.create(
        unit_number="B101",
        building="Email Building",
        floor=1,
        tenant=reporter,
    )

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=reporter,
        title="Broken Window",
        description="The bedroom window is broken.",
        status=Issue.IssueStatus.REPORTED,
        priority=Issue.Priority.HIGH,
    )

    return issue


@pytest.mark.django_db
@patch("core_apps.issues.emails.EmailMultiAlternatives")
@patch("core_apps.issues.emails.render_to_string")
@patch("core_apps.issues.emails.strip_tags")
def test_send_issue_confirmation_email(
    mock_strip_tags,
    mock_render_to_string,
    mock_email_class,
    issue_for_email,
):
    mock_render_to_string.return_value = "<html>Issue confirmation</html>"
    mock_strip_tags.return_value = "Issue confirmation"

    email = MagicMock()
    mock_email_class.return_value = email

    send_issue_confirmation_email(issue_for_email)

    mock_render_to_string.assert_called_once_with(
        "emails/issue_confirmation.html",
        {
            "issue": issue_for_email,
            "site_name": "Accommodation Center",
        },
    )

    mock_strip_tags.assert_called_once_with(
        "<html>Issue confirmation</html>"
    )

    mock_email_class.assert_called_once_with(
        "Issue Report Confirmation",
        "Issue confirmation",
        "admin@golden-ventures.com",
        ["reporter@example.com"],
    )

    email.attach_alternative.assert_called_once_with(
        "<html>Issue confirmation</html>",
        "text/html",
    )

    email.send.assert_called_once_with()


@pytest.mark.django_db
@patch("core_apps.issues.emails.EmailMultiAlternatives")
@patch("core_apps.issues.emails.render_to_string")
@patch("core_apps.issues.emails.strip_tags")
def test_send_resolution_email(
    mock_strip_tags,
    mock_render_to_string,
    mock_email_class,
    issue_for_email,
):
    mock_render_to_string.return_value = "<html>Issue resolved</html>"
    mock_strip_tags.return_value = "Issue resolved"

    email = MagicMock()
    mock_email_class.return_value = email

    send_resolution_email(issue_for_email)

    mock_render_to_string.assert_called_once_with(
        "emails/issue_resolved_notification.html",
        {
            "issue": issue_for_email,
            "site_name": "Accommodation Center",
        },
    )

    mock_strip_tags.assert_called_once_with(
        "<html>Issue resolved</html>"
    )

    mock_email_class.assert_called_once_with(
        "Issue Resolved: Broken Window",
        "Issue resolved",
        "admin@golden-ventures.com",
        ["reporter@example.com"],
    )

    email.attach_alternative.assert_called_once_with(
        "<html>Issue resolved</html>",
        "text/html",
    )

    email.send.assert_called_once_with()


@pytest.mark.django_db
@patch("core_apps.issues.emails.logger.error")
@patch(
    "core_apps.issues.emails.render_to_string",
    side_effect=Exception("Template rendering failed"),
)
def test_send_issue_confirmation_email_handles_exception(
    mock_render_to_string,
    mock_logger_error,
    issue_for_email,
):
    send_issue_confirmation_email(issue_for_email)

    mock_logger_error.assert_called_once()

    error_message = mock_logger_error.call_args.args[0]

    assert (
        "Failed to send confirmation email for issue "
        "'Broken Window'" in error_message
    )

    assert "Template rendering failed" in error_message

    assert mock_logger_error.call_args.kwargs["exc_info"] is True


@pytest.mark.django_db
@patch("core_apps.issues.emails.logger.error")
@patch(
    "core_apps.issues.emails.render_to_string",
    side_effect=Exception("Template rendering failed"),
)
def test_send_resolution_email_handles_exception(
    mock_render_to_string,
    mock_logger_error,
    issue_for_email,
):
    send_resolution_email(issue_for_email)

    mock_logger_error.assert_called_once()

    error_message = mock_logger_error.call_args.args[0]

    assert (
        "Failed to send resolution email for issue "
        "'Broken Window'" in error_message
    )

    assert "Template rendering failed" in error_message

    assert mock_logger_error.call_args.kwargs["exc_info"] is True