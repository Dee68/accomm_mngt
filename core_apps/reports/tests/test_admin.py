import pytest
from django.contrib import admin

from core_apps.reports.admin import ReportAdmin
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
def report(report_users, monkeypatch):
    reporter, reported_user = report_users

    monkeypatch.setattr(
        "core_apps.reports.signals.send_warning_email",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "core_apps.reports.signals.send_deactivation_email",
        lambda *args, **kwargs: None,
    )

    return Report.objects.create(
        title="Broken Window",
        reported_by=reporter,
        reported_user=reported_user,
        description="The bedroom window has been broken.",
    )


@pytest.fixture
def report_admin():
    return ReportAdmin(Report, admin.site)


def test_report_is_registered_with_admin():
    assert admin.site.is_registered(Report)
    assert isinstance(admin.site._registry[Report], ReportAdmin)


def test_report_admin_has_expected_list_display(report_admin):
    assert report_admin.list_display == [
        "title",
        "reported_by",
        "reported_user",
        "get_report_count",
        "created_at",
    ]


def test_report_admin_has_expected_search_fields(report_admin):
    assert report_admin.search_fields == [
        "title",
        "reported_by__first_name",
        "reported_user__first_name",
        "reported_user__last_name",
    ]


@pytest.mark.django_db
def test_get_queryset_selects_reported_user_profile(report_admin, report):
    queryset = report_admin.get_queryset(None)

    assert "reported_user" in queryset.query.select_related
    assert "profile" in queryset.query.select_related["reported_user"]


def test_get_report_count_returns_report_count(report_admin, report):
    report.reported_user.profile.report_count = 3
    report.reported_user.profile.save()

    report.reported_user.profile.refresh_from_db()

    assert report_admin.get_report_count(report) == 3


def test_get_report_count_has_correct_short_description(report_admin):
    assert report_admin.get_report_count.short_description == "Report Count"