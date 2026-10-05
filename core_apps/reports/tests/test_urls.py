from django.urls import reverse


def test_create_report_url():
    assert reverse("create-report") == "/api/v1/reports/create/"


def test_my_reports_url():
    assert reverse("my-reports") == "/api/v1/reports/me/"