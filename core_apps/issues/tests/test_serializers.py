import pytest
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from core_apps.common.models import ContentView
from core_apps.issues.models import Issue
from core_apps.apartments.models import Apartment
from core_apps.issues.serializers import IssueSerializer, IssueStatusUpdateSerializer
from rest_framework.test import APIRequestFactory



User = get_user_model()


@pytest.mark.django_db
def test_issue_serializer_returns_correct_view_count():
    user = User.objects.create_user(
        username="issue_view_user",
        email="issue_view_user@example.com",
        password="TestPassword123!",
    )

    apartment = Apartment.objects.create(
        unit_number="A101",
        building="Test Building",
        floor=1,
        tenant=user,
    )

    issue = Issue.objects.create(
        title="Test Issue",
        description="Testing issue view count.",
        apartment=apartment,
        reported_by=user,
    )

    content_type = ContentType.objects.get_for_model(issue)

    ContentView.objects.create(
        content_type=content_type,
        object_id=issue.id,
        user=user,
        viewer_ip="192.168.1.30",
        last_viewed="2026-10-04T20:00:00Z",
    )

    serializer = IssueSerializer(instance=issue)

    assert serializer.get_view_count(issue) == 1

@pytest.mark.django_db
def test_issue_status_update_records_content_view_when_resolved():
    user = User.objects.create_user(
        username="issue_resolve_user",
        email="issue_resolve_user@example.com",
        password="TestPassword123!",
    )

    apartment = Apartment.objects.create(
        unit_number="A102",
        building="Test Building",
        floor=1,
        tenant=user,
    )

    issue = Issue.objects.create(
        title="Issue To Resolve",
        description="Testing resolution view recording.",
        apartment=apartment,
        reported_by=user,
    )

    request = APIRequestFactory().patch(
        "/api/v1/issues/",
        {"status": Issue.IssueStatus.RESOLVED},
        format="json",
    )
    request.user = user

    serializer = IssueStatusUpdateSerializer(
        instance=issue,
        data={
            "title": issue.title,
            "description": issue.description,
            "status": Issue.IssueStatus.RESOLVED,
        },
        context={"request": request},
    )

    assert serializer.is_valid()

    serializer.save()

    content_type = ContentType.objects.get_for_model(issue)

    assert ContentView.objects.filter(
        content_type=content_type,
        object_id=issue.id,
        user=user,
    ).exists()
