import pytest
from rest_framework.test import APIClient

from core_apps.reports.models import Report


@pytest.fixture
def api_client():
    return APIClient()


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

    other_user = django_user_model.objects.create_user(
        username="other",
        email="other@example.com",
        password="TestPass123!",
        first_name="Other",
        last_name="User",
    )

    return reporter, reported_user, other_user


@pytest.fixture
def mock_report_emails(monkeypatch):
    monkeypatch.setattr(
        "core_apps.reports.signals.send_warning_email",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "core_apps.reports.signals.send_deactivation_email",
        lambda *args, **kwargs: None,
    )


def test_authenticated_user_can_create_report(
    api_client,
    report_users,
    mock_report_emails,
):
    reporter, reported_user, _ = report_users

    api_client.force_authenticate(user=reporter)

    response = api_client.post(
        "/api/v1/reports/create/",
        {
            "title": "Broken Window",
            "description": "The bedroom window has been broken.",
            "reported_user_username": reported_user.username,
        },
        format="json",
    )

    assert response.status_code == 201

    report = Report.objects.get()

    assert report.title == "Broken Window"
    assert report.description == "The bedroom window has been broken."
    assert report.reported_by == reporter
    assert report.reported_user == reported_user


def test_create_report_sets_reported_by_to_authenticated_user(
    api_client,
    report_users,
    mock_report_emails,
):
    reporter, reported_user, other_user = report_users

    api_client.force_authenticate(user=reporter)

    response = api_client.post(
        "/api/v1/reports/create/",
        {
            "title": "Noise Complaint",
            "description": "Loud noise was coming from the apartment.",
            "reported_user_username": reported_user.username,
        },
        format="json",
    )

    assert response.status_code == 201

    report = Report.objects.get()

    assert report.reported_by == reporter
    assert report.reported_by != other_user


def test_create_report_with_nonexistent_username_returns_400(
    api_client,
    report_users,
    mock_report_emails,
):
    reporter, _, _ = report_users

    api_client.force_authenticate(user=reporter)

    response = api_client.post(
        "/api/v1/reports/create/",
        {
            "title": "Invalid Report",
            "description": "This report should fail validation.",
            "reported_user_username": "does-not-exist",
        },
        format="json",
    )

    assert response.status_code == 400
    assert response.data["reported_user_username"][0] == (
        "The provided username does not exist"
    )
    assert Report.objects.count() == 0


def test_my_reports_returns_only_authenticated_users_reports(
    api_client,
    report_users,
    mock_report_emails,
):
    reporter, reported_user, other_user = report_users

    own_report = Report.objects.create(
        title="My Report",
        description="My report description.",
        reported_by=reporter,
        reported_user=reported_user,
    )

    other_report = Report.objects.create(
        title="Other Report",
        description="Other report description.",
        reported_by=other_user,
        reported_user=reported_user,
    )

    api_client.force_authenticate(user=reporter)

    response = api_client.get("/api/v1/reports/me/")

    assert response.status_code == 200

    results = response.data["results"]

    assert len(results) == 1
    assert results[0]["id"] == str(own_report.id)
    assert results[0]["title"] == "My Report"
    assert results[0]["id"] != str(other_report.id)


def test_unauthenticated_user_cannot_create_report(
    api_client,
    report_users,
    mock_report_emails,
):
    _, reported_user, _ = report_users

    response = api_client.post(
        "/api/v1/reports/create/",
        {
            "title": "Unauthenticated Report",
            "description": "This should not be created.",
            "reported_user_username": reported_user.username,
        },
        format="json",
    )

    assert response.status_code in (401, 403)
    assert Report.objects.count() == 0