import pytest

from unittest.mock import patch

from django.contrib.auth import get_user_model

from core_apps.apartments.models import Apartment
from core_apps.issues.models import Issue
from config.settings.local import DEFAULT_FROM_EMAIL

User = get_user_model()


@pytest.fixture
def issue_dependencies():
    user = User.objects.create_user(
        username="issueuser",
        email="issueuser@example.com",
        password="TestPassword123!",
    )

    apartment = Apartment.objects.create(
        unit_number="A101",
        building="Test Building",
        floor=1,
    )

    return user, apartment


@pytest.mark.django_db
def test_issue_str_returns_title(issue_dependencies):
    user, apartment = issue_dependencies

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        title="Broken heater",
        description="The heater is not working.",
    )

    assert str(issue) == "Broken heater"


@pytest.mark.django_db
def test_issue_status_defaults_to_reported(issue_dependencies):
    user, apartment = issue_dependencies

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        title="Broken heater",
        description="The heater is not working.",
    )

    assert issue.status == Issue.IssueStatus.REPORTED


@pytest.mark.django_db
def test_issue_priority_defaults_to_low(issue_dependencies):
    user, apartment = issue_dependencies

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        title="Broken heater",
        description="The heater is not working.",
    )

    assert issue.priority == Issue.Priority.LOW


@pytest.mark.django_db
def test_issue_assigned_to_defaults_to_none(issue_dependencies):
    user, apartment = issue_dependencies

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        title="Broken heater",
        description="The heater is not working.",
    )

    assert issue.assigned_to is None


@pytest.mark.django_db
def test_issue_resolved_on_defaults_to_none(issue_dependencies):
    user, apartment = issue_dependencies

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        title="Broken heater",
        description="The heater is not working.",
    )

    assert issue.resolved_on is None


@pytest.mark.django_db
def test_creating_issue_does_not_notify_assigned_user(issue_dependencies):
    user, apartment = issue_dependencies

    assigned_user = User.objects.create_user(
        username="assigneduser",
        email="assigned@example.com",
        password="TestPassword123!",
    )

    with patch.object(Issue, "notify_assigned_user") as mock_notify:
        Issue.objects.create(
            apartment=apartment,
            reported_by=user,
            assigned_to=assigned_user,
            title="Broken heater",
            description="The heater is not working.",
        )

    mock_notify.assert_not_called()


@pytest.mark.django_db
def test_assigning_user_to_existing_issue_notifies_assigned_user(issue_dependencies):
    user, apartment = issue_dependencies

    assigned_user = User.objects.create_user(
        username="assigneduser",
        email="assigned@example.com",
        password="TestPassword123!",
    )

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        title="Broken heater",
        description="The heater is not working.",
    )

    with patch.object(Issue, "notify_assigned_user") as mock_notify:
        issue.assigned_to = assigned_user
        issue.save()

    mock_notify.assert_called_once()


@pytest.mark.django_db
def test_changing_assigned_user_notifies_new_assigned_user(issue_dependencies):
    user, apartment = issue_dependencies

    first_assignee = User.objects.create_user(
        username="firstassignee",
        email="first@example.com",
        password="TestPassword123!",
    )

    second_assignee = User.objects.create_user(
        username="secondassignee",
        email="second@example.com",
        password="TestPassword123!",
    )

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        assigned_to=first_assignee,
        title="Broken heater",
        description="The heater is not working.",
    )

    with patch.object(Issue, "notify_assigned_user") as mock_notify:
        issue.assigned_to = second_assignee
        issue.save()

    mock_notify.assert_called_once()


@pytest.mark.django_db
def test_saving_issue_without_changing_assignee_does_not_notify(
    issue_dependencies,
):
    user, apartment = issue_dependencies

    assigned_user = User.objects.create_user(
        username="assigneduser",
        email="assigned@example.com",
        password="TestPassword123!",
    )

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        assigned_to=assigned_user,
        title="Broken heater",
        description="The heater is not working.",
    )

    with patch.object(Issue, "notify_assigned_user") as mock_notify:
        issue.title = "Updated heater issue"
        issue.save()

    mock_notify.assert_not_called()


