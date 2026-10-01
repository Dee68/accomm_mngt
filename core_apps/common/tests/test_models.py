import pytest
from django.contrib.contenttypes.models import ContentType

from core_apps.common.models import ContentView
from core_apps.profiles.models import Profile
from core_apps.users.models import User


@pytest.mark.django_db
def test_content_view_has_uuid_and_timestamps():
    user = User.objects.create_user(
        username="contentviewuser",
        email="contentviewuser@example.com",
        password="TestPassword123!",
    )

    profile = user.profile

    content_type = ContentType.objects.get_for_model(profile)

    view = ContentView.objects.create(
        content_type=content_type,
        object_id=profile.pkid,
        user=user,
        viewer_ip="192.168.1.10",
        last_viewed="2026-10-01T12:00:00Z",
    )

    assert view.pkid is not None
    assert view.id is not None
    assert view.created_at is not None
    assert view.updated_at is not None

@pytest.mark.django_db
def test_content_view_returns_content_object():
    user = User.objects.create_user(
        username="contentobjectuser",
        email="contentobjectuser@example.com",
        password="TestPassword123!",
    )

    profile = user.profile
    content_type = ContentType.objects.get_for_model(profile)

    view = ContentView.objects.create(
        content_type=content_type,
        object_id=profile.pkid,
        user=user,
        viewer_ip="192.168.1.20",
        last_viewed="2026-10-01T12:00:00Z",
    )

    assert view.content_object == profile

@pytest.mark.django_db
def test_content_view_string_representation_with_user():
    user = User.objects.create_user(
        username="stringuser",
        email="stringuser@example.com",
        password="TestPassword123!",
        first_name="John",
        last_name="Doe",
    )

    profile = user.profile
    content_type = ContentType.objects.get_for_model(profile)

    view = ContentView.objects.create(
        content_type=content_type,
        object_id=profile.pkid,
        user=user,
        viewer_ip="192.168.1.30",
        last_viewed="2026-10-01T12:00:00Z",
    )

    assert str(view) == (
        f"{profile} viewed by John Doe from IP:192.168.1.30"
    )

@pytest.mark.django_db
def test_content_view_string_representation_for_anonymous_user():
    user = User.objects.create_user(
        username="anonymouscontentuser",
        email="anonymouscontentuser@example.com",
        password="TestPassword123!",
    )

    profile = user.profile
    content_type = ContentType.objects.get_for_model(profile)

    view = ContentView.objects.create(
        content_type=content_type,
        object_id=profile.pkid,
        user=None,
        viewer_ip="192.168.1.40",
        last_viewed="2026-10-01T12:00:00Z",
    )

    assert str(view) == (
        f"{profile} viewed by Anonymous from IP:192.168.1.40"
    )

@pytest.mark.django_db
def test_content_view_record_view_creates_view():
    user = User.objects.create_user(
        username="recordviewuser",
        email="recordviewuser@example.com",
        password="TestPassword123!",
    )

    profile = user.profile

    ContentView.record_view(
        content_object=profile,
        user=user,
        viewer_ip="192.168.1.50",
    )

    content_type = ContentType.objects.get_for_model(profile)

    view = ContentView.objects.filter(
        content_type=content_type,
        object_id=profile.pkid,
    ).first()

    assert view is not None
    assert view.user == user
    assert view.viewer_ip == "192.168.1.50"
    assert view.last_viewed is not None

@pytest.mark.django_db
def test_content_view_record_view_does_not_create_duplicate():
    user = User.objects.create_user(
        username="duplicateviewuser",
        email="duplicateviewuser@example.com",
        password="TestPassword123!",
    )

    profile = user.profile

    ContentView.record_view(
        content_object=profile,
        user=user,
        viewer_ip="192.168.1.60",
    )

    ContentView.record_view(
        content_object=profile,
        user=user,
        viewer_ip="192.168.1.60",
    )

    content_type = ContentType.objects.get_for_model(profile)

    assert ContentView.objects.filter(
        content_type=content_type,
        object_id=profile.pkid,
        user=user,
        viewer_ip="192.168.1.60",
    ).count() == 1

@pytest.mark.django_db
def test_content_view_record_view_allows_different_users():
    user1 = User.objects.create_user(
        username="viewerone",
        email="viewerone@example.com",
        password="TestPassword123!",
    )

    user2 = User.objects.create_user(
        username="viewertwo",
        email="viewertwo@example.com",
        password="TestPassword123!",
    )

    profile = user1.profile

    ContentView.record_view(
        content_object=profile,
        user=user1,
        viewer_ip="192.168.1.70",
    )

    ContentView.record_view(
        content_object=profile,
        user=user2,
        viewer_ip="192.168.1.71",
    )

    content_type = ContentType.objects.get_for_model(profile)

    views = ContentView.objects.filter(
        content_type=content_type,
        object_id=profile.pkid,
    )

    assert views.count() == 2
    assert views.filter(user=user1).exists()
    assert views.filter(user=user2).exists()

@pytest.mark.django_db
def test_content_view_record_view_allows_different_ips():
    user = User.objects.create_user(
        username="differentipuser",
        email="differentipuser@example.com",
        password="TestPassword123!",
    )

    profile = user.profile

    ContentView.record_view(
        content_object=profile,
        user=user,
        viewer_ip="192.168.1.80",
    )

    ContentView.record_view(
        content_object=profile,
        user=user,
        viewer_ip="192.168.1.81",
    )

    content_type = ContentType.objects.get_for_model(profile)

    views = ContentView.objects.filter(
        content_type=content_type,
        object_id=profile.pkid,
        user=user,
    )

    assert views.count() == 2
    assert views.filter(viewer_ip="192.168.1.80").exists()
    assert views.filter(viewer_ip="192.168.1.81").exists()

@pytest.mark.django_db
def test_content_view_record_view_allows_anonymous_user():
    user = User.objects.create_user(
        username="anonymousviewer",
        email="anonymousviewer@example.com",
        password="TestPassword123!",
    )

    profile = user.profile

    ContentView.record_view(
        content_object=profile,
        user=None,
        viewer_ip="192.168.1.90",
    )

    content_type = ContentType.objects.get_for_model(profile)

    view = ContentView.objects.get(
        content_type=content_type,
        object_id=profile.pkid,
        user=None,
        viewer_ip="192.168.1.90",
    )

    assert view.user is None
    assert view.viewer_ip == "192.168.1.90"
    assert view.last_viewed is not None

@pytest.mark.django_db
def test_content_view_user_is_set_to_null_when_user_is_deleted():
    user = User.objects.create_user(
        username="deleteviewuser",
        email="deleteviewuser@example.com",
        password="TestPassword123!",
    )

    profile = user.profile
    content_type = ContentType.objects.get_for_model(profile)

    view = ContentView.objects.create(
        content_type=content_type,
        object_id=profile.pkid,
        user=user,
        viewer_ip="192.168.1.100",
        last_viewed="2026-10-01T12:00:00Z",
    )

    view_id = view.pkid

    user.delete()

    view.refresh_from_db()

    assert view.pkid == view_id
    assert view.user is None
    assert ContentView.objects.filter(pkid=view_id).exists()
