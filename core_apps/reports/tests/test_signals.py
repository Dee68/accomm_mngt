import pytest
from unittest.mock import MagicMock

from core_apps.reports.models import Report


@pytest.fixture
def report_users(db, django_user_model):
    reporter = django_user_model.objects.create_user(
        username="reporter",
        email="reporter@example.com",
        password="TestPass123!",
        first_name="John",
        last_name="Reporter",
    )

    reported_user = django_user_model.objects.create_user(
        username="reported",
        email="reported@example.com",
        password="TestPass123!",
        first_name="Jane",
        last_name="Reported",
    )

    return reporter, reported_user


@pytest.fixture
def mock_report_emails(monkeypatch):
    mock_warning_email = MagicMock()
    mock_deactivation_email = MagicMock()

    monkeypatch.setattr(
        "core_apps.reports.signals.send_warning_email",
        mock_warning_email,
    )
    monkeypatch.setattr(
        "core_apps.reports.signals.send_deactivation_email",
        mock_deactivation_email,
    )

    return {
        "warning": mock_warning_email,
        "deactivation": mock_deactivation_email,
    }


def create_report(reporter, reported_user, title="Test Report"):
    return Report.objects.create(
        title=title,
        reported_by=reporter,
        reported_user=reported_user,
        description="Test report description.",
    )


def test_report_creation_increments_report_count(
    report_users,
    mock_report_emails,
):
    reporter, reported_user = report_users

    create_report(reporter, reported_user)

    reported_user.profile.refresh_from_db()

    assert reported_user.profile.report_count == 1


def test_first_report_sends_warning_email(
    report_users,
    mock_report_emails,
):
    reporter, reported_user = report_users

    report = create_report(
        reporter,
        reported_user,
        title="Broken Window",
    )

    mock_report_emails["warning"].assert_called_once_with(
        reported_user,
        report.title,
        report.description,
    )

    mock_report_emails["deactivation"].assert_not_called()


def test_fifth_report_deactivates_user(
    report_users,
    mock_report_emails,
):
    reporter, reported_user = report_users

    for number in range(1, 5):
        create_report(
            reporter,
            reported_user,
            title=f"Report {number}",
        )

    reported_user.refresh_from_db()
    assert reported_user.is_active is True

    fifth_report = create_report(
        reporter,
        reported_user,
        title="Report 5",
    )

    reported_user.refresh_from_db()

    assert reported_user.profile.report_count == 5
    assert reported_user.is_active is False

    mock_report_emails["deactivation"].assert_called_once_with(
        reported_user,
        fifth_report.title,
        fifth_report.description,
    )


def test_existing_report_update_does_not_trigger_signal(
    report_users,
    mock_report_emails,
):
    reporter, reported_user = report_users

    report = create_report(reporter, reported_user)

    reported_user.profile.refresh_from_db()
    assert reported_user.profile.report_count == 1

    mock_report_emails["warning"].reset_mock()
    mock_report_emails["deactivation"].reset_mock()

    report.description = "Updated description."
    report.save()

    reported_user.profile.refresh_from_db()

    assert reported_user.profile.report_count == 1
    mock_report_emails["warning"].assert_not_called()
    mock_report_emails["deactivation"].assert_not_called()