@pytest.mark.django_db
def test_removing_assignee_does_not_notify(issue_dependencies):
    user, apartment = issue_dependencies

    assigned_user = User.objects.create_user(
        username="assigneduser",
        email="assigned@example.com",
        password="TestPassword123!",
    )

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        assigned_to=assigned_user,
        title="Broken heater",
        description="The heater is not working.",
    )

    with patch.object(Issue, "notify_assigned_user") as mock_notify:
        issue.assigned_to = None
        issue.save()

    mock_notify.assert_not_called()

@pytest.mark.django_db
def test_notify_assigned_user_sends_email(issue_dependencies):
    user, apartment = issue_dependencies

    assigned_user = User.objects.create_user(
        username="assigneduser",
        email="assigned@example.com",
        password="TestPassword123!",
    )

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        assigned_to=assigned_user,
        title="Broken heater",
        description="The heater is not working.",
    )

    with (
        patch(
            "core_apps.issues.models.render_to_string",
            return_value="<p>Issue assigned</p>",
        ),
        patch(
            "core_apps.issues.models.EmailMultiAlternatives"
        ) as mock_email,
    ):
        mock_email_instance = mock_email.return_value

        issue.notify_assigned_user()

        mock_email.assert_called_once_with(
            "New Issue Assigned: Broken heater",
            "Issue assigned",
            DEFAULT_FROM_EMAIL,
            ["assigned@example.com"],
        )

        mock_email_instance.attach_alternative.assert_called_once_with(
            "<p>Issue assigned</p>",
            "text/html",
        )

        mock_email_instance.send.assert_called_once()

@pytest.mark.django_db
def test_notify_assigned_user_logs_email_failure(issue_dependencies):
    user, apartment = issue_dependencies

    assigned_user = User.objects.create_user(
        username="assigneduser",
        email="assigned@example.com",
        password="TestPassword123!",
    )

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        assigned_to=assigned_user,
        title="Broken heater",
        description="The heater is not working.",
    )

    with (
        patch(
            "core_apps.issues.models.render_to_string",
            side_effect=Exception("Template rendering failed"),
        ),
        patch("core_apps.issues.models.logger.error") as mock_logger,
    ):
        issue.notify_assigned_user()

    mock_logger.assert_called_once()

    logged_message = mock_logger.call_args[0][0]

    assert "Failed to send issue assignment email" in logged_message
    assert "Broken heater" in logged_message
    assert "Template rendering failed" in logged_message


@pytest.mark.django_db
def test_deleting_assigned_user_sets_assigned_to_none(issue_dependencies):
    user, apartment = issue_dependencies

    assigned_user = User.objects.create_user(
        username="assigneduser",
        email="assigned@example.com",
        password="TestPassword123!",
    )

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        assigned_to=assigned_user,
        title="Broken heater",
        description="The heater is not working.",
    )

    assigned_user.delete()

    issue.refresh_from_db()

    assert issue.assigned_to is None


@pytest.mark.django_db
def test_deleting_apartment_deletes_issue(issue_dependencies):
    user, apartment = issue_dependencies

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        title="Broken heater",
        description="The heater is not working.",
    )

    issue_id = issue.pk

    apartment.delete()

    assert not Issue.objects.filter(pk=issue_id).exists()


@pytest.mark.django_db
def test_deleting_reporter_deletes_issue(issue_dependencies):
    user, apartment = issue_dependencies

    issue = Issue.objects.create(
        apartment=apartment,
        reported_by=user,
        title="Broken heater",
        description="The heater is not working.",
    )

    issue_id = issue.pk

    user.delete()

    assert not Issue.objects.filter(pk=issue_id).exists()

