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


@pytest.fixture
def report(db, report_users, mock_report_emails):
    reporter, reported_user = report_users

    return Report.objects.create(
        title="Broken Window",
        reported_by=reporter,
        reported_user=reported_user,
        description="The bedroom window has been broken.",
    )


def test_report_str_returns_expected_description(report, report_users):
    reporter, reported_user = report_users

    assert str(report) == (
        f"Report by {reporter.get_full_name} "
        f"against {reported_user.get_full_name}"
    )


def test_report_stores_title(report):
    assert report.title == "Broken Window"


def test_report_stores_description(report):
    assert report.description == "The bedroom window has been broken."


def test_report_generates_slug_from_title(report):
    assert report.slug == "broken-window"


def test_report_slug_is_unique(report, report_users, mock_report_emails):
    reporter, reported_user = report_users

    second_report = Report.objects.create(
        title="Broken Window",
        reported_by=reporter,
        reported_user=reported_user,
        description="Another description.",
    )

    assert second_report.slug != report.slug
    assert second_report.slug == "broken-window-2"


def test_report_has_correct_reported_by_relationship(report, report_users):
    reporter, _ = report_users

    assert report.reported_by == reporter
    assert report in reporter.report_made.all()


def test_report_has_correct_reported_user_relationship(report, report_users):
    _, reported_user = report_users

    assert report.reported_user == reported_user
    assert report in reported_user.report_received.all()


@pytest.mark.django_db
def test_deleting_reported_by_deletes_report(
    report,
    report_users,
):
    reporter, _ = report_users
    report_pk = report.pk

    reporter.delete()

    assert not Report.objects.filter(pk=report_pk).exists()


@pytest.mark.django_db
def test_deleting_reported_user_deletes_report(
    report,
    report_users,
):
    _, reported_user = report_users
    report_pk = report.pk

    reported_user.delete()

    assert not Report.objects.filter(pk=report_pk).exists()


def test_report_has_created_and_updated_timestamps(report):
    assert report.created_at is not None
    assert report.updated_at is not None


def test_report_has_uuid_id(report):
    assert report.id is not None


def test_report_metadata():
    assert Report._meta.verbose_name == "Report"
    assert Report._meta.verbose_name_plural == "Reports"


def test_report_warning_email_is_triggered_on_first_report(
    report,
    mock_report_emails,
):
    mock_report_emails["warning"].assert_called_once_with(
        report.reported_user,
        report.title,
        report.description,
    )


def test_reported_user_report_count_is_incremented(
    report,
):
    report.reported_user.profile.refresh_from_db()

    assert report.reported_user.profile.report_count == 1