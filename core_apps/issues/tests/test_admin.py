import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory

from core_apps.common.models import ContentView
from core_apps.apartments.models import Apartment
from core_apps.issues.admin import AssignmentStatusFilter, IssueAdmin
from core_apps.issues.models import Issue
from django.utils import timezone
from django.contrib.messages.storage.fallback import FallbackStorage


User = get_user_model()


@pytest.fixture
def admin_site():
    return AdminSite()


@pytest.fixture
def issue_admin(admin_site):
    return IssueAdmin(Issue, admin_site)


@pytest.fixture
def issue_users():
    reporter = User.objects.create_user(
        username="reporter",
        email="reporter@example.com",
        password="testpass123",
    )
    assigned_user = User.objects.create_user(
        username="electrician",
        email="electrician@example.com",
        password="testpass123",
    )
    assigned_user.profile.occupation = "electrician"
    assigned_user.profile.save()

    unassigned_user = User.objects.create_user(
        username="tenant",
        email="tenant@example.com",
        password="testpass123",
    )

    return reporter, assigned_user, unassigned_user


@pytest.fixture
def apartment():
    return Apartment.objects.create(
        unit_number="A101",
        building="Test Building",
        floor=1,
    )


@pytest.fixture
def issue(issue_users, apartment):
    reporter, assigned_user, _ = issue_users

    return Issue.objects.create(
        apartment=apartment,
        reported_by=reporter,
        assigned_to=assigned_user,
        title="Broken window",
        description="The bedroom window is broken.",
    )


def test_assignment_status_filter_lookups():
    filter_instance = AssignmentStatusFilter(
        request=None,
        params={},
        model=Issue,
        model_admin=None,
    )

    assert filter_instance.lookups(None, None) == (
        ("unassigned", "Unassigned"),
        ("assigned", "Assigned"),
    )


@pytest.mark.django_db
def test_assignment_status_filter_unassigned(issue_users, apartment):
    reporter, _, unassigned_user = issue_users

    Issue.objects.create(
        apartment=apartment,
        reported_by=reporter,
        assigned_to=None,
        title="Unassigned issue",
        description="Needs assignment.",
    )

    assigned_apartment = Apartment.objects.create(
        unit_number="A102",
        building="Test Building",
        floor=1,
    )

    Issue.objects.create(
        apartment=assigned_apartment,
        reported_by=reporter,
        assigned_to=unassigned_user,
        title="Assigned issue",
        description="Already assigned.",
    )

    queryset = Issue.objects.all()

    filter_instance = AssignmentStatusFilter(
        request=None,
        params={"assigned": "unassigned"},
        model=Issue,
        model_admin=None,
    )

    filtered = filter_instance.queryset(None, queryset)

    assert filtered.count() == 1
    assert filtered.first().assigned_to is None


@pytest.mark.django_db
def test_assignment_status_filter_assigned(issue):
    queryset = Issue.objects.all()

    filter_instance = AssignmentStatusFilter(
        request=None,
        params={"assigned": "assigned"},
        model=Issue,
        model_admin=None,
    )

    filtered = filter_instance.queryset(None, queryset)

    assert filtered.count() == 1
    assert filtered.first().assigned_to == issue.assigned_to


@pytest.mark.django_db
def test_issue_admin_configuration(issue_admin):
    assert issue_admin.list_display == [
        "id",
        "apartment",
        "reported_by",
        "assigned_to",
        "status",
        "priority",
        "get_total_views",
    ]

    assert issue_admin.list_display_links == ["id", "apartment"]
    assert issue_admin.list_filter == [
        "status",
        "priority",
        AssignmentStatusFilter,
    ]
    assert issue_admin.search_fields == [
        "apartment__unit_number",
        "reported_by__first_name",
    ]
    assert issue_admin.ordering == ["-created_at"]
    assert issue_admin.autocomplete_fields == [
        "apartment",
        "reported_by",
    ]
    assert issue_admin.actions == ["mark_in_progress", "mark_resolved"]


@pytest.mark.django_db
def test_get_total_views(issue_admin, issue):
    content_type = ContentType.objects.get_for_model(issue)

    ContentView.objects.create(
        content_type=content_type,
        object_id=issue.id,
        user=issue.reported_by,
        viewer_ip="127.0.0.1",
        last_viewed=timezone.now(),
    )

    ContentView.objects.create(
        content_type=content_type,
        object_id=issue.id,
        user=None,
        viewer_ip="127.0.0.2",
        last_viewed=timezone.now(),
    )

    assert issue_admin.get_total_views(issue) == 2


@pytest.mark.django_db
def test_assigned_to_formfield_filters_users(issue_admin, issue_users):
    _, assigned_user, unassigned_user = issue_users

    request = RequestFactory().get("/admin/")

    formfield = issue_admin.formfield_for_foreignkey(
        Issue._meta.get_field("assigned_to"),
        request,
    )

    queryset = formfield.queryset

    assert assigned_user in queryset
    assert unassigned_user not in queryset


@pytest.mark.django_db
def test_assigned_to_formfield_label(issue_admin, issue_users):
    _, assigned_user, _ = issue_users

    request = RequestFactory().get("/admin/")

    formfield = issue_admin.formfield_for_foreignkey(
        Issue._meta.get_field("assigned_to"),
        request,
    )

    assert formfield.label_from_instance(assigned_user) == (
        "electrician@example.com — Electrician"
    )


@pytest.mark.django_db
def test_mark_in_progress_action(issue_admin, issue):
    request = RequestFactory().post("/admin/")
    request.session = {}
    request._messages = FallbackStorage(request)

    issue_admin.mark_in_progress(
        request,
        Issue.objects.filter(pk=issue.pk),
    )

    issue.refresh_from_db()

    assert issue.status == Issue.IssueStatus.IN_PROGRESS


@pytest.mark.django_db
def test_mark_resolved_action(issue_admin, issue):
    request = RequestFactory().post("/admin/")
    request.session = {}
    request._messages = FallbackStorage(request)

    issue_admin.mark_resolved(
        request,
        Issue.objects.filter(pk=issue.pk),
    )

    issue.refresh_from_db()

    assert issue.status == Issue.IssueStatus.RESOLVED
    assert issue.resolved_on == timezone.now().date()