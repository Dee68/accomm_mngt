import pytest
from rest_framework.exceptions import ValidationError

from core_apps.reports.models import Report
from core_apps.reports.serializers import ReportSerializer


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


def test_report_serializer_has_expected_fields():
    serializer = ReportSerializer()

    assert set(serializer.fields.keys()) == {
        "id",
        "title",
        "description",
        "reported_user_username",
        "created_at",
    }


def test_reported_user_username_is_write_only():
    serializer = ReportSerializer()

    assert serializer.fields["reported_user_username"].write_only is True


def test_valid_reported_user_username_passes_validation(report_users):
    _, reported_user = report_users

    serializer = ReportSerializer(
        data={
            "title": "Broken Window",
            "description": "The bedroom window has been broken.",
            "reported_user_username": reported_user.username,
        }
    )

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["reported_user_username"] == reported_user.username


def test_invalid_reported_user_username_fails_validation(report_users):
    serializer = ReportSerializer(
        data={
            "title": "Broken Window",
            "description": "The bedroom window has been broken.",
            "reported_user_username": "does-not-exist",
        }
    )

    assert not serializer.is_valid()
    assert (
        serializer.errors["reported_user_username"][0]
        == "The provided username does not exist"
    )


def test_create_resolves_reported_user_and_creates_report(
    report_users,
    monkeypatch,
):
    reporter, reported_user = report_users

    # Prevent the Report post_save signal from sending actual emails.
    warning_email = lambda *args, **kwargs: None
    deactivation_email = lambda *args, **kwargs: None

    monkeypatch.setattr(
        "core_apps.reports.signals.send_warning_email",
        warning_email,
    )
    monkeypatch.setattr(
        "core_apps.reports.signals.send_deactivation_email",
        deactivation_email,
    )

    serializer = ReportSerializer(
        data={
            "title": "Broken Window",
            "description": "The bedroom window has been broken.",
            "reported_user_username": reported_user.username,
        }
    )

    assert serializer.is_valid(), serializer.errors

    report = serializer.save(
        reported_by=reporter,
    )

    assert isinstance(report, Report)
    assert report.title == "Broken Window"
    assert report.description == "The bedroom window has been broken."
    assert report.reported_user == reported_user
    assert report.reported_by == reporter


def test_report_serializer_output_does_not_include_reported_user_username(
    report_users,
    monkeypatch,
):
    reporter, reported_user = report_users

    monkeypatch.setattr(
        "core_apps.reports.signals.send_warning_email",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "core_apps.reports.signals.send_deactivation_email",
        lambda *args, **kwargs: None,
    )

    report = Report.objects.create(
        title="Broken Window",
        reported_by=reporter,
        reported_user=reported_user,
        description="The bedroom window has been broken.",
    )

    serializer = ReportSerializer(report)

    assert "reported_user_username" not in serializer.data
    assert serializer.data["title"] == "Broken Window"
    assert serializer.data["description"] == (
        "The bedroom window has been broken."
    )