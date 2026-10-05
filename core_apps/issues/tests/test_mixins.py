import pytest

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from core_apps.apartments.models import Apartment
from core_apps.common.models import ContentView
from core_apps.issues.models import Issue
from types import SimpleNamespace

from core_apps.issues.mixins import IssueViewMixin
from unittest.mock import patch

User = get_user_model()


def test_get_client_ip_uses_x_forwarded_for():
    mixin = IssueViewMixin()

    mixin.request = SimpleNamespace(
        META={
            "HTTP_X_FORWARDED_FOR": "192.168.1.10, 10.0.0.1",
            "REMOTE_ADDR": "127.0.0.1",
        }
    )

    assert mixin.get_client_ip() == "192.168.1.10"


def test_get_client_ip_uses_remote_addr_when_no_forwarded_for():
    mixin = IssueViewMixin()

    mixin.request = SimpleNamespace(
        META={
            "REMOTE_ADDR": "192.168.1.20",
        }
    )

    assert mixin.get_client_ip() == "192.168.1.20"

@pytest.fixture
def issue_for_view():
    user = User.objects.create_user(
        username="viewer",
        email="viewer@example.com",
        password="TestPassword123!",
    )

    apartment = Apartment.objects.create(
        unit_number="B101",
        building="View Building",
        floor=1,
    )

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        title="Broken window",
        description="The window is broken.",
    )

    return issue, user


@pytest.mark.django_db
def test_record_issue_view_creates_content_view(issue_for_view):
    issue, user = issue_for_view

    mixin = IssueViewMixin()

    mixin.request = SimpleNamespace(
        user=user,
        META={"REMOTE_ADDR": "192.168.1.30"},
    )

    mixin.record_issue_view(issue)

    content_type = ContentType.objects.get_for_model(issue)

    content_view = ContentView.objects.get(
        content_type=content_type,
        object_id=issue.id,
        user=user,
        viewer_ip="192.168.1.30",
    )

    assert content_view.object_id == issue.id
    assert content_view.user == user
    assert content_view.viewer_ip == "192.168.1.30"
    assert content_view.last_viewed is not None


@pytest.mark.django_db
def test_record_issue_view_does_not_create_duplicate_content_view(
    issue_for_view,
):
    issue, user = issue_for_view

    mixin = IssueViewMixin()

    mixin.request = SimpleNamespace(
        user=user,
        META={"REMOTE_ADDR": "192.168.1.40"},
    )

    mixin.record_issue_view(issue)
    mixin.record_issue_view(issue)

    content_type = ContentType.objects.get_for_model(issue)

    assert ContentView.objects.filter(
        content_type=content_type,
        object_id=issue.id,
        user=user,
        viewer_ip="192.168.1.40",
    ).count() == 1


@pytest.mark.django_db
def test_record_issue_view_handles_content_view_error(issue_for_view):
    issue, user = issue_for_view

    mixin = IssueViewMixin()

    mixin.request = SimpleNamespace(
        user=user,
        META={"REMOTE_ADDR": "192.168.1.50"},
    )

    with patch(
        "core_apps.issues.mixins.ContentView.objects.get_or_create",
        side_effect=Exception("Database error"),
    ):
        mixin.record_issue_view(issue)

