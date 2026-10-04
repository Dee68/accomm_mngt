import pytest
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient

from core_apps.common.models import ContentView
from core_apps.issues.models import Issue
from core_apps.apartments.models import Apartment
from core_apps.users.models import User


@pytest.mark.django_db
def test_issue_detail_records_content_view_with_uuid():
    user = User.objects.create_user(
        username="issue_view_user",
        email="issue_view_user@example.com",
        password="TestPassword123!",
    )

    apartment = Apartment.objects.create(
        unit_number="A103",
        building="Test Building",
        floor=1,
        tenant=user,
    )

    issue = Issue.objects.create(
        title="Issue View Test",
        description="Testing issue view recording.",
        apartment=apartment,
        reported_by=user,
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(f"/api/v1/issues/{issue.id}/")

    assert response.status_code == 200

    content_type = ContentType.objects.get_for_model(Issue)

    assert ContentView.objects.filter(
        content_type=content_type,
        object_id=issue.id,
        user=user,
    ).exists()